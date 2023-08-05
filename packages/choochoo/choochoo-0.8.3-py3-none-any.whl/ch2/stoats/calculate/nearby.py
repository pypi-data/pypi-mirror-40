
from collections import defaultdict, namedtuple
from json import loads

from sqlalchemy import inspect, select, alias, and_, distinct, func

from .. import DbPipeline
from ..names import LONGITUDE, LATITUDE
from ...arty import MatchType
from ...arty.spherical import SQRTree
from ...lib.date import to_time
from ...lib.dbscan import DBSCAN
from ...lib.optimizn import expand_max
from ...squeal.tables.activity import ActivityJournal, ActivityGroup
from ...squeal.tables.constant import Constant
from ...squeal.tables.nearby import ActivitySimilarity, ActivityNearby
from ...squeal.tables.statistic import StatisticName, StatisticJournal, StatisticJournalFloat

Nearby = namedtuple('Nearby', 'constraint, activity_group, border, start, finish, '
                              'latitude, longitude, height, width')


class NearbySimilarityCalculator(DbPipeline):

    def _on_init(self, *args, **kargs):
        super()._on_init(*args, **kargs)
        nearby = self._assert_karg('nearby')
        with self._db.session_context() as s:
            self._config = Nearby(**loads(Constant.get(s, nearby).at(s).value))
        self._log.info('%s: %s' % (nearby, self._config))

    def run(self, force=False, after=None):

        rtree = SQRTree(default_match=MatchType.INTERSECTS, default_border=self._config.border)

        with self._db.session_context() as s:
            if force:
                self._delete(s)
            n_points = defaultdict(lambda: 0)
            self._prepare(s, rtree, n_points, 10000)
            n_intersects = defaultdict(lambda: defaultdict(lambda: 0))
            new_ids = self._measure(s, rtree, n_points, n_intersects, 1000)
            self._save(s, new_ids, n_points, n_intersects, 10000)

    def _delete(self, s):
        self._log.warning('Deleting similarity data for %s' % self._config.constraint)
        s.query(ActivitySimilarity). \
            filter(ActivitySimilarity.constraint == self._config.constraint). \
            delete()

    def _save(self, s, new_ids, n_points, n_intersects, delta):
        n, total = 0, (len(new_ids) * (len(new_ids) - 1)) / 2
        for lo in new_ids:
            for hi in filter(lambda hi: hi > lo, new_ids):
                s.add(ActivitySimilarity(constraint=self._config.constraint,
                                         activity_journal_lo_id=lo, activity_journal_hi_id=hi,
                                         similarity=n_intersects[lo][hi] / (n_points[lo] + n_points[hi])))
                n += 1
                if n % delta == 0:
                    self._log.info('Saved %d / %d for %s' % (n, total, self._config.constraint))

    def _prepare(self, s, rtree, n_points, delta):
        n = 0
        for id_in, lon, lat in self._data(s, new=False):
            p = [(lon, lat)]
            rtree[p] = id_in
            n_points[id_in] += 1
            n += 1
            if n % delta == 0:
                self._log.info('Loaded %s points for %s' % (n, self._config.constraint))

    def _measure(self, s, rtree, n_points, n_intersects, delta):
        new_ids, current_id, seen, n = [], None, None, 0
        for id_in, lon, lat in self._data(s, new=True):
            if id_in != current_id:
                current_id, seen = id_in, set()
                new_ids.append(id_in)
            p = [(lon, lat)]
            for other_p, id_out in rtree.get_items(p):
                if id_in != id_out:
                    if other_p not in seen:
                        lo, hi = min(id_in, id_out), max(id_in, id_out)
                        n_intersects[lo][hi] += 1
                        seen.add(other_p)
            rtree[p] = id_in
            n_points[id_in] += 1
            n += 1
            if n % delta == 0:
                self._log.info('Measured %s points for %s' % (n, self._config.constraint))
        return new_ids

    def _data(self, s, new=True):

        start = to_time(self._config.start)
        finish = to_time(self._config.finish)

        lat = s.query(StatisticName.id).filter(StatisticName.name == LATITUDE).scalar()
        lon = s.query(StatisticName.id).filter(StatisticName.name == LONGITUDE).scalar()
        agroup = s.query(ActivityGroup.id).filter(ActivityGroup.name == self._config.activity_group).scalar()

        sj_lat = inspect(StatisticJournal).local_table
        sj_lon = alias(inspect(StatisticJournal).local_table)
        sjf_lat = inspect(StatisticJournalFloat).local_table
        sjf_lon = alias(inspect(StatisticJournalFloat).local_table)
        aj = inspect(ActivityJournal).local_table
        ns = inspect(ActivitySimilarity).local_table

        existing_lo = select([ns.c.activity_journal_lo_id]). \
            where(ns.c.constraint == self._config.constraint)
        existing_hi = select([ns.c.activity_journal_hi_id]). \
            where(ns.c.constraint == self._config.constraint)
        existing = existing_lo.union(existing_hi).cte()

        stmt = select([sj_lat.c.source_id, sjf_lon.c.value, sjf_lat.c.value]). \
            select_from(sj_lat).select_from(sj_lon).select_from(sjf_lat).select_from(sjf_lat).select_from(aj). \
            where(and_(sj_lat.c.source_id == sj_lon.c.source_id,  # same source
                       sj_lat.c.time == sj_lon.c.time,            # same time
                       sj_lat.c.source_id == aj.c.id,             # and associated with an activity
                       aj.c.activity_group_id == agroup,          # of the right group
                       sj_lat.c.id == sjf_lat.c.id,               # lat sub-class
                       sj_lon.c.id == sjf_lon.c.id,               # lon sub-class
                       sj_lat.c.statistic_name_id == lat,         # lat name
                       sj_lon.c.statistic_name_id == lon,         # lon name
                       sj_lat.c.time >= start.timestamp(),        # time limits
                       sj_lat.c.time < finish.timestamp(),
                       sjf_lat.c.value > self._config.latitude - self._config.height / 2,
                       sjf_lat.c.value < self._config.latitude + self._config.height / 2,
                       sjf_lon.c.value > self._config.longitude - self._config.width / 2,
                       sjf_lon.c.value < self._config.longitude + self._config.width / 2))

        if new:
            stmt = stmt.where(func.not_(sj_lat.c.source_id.in_(existing)))
        else:
            stmt = stmt.where(sj_lat.c.source_id.in_(existing))
        stmt = stmt.order_by(sj_lat.c.source_id)  # needed for seen logic
        yield from s.connection().execute(stmt)


class NearbySimilarityDBSCAN(DBSCAN):

    def __init__(self, log, s, constraint, epsilon, minpts):
        super().__init__(log, epsilon, minpts)
        self.__s = s
        self.__constraint = constraint
        self.__max_similarity = self.__s.query(func.max(ActivitySimilarity.similarity)). \
            filter(ActivitySimilarity.constraint == constraint).scalar()
        # self._log.info('Max similarity %.2f' % self.__max_similarity)

    def run(self):
        candidates = set(x[0] for x in
                         self.__s.query(distinct(ActivitySimilarity.activity_journal_lo_id)).
                         filter(ActivitySimilarity.constraint == self.__constraint).all())
        candidates.union(set(x[0] for x in
                             self.__s.query(distinct(ActivitySimilarity.activity_journal_lo_id)).
                             filter(ActivitySimilarity.constraint == self.__constraint).all()))
        candidates = sorted(candidates)
        # shuffle(candidates)  # skip for repeatability
        return super().run(candidates)

    def neighbourhood(self, candidate, epsilon):
        qlo = self.__s.query(ActivitySimilarity.activity_journal_lo_id). \
            filter(ActivitySimilarity.constraint == self.__constraint,
                   ActivitySimilarity.activity_journal_hi_id == candidate,
                   (self.__max_similarity - ActivitySimilarity.similarity) / self.__max_similarity < epsilon)
        qhi = self.__s.query(ActivitySimilarity.activity_journal_hi_id). \
            filter(ActivitySimilarity.constraint == self.__constraint,
                   ActivitySimilarity.activity_journal_lo_id == candidate,
                   (self.__max_similarity - ActivitySimilarity.similarity) / self.__max_similarity < epsilon)
        return [x[0] for x in qlo.all()] + [x[0] for x in qhi.all()]


class NearbyStatistics(NearbySimilarityCalculator):

    def run(self, force=False, after=None):
        super().run(force=force, after=after)
        with self._db.session_context() as s:
            d_min, _ = expand_max(self._log, 0, 1, 5, lambda d: len(self.dbscan(s, d)))
            self.save(s, self.dbscan(s, d_min))

    def dbscan(self, s, d):
        return NearbySimilarityDBSCAN(self._log, s, self._config.constraint, d, 3).run()

    def save(self, s, groups):
        s.query(ActivityNearby). \
            filter(ActivityNearby.constraint == self._config.constraint).delete()
        for i, group in enumerate(groups):
            self._log.info('Group %d has %d members' % (i, len(group)))
            for activity_journal_id in group:
                s.add(ActivityNearby(constraint=self._config.constraint, group=i,
                                     activity_journal_id=activity_journal_id))


from _csv import reader
from glob import glob
from itertools import zip_longest
from logging import getLogger, basicConfig, DEBUG
from os.path import splitext, split, join, basename
from re import sub
from sys import stdout
from tempfile import TemporaryDirectory
from unittest import TestCase

from ch2.command.args import FIELDS
from ch2.fit.format.read import filtered_records
from ch2.fit.format.records import no_names, append_units, no_bad_values, fix_degrees, chain
from ch2.fit.profile.fields import DynamicField
from ch2.fit.profile.profile import read_external_profile, read_fit
from ch2.fit.summary import summarize, summarize_csv, summarize_tables
from ch2.lib.tests import OutputMixin, HEX_ADDRESS


class TestFit(TestCase, OutputMixin):

    def setUp(self):
        basicConfig(stream=stdout, level=DEBUG)
        self.log = getLogger()

    def test_profile(self):
        nlog, types, messages = read_external_profile(self.log,
                                                      '/home/andrew/project/ch2/choochoo/data/sdk/Profile.xlsx')
        cen = types.profile_to_type('carry_exercise_name')
        self.assertEqual(cen.profile_to_internal('farmers_walk'), 1)
        session = messages.profile_to_message('session')
        field = session.profile_to_field('total_cycles')
        self.assertIsInstance(field, DynamicField)
        for name in field.references:
            self.assertEqual(name, 'sport')
        workout_step = messages.profile_to_message('workout_step')
        field = workout_step.number_to_field(4)
        self.assertEqual(field.name, 'target_value')
        fields = ','.join(sorted(field.references))
        self.assertEqual(fields, 'duration_type,target_type')

    def test_decode(self):
        types, messages, records = \
            filtered_records(self.log,
                             read_fit(self.log,
                                      '/home/andrew/project/ch2/choochoo/data/test/personal/2018-07-26-rec.fit'),
                             profile_path='/home/andrew/project/ch2/choochoo/data/sdk/Profile.xlsx')
        with self.assertFileMatch(
                '/home/andrew/project/ch2/choochoo/data/test/target/TestFit.test_decode',
                filters=[HEX_ADDRESS]) as output:
            for record in records:
                print(record.into(tuple, filter=chain(no_names, append_units, no_bad_values, fix_degrees)),
                      file=output)

    def test_dump(self):
        with self.assertFileMatch(
                '/home/andrew/project/ch2/choochoo/data/test/target/TestFit.test_dump') as output:
            path = '/home/andrew/project/ch2/choochoo/data/test/personal/2018-07-30-rec.fit'
            summarize(self.log, FIELDS, read_fit(self.log, path),
                      profile_path='/home/andrew/project/ch2/choochoo/data/sdk/Profile.xlsx',
                      width=80, output=output)

    def test_developer(self):
        with self.assertFileMatch(
                '/home/andrew/project/ch2/choochoo/data/test/target/TestFit.test_developer') as output:
            path = '/home/andrew/project/ch2/choochoo/data/test/sdk/DeveloperData.fit'
            summarize(self.log, FIELDS, read_fit(self.log, path),
                      profile_path='/home/andrew/project/ch2/choochoo/data/sdk/Profile.xlsx',
                      width=80, output=output)

    def test_csv(self):
        with TemporaryDirectory() as dir:
            skip = Skip(2)  # timer_trigger in ActivityGroup.fit
            for fit_file in glob('/home/andrew/project/ch2/choochoo/data/test/sdk/*.fit'):
                print(fit_file)
                fit_dir, file = split(fit_file)
                name = splitext(file)[0]
                csv_name = '%s.%s' % (name, 'csv')
                csv_us = join(dir, csv_name)
                csv_them = join(fit_dir, csv_name)
                dump_csv(self.log, fit_file, csv_us)
                compare_csv(self.log, csv_us, csv_them, name, skip)
            assert skip.skip == 0, 'Unused skipped tests'

    def test_personal(self):
        for fit_file in glob('/home/andrew/project/ch2/choochoo/data/test/personal/*.fit'):
            file_name = basename(fit_file)
            with self.assertFileMatch(
                    '/home/andrew/project/ch2/choochoo/data/test/target/TestFit.test_personal:' + file_name) as output:
                summarize_tables(self.log, read_fit(self.log, fit_file), width=80, output=output,
                                 profile_path='/home/andrew/project/ch2/choochoo/data/sdk/Profile.xlsx')

    def test_timestamp_16(self):
        types, messages, records = \
            filtered_records(self.log,
                             read_fit(self.log,
                                      '/home/andrew/project/ch2/choochoo/data/test/personal/andrew@acooke.org_24755630065.fit'),
                             profile_path='/home/andrew/project/ch2/choochoo/data/sdk/Profile.xlsx')
        with self.assertFileMatch(
                '/home/andrew/project/ch2/choochoo/data/test/target/TestFit.test_tiemstamp_16',
                filters=[HEX_ADDRESS]) as output:
            for record in records:
                if record.name == 'monitoring':
                    print(record.into(tuple, filter=chain(no_names, append_units, no_bad_values, fix_degrees)),
                          file=output)


def dump_csv(log, fit_file, csv_file):
    with open(csv_file, 'w') as output:
        summarize_csv(log, read_fit(log, fit_file),
                      profile_path='/home/andrew/project/ch2/choochoo/data/sdk/Profile.xlsx',
                      output=output)


# https://docs.python.org/3/library/itertools.html#itertools-recipes
def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


class Skip:

    def __init__(self, skip):
        self.skip = skip

    def __bool__(self):
        try:
            return bool(self.skip)
        finally:
            self.skip -= 1


def cleaned(values):
    # want a good example for scaling errors, not zero
    # also, suspect some 0.0 might be 0.... (remove this later to check)
    return (value[:-2] if value.endswith('.0') else value for value in values)


def compare_rows(log, us, them, name, skip):
    assert us[0:3] == them[0:3] or skip, "%s != %s for %s\n(%s\n%s)" % (us[0:3], them[0:3], name, us, them)
    excess = len(them) % 3
    if excess and not any(them[-excess:]):
        log.debug('Discarding %d empty values from reference' % excess)
        them = them[:-excess]
    while len(them) > len(us) + 2 and not any(them[-3:]):
        them = them[:-3]
    # after first 3 entries need to sort to be sure order is correct
    for us_nvu, them_nvu in zip_longest(sorted(grouper(cleaned(us[3:]), 3)),
                                        sorted(grouper(cleaned(them[3:]), 3))):
        if 'COMPOSITE' not in us_nvu[1]:
            assert us_nvu == them_nvu or skip, "%s != %s for %s\n(%s\n%s)" % (us_nvu, them_nvu, name, us, them)


def compare_csv(log, us, them, name, skip):
    print(us)
    with open(us, 'r') as us_in:
        for line in us_in.readlines():
            print("%s" % line.strip())
            if '\0' in line:
                print(sub('\0', 'NULL', line.strip()))
    print(them)
    with open(them, 'r') as them_in:
        for line in them_in.readlines():
            print("%s" % line.strip())
            if '\0' in line:
                print(sub('\0', 'NULL', line.strip()))
    def filter(us):
        for row in us:
            if row[0] in ('FileHeader', 'Checksum'):
                pass
            elif row[0] == 'DeveloperField':
                yield ['Data'] + row[1:]
            else:
                yield row
    with open(us, 'r') as us_in, open(them, 'r') as them_in:
        us_reader = filter(reader(us_in))
        them_reader = reader(them_in)
        next(them_reader)  # skip titles
        for us_row, them_row in zip_longest(us_reader, them_reader):
            compare_rows(log, us_row, them_row, name, skip)

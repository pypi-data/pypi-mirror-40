
from math import sqrt
from random import uniform, gauss, seed, randrange
from time import time

from ch2.arty.spherical import Global
from ch2.arty.tree import CLRTree, MatchType, CQRTree, CERTree, LQRTree


def known_points(tree):
    tree.add([(0, 0)], '0')
    tree.add([(0, 1)], 'y')
    tree.add([(1, 0)], 'x')
    tree.add([(1, 1)], '1')
    assert len(tree) == 4, len(tree)
    all = list(tree.get([(0, 0), (1, 1)], match=MatchType.CONTAINS))
    assert len(all) == 4, all
    some = list(tree.get([(0, 0), (0, 1)], match=MatchType.CONTAINS))
    assert len(some) == 2, some
    some = list(tree.get([(0, 0), (0, 1)], match=MatchType.CONTAINED))
    assert len(some) == 0, some
    some = list(tree.get([(0, 0), (0, 1)], match=MatchType.EQUALS))
    assert len(some) == 0, some
    assert len(tree) == 4, len(tree)
    tree.delete([(0, 0)])
    assert len(tree) == 3, len(tree)
    some = list(tree.get([(0, 0), (0, 1)], match=MatchType.CONTAINS))
    assert len(some) == 1, some


def test_known_points():
    known_points(CLRTree(max_entries=2))
    known_points(CLRTree())
    known_points(CQRTree(max_entries=2))
    known_points(CQRTree())
    known_points(CERTree(max_entries=2))
    known_points(CERTree())


def known_boxes(tree):
    tree.add([(-0.1, -0.1), (0.1, 0.1)], '0')
    tree.add([(0.9, 0.9), (1.1, 1.1)], '1')
    tree.add([(0, 0), (1, 1)], 'sq')
    tree.add([(2, 2), (3, 3)], 'x')
    some = list(tree.get([(0, 0), (1, 1)], match=MatchType.CONTAINED))
    assert len(some) == 1, some
    some = list(tree.get([(0, 0), (1, 1)], match=MatchType.CONTAINS))
    assert len(some) == 1, some
    some = list(tree.get([(0, 0), (2, 1)], match=MatchType.CONTAINED))
    assert len(some) == 0, some
    some = list(tree.get([(0, 0), (2, 1)], match=MatchType.CONTAINS))
    assert len(some) == 1, some
    some = list(tree.get([(0, 0), (1, 1)], match=MatchType.INTERSECTS))
    assert len(some) == 3, some


def test_known_boxes():
    known_boxes(CLRTree(max_entries=2))
    known_boxes(CLRTree())
    known_boxes(CQRTree(max_entries=2))
    known_boxes(CQRTree())
    known_points(CERTree(max_entries=2))
    known_points(CERTree())


def test_delete_points():

    for size in 2, 3, 4, 8:

        def new_tree():
            tree = CQRTree(max_entries=size)
            for i in range(4):
                for j in range(4):
                    tree.add([(i, j)], i+j)
            assert len(tree) == 16
            return tree

        tree = new_tree()
        tree.delete([(1, 2)])
        assert len(tree) == 15, len(tree)

        tree = new_tree()
        tree.delete([(1, 1), (2, 2)])
        assert len(tree) == 16, len(tree)  # default is EQUALS
        tree = new_tree()
        tree.delete([(1, 1), (2, 2)], match=MatchType.CONTAINS)
        assert len(tree) == 12, len(tree)
        tree = new_tree()
        tree.delete([(1, 1), (2, 2)], match=MatchType.CONTAINED)
        assert len(tree) == 16, len(tree)


def random_box(n, size):
    x = uniform(0, size)
    y = uniform(0, size)
    dx = gauss(0, size/sqrt(n))
    dy = gauss(0, size/sqrt(n))
    return [(x, y), (x + dx, y + dy)]


def gen_random(n, size=100):
    for i in range(n):
        yield 1, random_box(n, size=size)


def test_equals():
    for size in 2, 3, 4, 8:
        tree1 = CQRTree(max_entries=size)
        for i, box in gen_random(10):
            tree1.add(box, i)
        tree2 = CQRTree(max_entries=size)
        for k, v in tree1.items():
            tree2.add(k, v)
        assert tree1 == tree2


def test_underscores():

    for size in 2, 3, 4, 8:
        seed(size)
        tree1 = CQRTree(max_entries=size)
        for i, box in gen_random(10):
            tree1[box] = i
        tree2 = CQRTree(max_entries=size)
        for k, v in tree1.items():
            tree2.add(k, v)
        assert tree1 == tree2
        if size == 2:
            assert str(tree1) == 'Quadratic RTree (10 leaves, 4 height, 1-2 entries)', str(tree1)
        tree3 = CQRTree(tree1.items(), max_entries=size)
        assert tree1 == tree3

    tree = CQRTree()
    tree.add([(1, 1)], '1')
    tree.add([(2, 2)], '2')
    assert len(tree) == 2
    assert [(1, 1)] in tree
    assert not [(3, 3)] in tree
    assert '1' in list(tree.values())
    assert ((1, 1),) in list(tree.keys()), list(tree.keys())
    assert (((1, 1),), '1') in list(tree.items())
    del tree[[(1, 1)]]
    assert len(tree) == 1
    assert list(tree[[(2, 2)]])
    assert list(tree.get([(2, 2)]))
    assert list(tree.get([(2, 2)], value='2'))
    assert not list(tree.get([(2, 2)], value='1'))
    assert tree
    del tree[[(2, 2)]]
    assert not tree


def best_bug(tree):
    for i, (value, box) in enumerate(gen_random(100)):
        tree.add(box, value % 10)
        tree.assert_consistent()


def test_best_bug():
    seed(4)  # 1:46 2:17 3:56 4:8 5:10 6:16 7:58 8:8
    best_bug(CLRTree(max_entries=2))
    best_bug(CQRTree(max_entries=2))
    best_bug(CERTree(max_entries=2))


def stress(type, n_children, n_data, check=True):
    seed(1)
    tree = type(max_entries=n_children)
    data = list(gen_random(n_data))

    for value, box in data:
        tree.add(box, value)
        if check:
            tree.assert_consistent()

    for i in range(10):

        n_delete = randrange(int(1.1 * n_data))   # delete to empty 10% of time
        for j in range(n_delete):
            if data:
                index = randrange(len(data))
                value, box = data[index]
                del data[index]
                tree.delete_one(box, value=value)
                if check:
                    tree.assert_consistent()
            else:
                assert not tree, tree

        while len(data) < n_data:
            value, box = next(gen_random(1))
            data.append((value, box))
            tree.add(box, value)
            if check:
                tree.assert_consistent()

        for j in range(n_data // 4):
            for match in range(4):
                list(tree.get(random_box(10, 100), match=MatchType(match)))


# def test_stress():
#     for type in CLRTree, CQRTree, CERTree:
#         print('type %s' % type)
#         for n_children in 3, 4, 10:
#             print('n_children %d' % n_children)
#             for n_data in 1, 2, 3, 100:
#                 print('n_data %d' % n_data)
#                 stress(type, n_children, n_data)


def test_latlon():
    tree = LQRTree()
    for lon in -180, 180:
        tree.add([(lon, 0)], str(lon))
    for lon in -180, 180:
        found = list(tree.get([(lon, 0)]))
        assert len(found) == 2, found
    area = tree._area_of_mbr(tree._mbr_of_points(tree._normalize_points([(-179, -1), (179, 1)])))
    assert area == 4, area

    tree = LQRTree()
    tree.add([(180, 0)], None)
    assert ((180, 0),) in list(tree.keys()), list(tree.keys())


def test_docs():

    tree = CQRTree()
    square = ((0,0),(0,1),(1,1),(1,0))
    tree[square] = 'square'
    assert list(tree[square]) == ['square']
    assert square in tree
    diagonal = ((0,0),(1,1))
    assert list(tree[diagonal]) == []
    assert not diagonal in tree
    assert list(tree.keys()) == [((0,0),(0,1),(1,1),(1,0))]
    assert list(tree.values()) == ['square']
    assert list(tree.items()) == [(((0,0),(0,1),(1,1),(1,0)), 'square')]
    assert len(tree) == 1
    del tree[square]
    assert len(tree) == 0

    tree = CQRTree(default_match=MatchType.INTERSECTS)
    tree[square] = 'square'
    assert list(tree[diagonal]) == ['square']

    tree = CQRTree(default_match=MatchType.INTERSECTS)
    tree[square] = 'square'
    assert list(tree.get_items(diagonal)) == [(((0,0),(0,1),(1,1),(1,0)), 'square')]


def test_canary():
    tree = CQRTree()
    for i in range(5):
        tree.add([(i, i)], i)
    keys = tree.keys()
    next(keys)
    del tree[[(1, 1)]]
    try:
        next(keys)
        assert False, 'expected error'
    except RuntimeError as e:
        assert 'mutated' in str(e), e


def measure(tree, n_data, n_loops, dim=100):

    seed(1)
    data = list(gen_random(n_data, size=dim))

    start = time()
    for i in range(n_loops):
        for value, box in data:
            tree[box] = value
        assert len(tree) == len(data), len(tree)
        for _, box in data:
            list(tree[box])
        for value, box in data:
            del tree[box]
        assert len(tree) == 0

    return time() - start


def measure_sizes():
    for type in CLRTree, CQRTree, CERTree:
        print()
        for size in 2, 3, 4, 6, 8, 10, 16, 32, 64, 128:
            for subtrees in True, False:
                t = measure(type(max_entries=size, subtrees_flag=subtrees), 1000, 2)
                print('%s %d %s %s' % (type, size, subtrees, t))
                if t > 5 and size > 4:
                    print('abort')
                    return


def test_global():

    def test_point(x, y, z):
        t = Global()
        t.add([(x, y)], z)
        l = list(t.get_items([(x, y)]))
        assert len(l) == 9, l
        for p, q in l:
            assert -0.001 < p[0][0] - x < 0.001, (p, (x, y))
            assert -0.001 < p[0][1] - y < 0.001, (p, (x, y))
            assert q == z, (q, z)

    test_point(0.01, 0.01, 0)
    test_point(179.9, 0.01, 1)
    test_point(-179.9, 0.01, 2)
    test_point(0.01, 89.99, 0)
    test_point(179.9, 89.99, 1)
    test_point(-179.9, 89.99, 2)
    test_point(0.01, -89.99, 0)
    test_point(179.9, -89.99, 1)
    test_point(-179.9, -89.99, 2)


        # for profiling
# PYTHONPATH=. python -m cProfile -s tottime tests/test_arty.py
if __name__ == '__main__':
    stress(CQRTree, 4, 1000, check=False)

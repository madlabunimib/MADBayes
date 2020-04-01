from random import sample
from . import weighted_imputation as wi
OrderedSet = wi.structures.OrderedSet


def test_orderedset():
    # Create empty OrderedSet
    orderedset = OrderedSet()
    # Test empty OrderedSet
    assert(orderedset == set())
    assert(len(orderedset) == 0)

    # Create non-empty OrderedSet
    N = 100
    items = sample(range(N), N)
    orderedset = OrderedSet(items)
    # Equality without order
    assert(orderedset == set(sample(items, N)))
    # Equality with order
    assert([v for v in orderedset] == items)

    # Test repeted element insertion
    orderedset = OrderedSet()
    orderedset.add(1)
    orderedset.add(1)
    assert(orderedset == set([1]))

    # Test element discarding
    orderedset.add(1)
    orderedset.discard(1)
    orderedset.discard(2)
    assert(orderedset == set())

    # Test element removal
    orderedset.add(1)
    orderedset.remove(1)
    try:
        orderedset.remove(2)
        assert(False)
    except KeyError:
        assert(True)
    
    # Test element popping
    orderedset = OrderedSet(items)
    assert(items[0] == orderedset.pop())
    assert(items[1] == orderedset[0])

    # Test items intersection
    N = 100
    A = list(range(0, int(N/2)))
    B = list(range(int(N/3), N))
    assert(
        OrderedSet(A).intersection(set(B)) == \
        set(A).intersection(set(B))
    )
    assert(
        OrderedSet(A).intersection(OrderedSet(B)) == \
        set(A).intersection(set(B))
    )
    assert(
        set(A).intersection(OrderedSet(B)) == \
        set(A).intersection(set(B))
    )

    # Test items union
    N = 100
    A = list(range(0, int(N/2)))
    B = list(range(int(N/3), N))
    assert(
        OrderedSet(A).union(set(B)) == \
        set(A).union(set(B))
    )
    assert(
        OrderedSet(A).union(OrderedSet(B)) == \
        set(A).union(set(B))
    )
    assert(
        set(A).union(OrderedSet(B)) == \
        set(A).union(set(B))
    )

    # Test items difference
    N = 100
    A = list(range(0, int(N/2)))
    B = list(range(int(N/3), N))
    assert(
        OrderedSet(A).difference(set(B)) == \
        set(A).difference(set(B))
    )
    assert(
        OrderedSet(A).difference(OrderedSet(B)) == \
        set(A).difference(set(B))
    )
    assert(
        set(A).difference(OrderedSet(B)) == \
        set(A).difference(set(B))
    )

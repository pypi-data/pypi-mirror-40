# -*- coding: utf-8 -*-
import math


def stripl(l):
    """
    Strips all elements and removes the empty in a list.
    """
    return filter(lambda x:x, map(lambda x: x.strip(), l))


def islice(n, m):
    """
    An iterator splits an amount into several parts, each of which has the
    length of m.
    """
    npiece = int(math.ceil(1.0*n/m))
    for i in range(npiece):
        if (i+1)*m > n:
            yield i, i*m, n
        else:
            yield i, i*m, (i+1)*m

def slice(n, m):
    """
    Similar to `islice` but returns an list instead of an iterator.
    """
    chunks = []
    for piece in islice(n, m):
        chunks.append(piece)
    return chunks

def islicel(l, m):
    """
    An iterator to return slices from the list, each slice has m elements
    except for the last one.
    """
    for i, start, end in islice(len(l), m):
        yield i, l[start:end]

import pandas as pd
import numpy as np
from yo_core._common import Obj
from .generics import KeyValuePair

def _or_default(with_default, default):
    if with_default:
        return default
    raise ValueError("Sequence contains no elements")


def first(en, with_default, default=None):
    for e in en:
        return e
    return _or_default(with_default, default)

def single(en, with_default, default=None):
    firstTime = True
    value = None
    for e in en:
        if firstTime:
            value = e
            firstTime = False
        else:
            raise ValueError('Sequence contains more than one element')
    if not firstTime:
        return value
    return _or_default(with_default, default)

def last(en, with_default, default=None):
    firstTime = True
    value = None
    for e in en:
        if firstTime:
            firstTime = False
        value = e
    if not firstTime:
        return value
    return _or_default(with_default, default)

def count(en):
    counter = 0
    for e in en:
        counter+=1
    return counter

def sum(en):
    result = 0
    for e in en:
        result+= e
    return result


def to_set(en):
    result = set()
    for e in en:
        if e in result:
            raise ValueError("Duplicating element {0}".format(e))
        result.add(e)
    return result


def to_ndarray(en):
    return np.array(list(en))


def _solve_key_value_pair_problem(en):
    isKeyValuePairs = None
    for e in en:
        thisKeyValuePair = isinstance(e,KeyValuePair)
        if isKeyValuePairs is None:
            isKeyValuePairs = thisKeyValuePair
        elif isKeyValuePairs != thisKeyValuePair:
            raise ValueError('The sequence is a mixture of KeyValuePair and something else, which is not allowed')
        yield(e, isKeyValuePairs)





def to_dictionary(en, key_selector, value_selector):
    result = {}
    for e, isKeyValue in _solve_key_value_pair_problem(en):
        if isKeyValue:
            key = e.key
            value = e.value
        else:
            if key_selector is None:
                raise ValueError('The key_selector is not provided, and the sequence is not of KeyValuePair')
            if value_selector is None:
                raise ValueError('The value_selector is not provided, and the sequence is not of KeyValuePair')
            key = key_selector(e)
            value = value_selector(e)
        if key in result:
            raise ValueError('Duplicating value for the key `{0}`'.format(key))
        result[key]=value
    return result

def to_series(en, item_to_value, item_to_index):
    values = []
    index = []
    for e, isKeyValue in _solve_key_value_pair_problem(en):
        if isKeyValue:
            index.append(e.key)
            values.append(e.value)
        else:
            if item_to_index is None:
                index = None
            else:
                index.append(item_to_index(e))
            if item_to_value is None:
                values.append(e)
            else:
                values.append(item_to_value(e))
    return pd.Series(values,index)

def to_dataframe(q, **kwargs):
    data = list(q)
    df = pd.DataFrame(data,**kwargs)
    if len(data)>0 and isinstance(data[0],Obj):
        columns = list(data[0].keys())
        df = df[columns]
    return df

import pytest
from vowpal_platypus.utils import mean, clean, vw_hash_to_vw_str, split_object

def test_mean():
    assert mean([1, 2, 3]) == sum([1, 2, 3]) / 3.0
    assert mean([1]) == 1.0
    assert mean([-1, 1]) == 0.0

def test_clean():
    assert clean('hi') == 'hi'
    assert clean('') == ''
    assert clean('Hi') == 'hi'  # It lowercases
    assert clean('hi, how are you?') == 'hi how are you'  # It removes punctuation

def test_vw_hash_to_vw_str():
    assert vw_hash_to_vw_str({'label': 0, 'f': ['feature'] }) == '0 |f feature'
    assert vw_hash_to_vw_str({'label': '0', 'f': ['feature'] }) == '0 |f feature'
    assert vw_hash_to_vw_str({'label': 1, 'f': ['feature'] }) == '1 |f feature'
    assert vw_hash_to_vw_str({'f': ['feature'] }) == '|f feature'
    assert vw_hash_to_vw_str({'label': -1, 'f': ['feature'] }) == '-1 |f feature'
    assert vw_hash_to_vw_str({'label': 1000, 'f': ['feature'] }) == '1000 |f feature'
    assert vw_hash_to_vw_str({'label': 1.0, 'f': ['feature'] }) == '1.0 |f feature'
    assert vw_hash_to_vw_str({'label': 0.075, 'f': ['feature'] }) == '0.075 |f feature'
    assert vw_hash_to_vw_str({'label': 0, 'f': ['feature', 'other_feature'] }) == '0 |f feature other_feature'
    assert vw_hash_to_vw_str({'label': 0, 'f': {'a': 1}}) == '0 |f a:1'
    assert vw_hash_to_vw_str({'label': 1, 'a': ['a', 'b', 'c'] }) == '1 |a a b c'
    assert vw_hash_to_vw_str({'label': 1, 'a': ['a', 'b', 'c'], 'b': ['d', 'e'] }) == '1 |a a b c |b d e'
    assert vw_hash_to_vw_str({'label': 0, 'f': {'a': 1, 'b': 0.76}}) == '0 |f a:1 b:0.76'
    assert vw_hash_to_vw_str({'label': 0, 'f': {'house': 1, 'apple': 0.76}}) == '0 |f house:1 apple:0.76'
    assert vw_hash_to_vw_str({'label': 0, 'f': ['pizza', {'a': 1, 'b': 0.76}]}) == '0 |f pizza a:1 b:0.76'
    assert vw_hash_to_vw_str({'label': 1, 'importance': 100, 'a': ['a', 'b', 'c'] }) == '1 100 |a a b c'
    with pytest.raises(ValueError) as excinfo:
        vw_hash_to_vw_str({'label': 'bogus', 'f': ['feature'] })
    assert 'Labels passed to VP must be numeric.' in str(excinfo.value)
    with pytest.raises(ValueError) as excinfo:
        vw_hash_to_vw_str({'label': 0, 'f': {'a': 'feature'}})
    assert 'Named values passed to VP must be numeric.' in str(excinfo.value)
    with pytest.raises(ValueError) as excinfo:
        vw_hash_to_vw_str({'label': 0, 'f': {1: 2}})
    assert 'Named values passed to VP must have strings for names.' in str(excinfo.value)
    with pytest.raises(ValueError) as excinfo:
        assert vw_hash_to_vw_str({'label': 0, 'feature': ['feature'] })
    assert 'Namespaces passed to VP must be length-1 strings.' in str(excinfo.value)
    with pytest.raises(ValueError) as excinfo:
        assert vw_hash_to_vw_str({'label': 0, 1: ['feature'] })
    assert 'Namespaces passed to VP must be length-1 strings.' in str(excinfo.value)

def test_split_object_list():
    assert split_object([1], 1) == [[1]]
    assert split_object([1, 2], 1) == [[1, 2]]
    assert split_object([1, 2], 2) == [[1], [2]]
    assert split_object([1, 2, 3, 4, 5], 1) == [[1, 2, 3, 4, 5]]
    assert split_object([1, 2, 3, 4], 2) == [[1, 2], [3, 4]]
    assert split_object([1, 2, 3, 4, 5], 2) == [[1, 2, 3], [4, 5]]
    assert split_object([1, 2, 3, 4, 5, 6], 3) == [[1, 2], [3, 4], [5, 6]]
    assert split_object(['a', 'b', 'c', 'd'], 2) == [['a', 'b'], ['c', 'd']]
    assert split_object(['a', 1, 'c', 4], 2) == [['a', 1], ['c', 4]]
    assert split_object([[1, 2], [3, 4], [5, 6], [7, 8]], 2) == [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]
    with pytest.raises(ValueError) as excinfo:
        split_object([1, 2], 4)
    assert 'smaller (length 2)' in str(excinfo.value)
    assert 'splits (4)' in str(excinfo.value)

def test_split_object_dictionary():
    assert split_object({'a': 1}, 1) == [{'a': 1}]
    assert split_object({'a': 1, 'b': 2}, 1) == [{'a': 1, 'b': 2}]
    assert split_object({'a': 1, 'b': 2}, 2) == [{'a': 1}, {'b': 2}]
    assert split_object({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}, 1) == [{'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}]
    obj = split_object({'a': 1, 'b': 2, 'c': 3, 'd': 4}, 2)
    assert isinstance(obj, list)
    assert len(obj) == 2
    assert map(len, obj) == [2, 2]
    assert sorted(sum(map(lambda x: x.keys(), obj), [])) == ['a', 'b', 'c', 'd']
    obj = split_object({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}, 2)
    assert isinstance(obj, list)
    assert len(obj) == 2
    assert map(len, obj) == [3, 2]
    assert sorted(sum(map(lambda x: x.keys(), obj), [])) == ['a', 'b', 'c', 'd', 'e']
    obj = split_object({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6}, 2)
    assert len(obj) == 2
    assert map(len, obj) == [3, 3]
    assert sorted(sum(map(lambda x: x.keys(), obj), [])) == ['a', 'b', 'c', 'd', 'e', 'f']
    obj = split_object({'a': 'a', 'b': 'b', 'c': 'c', 'd': 'd'}, 2)
    assert len(obj) == 2
    assert map(len, obj) == [2, 2]
    assert sorted(sum(map(lambda x: x.keys(), obj), [])) == ['a', 'b', 'c', 'd']
    obj = split_object({'a': 'a', 'b': 'b', 'c': 'c', 'd': 'd', 'e': 'e', 'f': 'f'}, 3)
    assert len(obj) == 3
    assert map(len, obj) == [2, 2, 2]
    assert sorted(sum(map(lambda x: x.keys(), obj), [])) == ['a', 'b', 'c', 'd', 'e', 'f']
    obj = split_object({'a': 'a', 'b': 1, 'c': 'c', 'd': 4}, 2)
    assert len(obj) == 2
    assert map(len, obj) == [2, 2]
    assert sorted(sum(map(lambda x: x.keys(), obj), [])) == ['a', 'b', 'c', 'd']
    obj = split_object({'a': [1, 2], 'b': [3, 4], 'c': [5, 6], 'd': [7, 8]}, 2)
    assert len(obj) == 2
    assert map(len, obj) == [2, 2]
    assert sum(map(lambda x: map(len, x), map(lambda x: x.values(), obj)), []) == [2, 2, 2, 2]
    with pytest.raises(ValueError) as excinfo:
        split_object({'a': 1, 'b': 2, 'c': 3}, 5)
    assert 'smaller (length 3)' in str(excinfo.value)
    assert 'splits (5)' in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        split_object('apple', 2)
    assert 'should be a list or a dictionary. Instead a str was passed' in str(excinfo.value)

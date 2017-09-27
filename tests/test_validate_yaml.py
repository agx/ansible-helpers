import os

from validate_yamls import check_tree


def test_failure():
    dir = 'tests/data/invalid_yaml'
    assert os.path.exists(dir)
    errors = check_tree(dir)
    assert len(errors) == 1
    assert errors[0].problem == "could not find expected ':'"


def test_filter():
    dir = 'tests/data/invalid_yaml'
    assert os.path.exists(dir)
    errors = check_tree(dir, lambda x: x.endswith('/bla.yml'))
    assert len(errors) == 0

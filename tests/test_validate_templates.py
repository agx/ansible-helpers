import os

from validate_templates import check_tree


def test_failure():
    dir = 'tests/data/invalid_template'
    assert os.path.exists(dir)
    errors = check_tree(dir)
    assert len(errors) == 1
    assert errors[0].template == os.path.join(dir, 'bla.j2')


def test_filter():
    dir = 'tests/data/invalid_template'
    assert os.path.exists(dir)
    errors = check_tree(dir, lambda x: x.endswith('/bla.j2'))
    assert len(errors) == 0

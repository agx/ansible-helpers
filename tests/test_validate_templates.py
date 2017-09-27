import os

import validate_templates


def setup():
    validate_templates.env = validate_templates.setup_jinja2_env()


def test_failure():
    dir = 'tests/data/invalid_template'
    assert os.path.exists(dir)
    errors = validate_templates.check_tree(dir)
    assert len(errors) == 1
    assert errors[0].template == os.path.join(dir, 'bla.j2')


def test_filter():
    dir = 'tests/data/invalid_template'
    assert os.path.exists(dir)
    errors = validate_templates.check_tree(dir, lambda x: x.endswith('/bla.j2'))
    assert len(errors) == 0

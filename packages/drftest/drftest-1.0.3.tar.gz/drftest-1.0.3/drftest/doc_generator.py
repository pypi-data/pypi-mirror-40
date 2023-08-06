import os
import shutil
import textwrap

from django.conf import settings
from django.template import loader
from django.utils.safestring import mark_safe

"""
{
    'method': 'POST',
    'data': {'a': 'b'},
    'url': '/api/somewhere',
    'url_kwargs': {'a': 'b'},
    'format': 'json',
    'headers': {'a': 'b'},
    'success': 200 <= {response_status_cod} < 300,
    'meta': {
        'docs': '{docstring_for_the_test}',
        'method_name': '{Name of method being tested}',
        'class_name': '{Name of class containing the test}',
        'app_name': 'Name of django app containing the test'
    },
    'response': {
        'data': {'a': 'b'},
        'status': {response status code. eg. 200},
    }
}
"""
store = []
"""
class_docs keeps a dictionary which maps name of test class to its docs.
"""
class_docs = {}


def _categorize_store():
    """
    doc entry for each test case in `BaseViewTest` is a flat dictionary. with no categorization
    based on app, class or method.

    This function categorizes items in that list by (first) app_name and (secondly) class_name.
    """
    categorized = {}
    for test_result in store:
        app_name = test_result['meta']['app_name']
        class_name = test_result['meta']['class_name']
        if app_name not in categorized:
            categorized[app_name] = {}
        if class_name not in categorized[app_name]:
            categorized[app_name][class_name] = {
                'tests': [],
                'description': textwrap.dedent(mark_safe(class_docs.get(class_name) or '')),
            }
        categorized[app_name][class_name]['tests'].append(test_result)
    return categorized


def _get_root_dir():
    """
    mkdocs has a yml file and a docs directory containing yml files. Both of these two
    reside in a directory indicated by settings.DRF_TEST_DOCS_DIR which will be referred to
    as root directory.
    """
    return os.path.expanduser(settings.DRF_TEST_DOCS_DIR)


def _get_docs_path():
    return os.path.join(_get_root_dir(), 'docs')


def _clear_docs_path():
    """
    Removes everything in docs directory in order to prepare it for new docs.
    """
    docs_path = _get_docs_path()
    if os.path.exists(docs_path):
        if os.path.isdir(docs_path):
            shutil.rmtree(docs_path)
        else:
            os.remove(docs_path)
    os.mkdir(docs_path)


def _rewrite_yml(root_dir: str):
    yml_path = os.path.join(root_dir, 'mkdocs.yml')
    with open(yml_path, 'w+') as yml_file:
        yml_file.write('site_name: DRF Tests\n')
        yml_file.write('theme: readthedocs\n')


def write_docs():
    if not hasattr(settings, 'DRF_TEST_DOCS_DIR') or not settings.DRF_TEST_DOCS_DIR:
        return

    if not os.path.exists(_get_root_dir()):
        os.mkdir(_get_root_dir())

    _clear_docs_path()
    for app_name, app_docs in _categorize_store().items():
        md_path = os.path.join(_get_docs_path(), '{}.md'.format(app_name))
        t = loader.get_template('doc_of_app.md')
        rendered = t.render({
            'app_name': app_name,
            'app_docs': app_docs,
        })
        with open(md_path, 'w+') as md_file:
            md_file.write(rendered)
    index_path = os.path.join(_get_docs_path(), 'index.md')
    with open(index_path, 'w+') as index_file:
        index_file.write("""
# Welcome

Welcome to *DRF Test* documentation.

This documentation is categorized according to subsystems of your code.
Name of each subsystem is given in the navigation menu. You can click on
each item to visit documentation of that subsystem.

Happy coding :)
        """)

    _rewrite_yml(_get_root_dir())

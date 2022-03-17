"""
Info: Run tests, builds and other tasks using doit
--------------------------------------------------
Installing doit: pip install doit
------------------------------------
Command to list the tasks titles-
doit list

Command to check all the info for a task-
doit info <task-title>

Help command-
doit help <task-title>

Targeted run for individual task-
Examples:
        $ doit build
        $ doit test -m <flag> -f <module name>
        $ doit doc-build
        $ doit bench --flag -s / doit bench -m -s
        $ doit bench --flag -t / doit bench -m -t
        $ doit release-authors -p 1.7.0 -c 1.8.0
        $ doit release-notes -p 1.7.0 -c 1.8.0
"""
DOIT_CONFIG = {'verbosity': 2}
PARAMS_RELEASE = [{'name': 'start_revision',
                   'short': 'p',
                   'default': '',
                   'type': str},
                  {'name': 'end_revision',
                   'short': 'c',
                   'default': '',
                   'type': str}]


def task_build():
    """
    Scipy build task
    """
    return {'actions': ["python dev.py --build-only"],
            'doc': 'Task: Initializing build task'
            }


def task_test():
    """
    Runs the tests for a given module
    """

    return {'actions': ["python dev.py --no-build %(flag)s %(module)s"],
            'doc': 'Task: Initializing tests for the chosen module',
            'params': [{'name': 'flag',
                        'short': 'm',
                        'default': '',
                        'type': str,
                        'help': 'Enter flag parameter options: -s or -t'},
                       {'name': 'module',
                        'short': 'f',
                        'default': '',
                        'type': str,
                        'help': 'Enter the module name to run tests'}]
            }


def task_bench():
    """
    Runs benchmark tasks
    """
    return {'actions': ["python dev.py --bench %(param)s integrate.SolveBVP"],
            'doc': 'Task: Initializing benchmarking task',
            'params': [{'name': 'param',
                        'long': 'flag',
                        'short': 'm',
                        'default': '',
                        'type': str,
                        'help': 'Enter flag parameter options: -s or -t'}]
            }


def task_doc_build():
    """
    Task group with dependency for document build
    Task calls: build
    """
    return {'actions': ['python dev.py --doc'],
            'basename': 'doc-build',
            'doc': 'Task Group: Initializing document build tasks',
            'task_dep': ['build']
            }


def gen_release_tasks():
    """
    Task generator for release tasks
    """
    yield {'actions': ["python tools/authors.py v%(start_revision)s..v%(end_revision)s"],
           'basename': 'release-authors',
           'params': PARAMS_RELEASE,
           'doc': 'Task: Initializing create author list'}
    yield {'actions': ["python tools/write_release_and_log.py v%(start_revision)s v%(end_revision)s"],
           'basename': 'release-notes',
           'params': PARAMS_RELEASE,
           'doc': 'Task: Initializing create release notes'}


def task_release():
    """
    Call to task generator: gen_release_tasks()
    """
    yield gen_release_tasks()

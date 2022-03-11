import sys
import inspect

from doit.cmd_base import ModuleTaskLoader
from doit.doit_cmd import DoitMain
import click


#doit -f decorator_test_cli.py list
#python decorator_test_cli.py my-echo


#####################################
# to be extracted into a doit_click.py.

def run_doit_task(task_name):
    def callback():
        loader = ModuleTaskLoader(globals())
        doit_main = DoitMain(loader, extra_config={'GLOBAL': {'verbosity': 2}})
        sys.exit(doit_main.run([task_name]))
    return callback


class ClickDoit(click.Group):
    """
    subclass with an extra decorator used to create commands from doit task_creators (instead of plain function)
    """

    def click_cmd(self, name=None, **attrs):
        def decorator(creator):
            task_name = creator.__name__[5:] # 5 is len('task_')
            cmd_name = name if name else task_name
            cmd_help = inspect.getdoc(creator)
            cmd = click.Command(name=cmd_name, callback=run_doit_task(task_name, **attrs), help=cmd_help)
            self.add_command(cmd)
            return creator # return original task_creator to be used by doit itself
        return decorator



#######################################
# execute tasks through click based CLI
cli = ClickDoit()


@click.argument('name', default='guest')
@click.argument('age', type=int)
@cli.click_cmd('my-echo', name, age)
def task_hello(name, age):
   return {'actions': [f'echo {name} is {age} years old'],
           'doc': 'test'
           }


@cli.click_cmd('hello2')
def task_hello2():
    import sys
    m = sys.argv[4]
    return {'actions': [f'echo is {m} years old'],
            'doc': 'test..........'
            }


if __name__ == '__main__':
    hello()
    # hello2()

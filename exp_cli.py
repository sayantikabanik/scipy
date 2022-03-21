from doit import task_params
import click
from click.globals import push_context

import inspect
import sys
import os
from doit.cmd_base import ModuleTaskLoader, get_loader
from doit.doit_cmd import DoitMain
from doit.cmdparse import DefaultUpdate, CmdParse, CmdParseError
from doit.exceptions import InvalidDodoFile, InvalidCommand, InvalidTask

from rich_click import RichCommand, RichGroup
from rich.console import Console
from rich.syntax import Syntax

opt_build_dir = {
    'name': 'build_dir',
    'long': 'build-dir',
    'default': 'build',
    'help': "Relative path to build directory. Default is 'build'",
}

opt_install_prefix = {
    'name': 'install_prefix',
    'long': 'install-prefix',
    'default': None,
    'help': "Relative path to the install directory. Default is <build-dir>-install.",
}


class DoitMainAPI(DoitMain):
    """add new method to run tasks with parsed command line"""

    def run_tasks(self, task):
        """
        :params task: str - task name
        """

        # get list of available commands
        sub_cmds = self.get_cmds()
        task_loader = get_loader(self.config, self.task_loader, sub_cmds)

        # execute command
        cmd_name = 'run'
        command = sub_cmds.get_plugin(cmd_name)(
            task_loader=task_loader,
            config=self.config,
            bin_name=self.BIN_NAME,
            cmds=sub_cmds,
            opt_vals={},
        )

        try:
            cmd_opt = CmdParse(command.get_options())
            params, _ = cmd_opt.parse([])
            args = [task]
            command.execute(params, args)
        except (CmdParseError, InvalidDodoFile,
                InvalidCommand, InvalidTask) as err:
            if isinstance(err, InvalidCommand):
                err.cmd_used = cmd_name
                err.bin_name = self.BIN_NAME
            raise err


def param_doit2click(task_param: dict):
    """converts a doit TaskParam to Click.Parameter"""
    param_decls = [task_param['name']]
    if 'long' in task_param:
        param_decls.append(f"--{task_param['long']}")
    if 'short' in task_param:
        param_decls.append(f"-{task_param['short']}")
    return click.Option(param_decls, default=task_param['default'], help=task_param.get('help'))


def run_doit_task(task_name, **kwargs):
    """:param kwargs: contain task_opts"""
    loader = ModuleTaskLoader(globals())
    loader.task_opts = {task_name: kwargs}
    doit_main = DoitMainAPI(loader, extra_config={'GLOBAL': {'verbosity': 2}})
    return doit_main.run_tasks(task_name)


def doit_task_callback(task_name):
    def callback(**kwargs):
        sys.exit(run_doit_task(task_name, **kwargs))

    return callback


class ClickDoit(RichGroup):
    """
    subclass with an extra decorator used to create commands from doit task_creators
    (instead of plain function)
    """

    def task_as_cmd(self, name=None, **attrs):
        def decorator(creator):
            task_name = creator.__name__[5:]  # 5 is len('task_')
            cmd_name = name if name else task_name
            cmd_help = inspect.getdoc(creator)
            task_params = getattr(creator, '_task_creator_params', None)

            # convert doit task-params to click params
            params = []
            # if param is already define in group, do not add again
            group_options = set(par.name for par in self.params)
            if task_params:
                for tp in task_params:
                    if tp['name'] in group_options:
                        continue
                    params.append(param_doit2click(tp))
            cmd = click.Command(
                name=cmd_name,
                callback=doit_task_callback(task_name),
                help=cmd_help,
                params=params,
            )
            self.add_command(cmd)
            return creator  # return original task_creator to be used by doit itself

        return decorator


@click.group(cls=ClickDoit)
@click.option('--build-dir', default='build', help=opt_build_dir['help'])
@click.option('--install-prefix', default=None, help=opt_install_prefix['help'])
@click.pass_context
def cli(ctx, build_dir, install_prefix):
    ctx.ensure_object(dict)
    ctx.obj['build_dir'] = build_dir
    ctx.obj['install_prefix'] = install_prefix


@cli.task_as_cmd()
@task_params([{'name': 'start', 'long': 'log-start', 'default': None,
               'help': 'log start version'},
              {'name': 'end', 'long': 'log-end', 'default': None,
               'help': 'log end version'}
              ])
def task_notes(start, end):
    """Release notes."""
    cmd = f'python tools/write_release_and_log.py v{start} v{end}'
    click.echo(cmd)
    return {
        'actions': [cmd],
        'verbosity': 2
    }


if __name__ == '__main__':
    cli()
else:
    # make sure click.pass_obj decorator still works when running with plain doit
    push_context(click.core.Context(cli, obj={}))

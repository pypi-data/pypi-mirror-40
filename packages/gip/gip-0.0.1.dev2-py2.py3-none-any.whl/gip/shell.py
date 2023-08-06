import click
import click_completion

from gip import command

click_completion.init()


@click.group()
@click.option(
    '--debug/--no-debug',
    default=False,
    help='Enable or disable debug mode. Default is disabled.'
)
@click.option(
    '--gitlab-token',
    default=False,
    help='Provide the private token for the Gitlab API'
)
@click.option(
    '--github-token',
    default=False,
    help='Provide the private token for the Github API'
)
@click.version_option(version='0.0.1')
@click.pass_context
def main(ctx, debug, gitlab_token, github_token):
    """
    \b
     _______ __
    |     __|__|.-----.
    |    |  |  ||  _  |
    |_______|__||   __|
                |__|
    Gip is a language agnostic dependency manager
    which uses API calls to pull repositories.

    Enable autocomplete issue:
      eval "$(_GIP_COMPLETE=source gip)"
    """
    ctx.obj = {}
    ctx.obj['args'] = {}
    ctx.obj['args']['debug'] = debug
    ctx.obj['args']['gitlab_token'] = gitlab_token
    ctx.obj['args']['github_token'] = github_token


main.add_command(command.install.install)

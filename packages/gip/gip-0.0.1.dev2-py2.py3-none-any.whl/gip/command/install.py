import click
import logging
import pathlib
from urllib.parse import urlsplit

from gip import logger
from gip import parser
from gip.sources import github, gitlab

LOG = logger.get_logger(__name__)


def _get_base_url(repo):
    """ Return base url of repo url"""
    # Split repo url in parts
    split_url = urlsplit(repo)
    return "{0}://{1}".format(split_url.scheme, split_url.netloc)


@click.command()
@click.pass_context
@click.option(
    '--requirements',
    '-r',
    default=None,
    help='Requirements file to install')
def install(ctx, requirements):
    """
    Install dependencies
    """
    args = ctx.obj.get('args')
    requirements = parser.parse_requirements_file(requirements)

    for requirement in requirements:
        source = None

        if requirement['type'] == 'gitlab':
            # Repo comes from Gitlab, check for API token
            if args['gitlab_token']:
                # Init gitlab object
                source = gitlab.Gitlab(
                    url=_get_base_url(repo=requirement['repo']),
                    token=args['gitlab_token']
                )
            else:
                LOG.warn("No Gitlab API token provided")
                return

        elif requirement['type'] == 'github':
            # Repo comes from Github check for API token
            if args['github_token']:
                # Init Github object
                source = github.Github(
                    token=args['github_token']
                )
            else:
                LOG.warn("No Github API token provided")
                return

        if source:
            # Convert dest to absolute path
            dest = pathlib.Path(requirement['dest']).resolve()
            archive_name = "{}.zip".format(requirement['name'])
            # Append name to destination directory
            archive_dest = dest.joinpath(archive_name)

            # Get the archive
            try:
                source.get_archive(
                    repo=requirement['repo'],
                    version=requirement['version'],
                    dest=archive_dest
                )
            except Exception as e:
                LOG.exception(e)

            # Extract archive to location
            try:
                source.extract_archive(
                    src=archive_dest,
                    dest=dest,
                    name=requirement['name']
                )
            except Exception as e:
                LOG.exception(e)
        else:
            LOG.warn('{} has no valid type'.format(requirement['name']))

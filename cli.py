import click
import os
import logging
from github import Github
from gitlab import Gitlab


USER_DATA_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'userdata')


def init_user_data_dir():
    if not os.path.exists(USER_DATA_PATH):
        os.mkdir(USER_DATA_PATH)


@click.command()
@click.option('-t', '--token',
              prompt='Your GitHub access token', hide_input=True, help="Your personal GitHub access token")
@click.option('-e', '--exclude', multiple=True, type=str, help="Excludes these repositories from being exported")
@click.option('-v', '--verbose', is_flag=True, help='Enables verbose logging')
def export_from_github(token, exclude, verbose):
    init_user_data_dir()

    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    github = Github(token, USER_DATA_PATH)
    gitlab = Gitlab(token, USER_DATA_PATH)
    repo_names = set(github.list_all_repo_name())

    for exclude_repo in exclude:
        repo_names.remove(exclude_repo)

    for repo_name in repo_names:
        # parallelize this work with threading and generators
        tar_path = github.download_repo(repo_name)
        gitlab.export(tar_path)


if __name__ == '__main__':
    export_from_github()

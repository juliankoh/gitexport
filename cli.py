import click
from github import Github
import os
import logging


USER_DATA_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'userdata')


def init_user_data_dir():
    if not os.path.exists(USER_DATA_PATH):
        os.mkdir(USER_DATA_PATH)


@click.command()
@click.option('-t', '--token',
              prompt='Your GitHub access token', hide_input=True, help="Your personal GitHub access token")
@click.option('-e', '--exclude', multiple=True, type=str)
@click.option('-v', '--verbose', type=bool)
def export_from_github(token, exclude, verbose):
    init_user_data_dir()

    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    github = Github(token)
    repo_names = set(github.list_all_repo_name())

    for exclude_repo in exclude:
        repo_names.remove(exclude_repo)

    for repo_name in repo_names:
        # parallelize this work with threading and generators
        github.download_repo(repo_name, USER_DATA_PATH)


if __name__ == '__main__':
    export_from_github()

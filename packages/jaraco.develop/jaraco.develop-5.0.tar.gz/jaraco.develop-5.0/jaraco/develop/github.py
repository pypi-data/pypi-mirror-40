import pprint
import argparse
import getpass

import keyring
from github import Github


def create_repository(name):
	org, sep, name = name.rpartition('/')
	username = getpass.getuser()
	token = keyring.get_password('github.com', username)
	g = Github(token)
	owner = g.get_organization(org) if org else g.get_user()
	return owner.create_repo(name)


def create_repo_cmd():
	parser = argparse.ArgumentParser()
	parser.add_argument('repo_name')
	args = parser.parse_args()
	repo = create_repository(args.repo_name)
	pprint.pprint(repo.url)

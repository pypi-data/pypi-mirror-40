from __future__ import print_function

import os
from pygit2 import Repository, GIT_SORT_TOPOLOGICAL, GIT_SORT_REVERSE

from git_additions.additions.__helpers import find_toplevel


class Users(object):
    @staticmethod
    def report():
        max_name_length = 0
        max_email_length = 0

        authors = dict()
        repo = Repository('%s/.git' % find_toplevel(os.getcwd()))
        for commit in repo.walk(repo.head.target, GIT_SORT_TOPOLOGICAL | GIT_SORT_REVERSE):
            if commit.author.email not in authors.keys():
                authors[commit.author.email] = dict()
                authors[commit.author.email]['author'] = commit.author
                authors[commit.author.email]['commits'] = 1
                if len(commit.author.name) > max_name_length:
                    max_name_length = len(commit.author.name)
                if len(commit.author.email) > max_email_length:
                    max_email_length = len(commit.author.email)
            else:
                authors[commit.author.email]['commits'] += 1

        print(
            'Name'.ljust(max_name_length), '\t',
            'Email'.ljust(max_email_length), '\t',
            'Commits'
        )

        print(
            '_' * max_name_length, '\t',
            '_' * max_email_length, '\t',
            '_' * 7
        )
        for email, author in authors.items():
            print(
                author['author'].name.ljust(max_name_length), '\t',
                author['author'].email.ljust(max_email_length), '\t',
                author['commits']
            )

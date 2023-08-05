from __future__ import print_function

import os

import pygit2
from colorama import Fore, Style

from git_additions.additions.__helpers import find_toplevel


class Stats(object):

    def __init__(self, options):
        self.__options = options

    def report(self):
        repo = pygit2.Repository('%s/.git' % find_toplevel(os.getcwd()))
        if self.__options.short:
            self.short(repo)
        else:
            self.stats(repo)

    def stats(self, repo):
        previous_commit = None
        for commit in repo.walk(repo.head.target, pygit2.GIT_SORT_TOPOLOGICAL | pygit2.GIT_SORT_REVERSE):
            if previous_commit is not None:
                diff = commit.tree.diff_to_tree(previous_commit.tree)
                print('#%s%s' % (Fore.CYAN, commit.short_id), end='\t')
                print(
                    '%s%s%s <%s>%s' % (Fore.YELLOW, commit.author.name, Style.DIM, commit.author.email, Style.NORMAL),
                    end='\t'
                )
                print('%sf: %s' % (Fore.BLUE, diff.stats.files_changed), end='\t')
                print('%s+: %s' % (Fore.GREEN, diff.stats.insertions,), end='\t')
                print('%s-: %s' % (Fore.RED, diff.stats.deletions,), end='\t')
                if self.__options.message:
                    print('%s%s' % (Fore.LIGHTBLUE_EX, str(commit.message).strip()), end='\t')
                print(Style.RESET_ALL)
            previous_commit = commit

    @staticmethod
    def short(repo):
        previous_commit = None
        report = dict()
        total_files_changed = 0
        total_insertions = 0
        total_deletions = 0
        max_author_length = 0
        for commit in repo.walk(repo.head.target, pygit2.GIT_SORT_TOPOLOGICAL | pygit2.GIT_SORT_REVERSE):
            if previous_commit is not None:
                diff = commit.tree.diff_to_tree(previous_commit.tree)
                key = '%s-%s' % (commit.author.name, commit.author.email)
                if max_author_length < len(key):
                    max_author_length = len(key)
                if key not in report.keys():
                    report[key] = {'files_changed': 0, 'insertions': 0, 'deletions': 0}

                report[key]['files_changed'] += diff.stats.files_changed
                report[key]['insertions'] += diff.stats.insertions
                report[key]['deletions'] += diff.stats.deletions

                total_files_changed += diff.stats.files_changed
                total_insertions += diff.stats.insertions
                total_deletions += diff.stats.deletions

            previous_commit = commit
        for key in report.keys():
            author = str(key).split('-')
            print(
                '%s%s%s <%s>%s' % (Fore.YELLOW, author[0], Style.DIM, author[1], Style.NORMAL),
                ' ' * (max_author_length - len(key)),
                end=' '
            )
            print(
                '%sf: %s' % (Fore.BLUE, report[key]['files_changed']),
                ' ' * (len(str(total_files_changed)) - len(str(report[key]['files_changed']))), end=' '
            )
            print(
                '%s+: %s' % (Fore.GREEN, report[key]['insertions']),
                ' ' * (len(str(total_insertions)) - len(str(report[key]['insertions']))), end=' '
            )
            print('%s-: %s' % (Fore.RED, report[key]['deletions']))

        print('%sTotal' % Fore.YELLOW, ' ' * (max_author_length - 3), end=' ')
        print('%sf: %s' % (Fore.BLUE, total_files_changed), end='  ')
        print('%s+: %s' % (Fore.GREEN, total_insertions), end='  ')
        print('%s-: %s' % (Fore.RED, total_deletions))


Stats(None).short(pygit2.Repository('/Users/indrajit/_WORKSPACE/ROBI/myrobi/.git'))

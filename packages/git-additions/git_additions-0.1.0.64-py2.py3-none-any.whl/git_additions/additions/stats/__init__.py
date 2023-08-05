from optparse import OptionParser

from git_additions.additions.stats.stats import Stats


def runner():
    parser = OptionParser()
    parser.add_option(
        "-m", "--message", action="store_true", dest="message", default=False, help="Show Commit Message"
    )
    parser.add_option(
        "-s", "--short", action="store_true", dest="short", default=False, help="Show Short Stat"
    )
    (options, args) = parser.parse_args()
    Stats(options).report()

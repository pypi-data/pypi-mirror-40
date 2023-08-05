from optparse import OptionParser

from git_additions.additions.logs.logs import Logs


def runner():
    parser = OptionParser()
    parser.add_option(
        "-o", "--out-file", dest="output", help="write report to FILE", metavar="FILE"
    )
    parser.add_option(
        "-a", "--author", dest="author", help="filter by author name", metavar="AUTHOR"
    )
    parser.add_option(
        "-e", "--email", dest="email", help="filter by author email", metavar="EMAIL"
    )
    (options, args) = parser.parse_args()

    if options.output is not None:
        Logs(options.author, options.email, True, options.output).run()
    else:
        Logs(options.author, options.email).run()

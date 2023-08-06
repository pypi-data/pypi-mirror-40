import argparse

from logzero import logger

from pk.core.log import init
from pk.core.dhis import DhisAccess

"""
post-css
~~~~~~~~~~~~~~~~~
POST a CSS stylesheet to a server
"""


def parse_args():
    parser = argparse.ArgumentParser(usage='%(prog)s [-h] [-s] -c [-u] [-p] [-d]',
                                     description="Post CSS stylesheet to a server")
    parser.add_argument('-s', dest='server', action='store', help="DHIS2 server URL, e.g. 'play.dhis2.org/demo'")
    parser.add_argument('-c', dest='css', action='store', required=True, help="CSS file")
    parser.add_argument('-u', dest='username', action='store', help='DHIS2 username, e.g. -u=admin')
    parser.add_argument('-p', dest='password', action='store', help='DHIS2 password, e.g. -p=district')
    parser.add_argument('-d', dest='debug', action='store_true', default=False,
                        help="Debug flag - writes more info to log file, e.g. -d")
    return parser.parse_args()


def main():
    args = parse_args()
    init(args.debug)
    dhis = DhisAccess(server=args.server, username=args.username, password=args.password, api_version=None)

    dhis.post_file(endpoint='files/style', filename=args.css, content_type='text/css')
    logger.info("{} CSS posted to {}. Clear your caches.".format(args.css, dhis.api_url))


if __name__ == "__main__":
    main()

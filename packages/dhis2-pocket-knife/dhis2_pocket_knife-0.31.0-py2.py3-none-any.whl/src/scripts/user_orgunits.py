#!/usr/bin/env python

"""
user-orgunits
~~~~~~~~~~~~~~~~~
Checks each user assigned to an organisation unit if he/she is assigned to both organisation unit
and its sub-organisation units and prints them with their UID.
"""

import argparse
import unicodecsv as csv
import sys

from pk.core.dhis import DhisAccess
from pk.core.static import valid_uid
from pk.core.logger import *


def parse_args():

    parser = argparse.ArgumentParser(
        description="Create CSV of users of an orgunit who also have sub-orgunits assigned")
    parser.add_argument('-s', dest='server', action='store',
                        help="DHIS2 server URL without /api/ e.g. -s=play.dhis2.org/demo")
    parser.add_argument('-o', dest='orgunit', action='store', help="Top-level orgunit UID to check its users",
                        required=True)
    parser.add_argument('-u', dest='username', action='store', help="DHIS2 username")
    parser.add_argument('-p', dest='password', action='store', help="DHIS2 password")
    parser.add_argument('-v', dest='api_version', action='store', required=False, type=int,
                        help='DHIS2 API version e.g. -v=24')
    parser.add_argument('-d', dest='debug', action='store_true', default=False, required=False,
                        help="Writes more info in log file")

    return parser.parse_args()


def main():
    args = parse_args()
    init_logger(args.debug)
    log_start_info(__file__)

    dhis = DhisAccess(server=args.server, username=args.username, password=args.password, api_version=args.api_version)

    if not valid_uid(args.orgunit):
        log_info(u"{} is not a valid DHIS2 UID".format(args.orgunit))
        sys.exit()

    orgunit_root_uid = args.orgunit

    # get root orgunit
    endpoint1 = 'organisationUnits/{}'.format(orgunit_root_uid)
    params1 = {
        'fields': 'id,name,path,users'
    }
    root_orgunit = dhis.get(endpoint=endpoint1, params=params1)

    # get path of root orgunit
    path = root_orgunit['path']

    # get all descendant orgunit UIDs (excluding self) via 'path' field filter
    endpoint2 = 'organisationUnits'
    params2 = {
        'filter': [
            'path:^like:' + path,
            'id:!eq:' + orgunit_root_uid
        ],
        'fields': 'id',
        'paging': False
    }
    resp2 = dhis.get(endpoint=endpoint2, params=params2)

    no_of_users = len(root_orgunit['users'])

    # put the response ids into a list
    sub_uids = list(ou['id'] for ou in resp2['organisationUnits'])

    log_info(u"Checking users against Sub-OrgUnit assignments of Parent-OrgUnit {}".format(root_orgunit['name']))

    # Python2 & 3 compatibility
    try:
        xrange
    except NameError:
        xrange = range

    # check each user of root orgunit
    # log user if: [has more than 1 orgunit associated] AND [any other user orgunit is a sub-orgunit of root orgunit]
    users_export = []
    counter = 0
    for user in root_orgunit['users']:
        counter += 1
        user_uid = user['id']

        endpoint3 = 'users/{}'.format(user_uid)
        params3 = {
            'fields': 'id,name,organisationUnits,lastUpdated'
        }
        user = dhis.get(endpoint=endpoint3, params=params3)

        print("({}/{}) {} ...".format(str(counter), str(no_of_users), user_uid))

        user_orgunits = user['organisationUnits']
        if len(user_orgunits) > 1:
            # find conflicting sub-orgunits and only proceed if a conflict has not been found yet, otherwise break
            for x in xrange(len(user_orgunits)):
                user_orgunit_uid = user_orgunits[x]['id']
                if user_orgunit_uid != orgunit_root_uid and user_orgunit_uid in sub_uids:
                    users_export.append(user)
                    log_info(u"Conflicting user found: {} - UID: {}".format(user['name'], user_uid))
                    break

    # write conflicting users to CSV file
    if users_export:
        # remove orgunits for export
        for u in xrange(len(users_export)):
            users_export[u].pop('organisationUnits')

        file_name = 'user-orgunits_{}-{}_{}.csv'.format(root_orgunit['name'], root_orgunit['id'], dhis.file_timestamp)
        with open(file_name, 'w') as csv_file:
            # use the keys of first user as csv headers
            fieldnames = list(users_export[0].keys())

            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(users_export)

        log_info(u"+++ Success! Exported {} users to {}".format(len(users_export), file_name))
    else:
        log_info(u"+++ No conflicts found.")

if __name__ == "__main__":
    main()

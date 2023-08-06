#!/usr/bin/env python

from __future__ import print_function

"""
share-objects
~~~~~~~~~~~~~~~~~
Assigns sharing to shareable DHIS2 objects like userGroups and publicAccess by calling the /api/sharing endpoint.
"""

import argparse
import json
import sys

from six import iteritems

from pk.core.dhis import DhisAccess
from pk.core.logger import *

public_access = {
    'none': '--------',
    'readonly': 'r-------',
    'readwrite': 'rw------'
}


class Sharer(DhisAccess):

    def get_usergroup_uids(self, filter_list, access, delimiter):
        params = {
            'fields': 'id,name',
            'paging': False,
            'filter': filter_list
        }
        if delimiter == '||':
            root_junction = 'OR'
            params['rootJunction'] = root_junction
        else:
            root_junction = 'AND'

        endpoint = 'userGroups'
        print(("+++ GET {} with filter [rootJunction: {}] {} ({})".format(endpoint, root_junction, filter_list, access)))
        response = self.get(endpoint=endpoint, file_type='json', params=params)

        if len(response['userGroups']) > 0:
            # zip it into a dict { id: name, id:name }
            ugmap = {ug['id']: ug['name'] for ug in response['userGroups']}
            for (key, value) in iteritems(ugmap):
                log_info(u"{} - {}".format(key, value))
            return ugmap.keys()
        else:
            log_info(u"+++ No userGroup(s) found. Check your filter / DHIS2")
            sys.exit()

    def get_objects(self, objects, objects_filter, delimiter):

        params = {
            'fields': 'id,name,code,publicAccess,userGroupAccesses',
            'filter': objects_filter,
            'paging': False
        }

        if delimiter == '||':
            params['rootJunction'] = 'OR'
            print_junction = "+++ GET {} with filters [rootJunction: OR] {}"
        elif len(objects_filter) > 1:
            print_junction = "+++ GET {} with filters [rootJunction: AND] {}"
        else:
            print_junction = "+++ GET {} with filter {}"

        print(print_junction.format(objects, objects_filter))
        response = self.get(endpoint=objects, file_type='json', params=params)

        if response:
            if len(response[objects]) > 0:
                return response
        log_info(u'+++ No objects found. Wrong filter?')
        log_debug(u'objects: {}'.format(objects.encode('utf-8')))
        sys.exit()

    def share_object(self, sharing_object):
        params = {'type': sharing_object.object_type, 'id': sharing_object.uid}
        data = sharing_object.to_json()
        self.post(endpoint="sharing", params=params, payload=data)

    def get_object_type(self, argument):
        return super(Sharer, self).get_shareable_object_type(argument)


class SharingDefinition(object):

    def __init__(self, uid, object_type, public_access, usergroup_accesses=None):
        self.uid = uid
        self.object_type = object_type
        self.public_access = public_access
        self.usergroup_accesses = usergroup_accesses
        self.external_access = False
        self.user = {}

    def __eq__(self, other):
        return (self.uid == other.uid and
                self.object_type == other.object_type and
                self.public_access == other.public_access and
                self.usergroup_accesses == other.usergroup_accesses)

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.uid, self.object_type, self.public_access, self.usergroup_accesses))

    def __repr__(self):
        return u"{} {} {} {}".format(self.object_type, self.uid, self.public_access, self.usergroup_accesses)

    def to_json(self):
        return {
            'object': {
                'publicAccess': self.public_access,
                'externalAccess': self.external_access,
                'user': self.user,
                'userGroupAccesses': [x.to_json() for x in self.usergroup_accesses]
            }
        }


class UserGroupAccess(object):

    def __init__(self, uid, access):
        self.uid = uid
        self.access = access

    def __eq__(self, other):
        return self.uid == other.uid and self.access == other.access

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.uid, self.access))

    def __repr__(self):
        return json.dumps(self.to_json())

    def to_json(self):
        return {"id": self.uid, "access": self.access}


def parse_args():
    parser = argparse.ArgumentParser(usage='%(prog)s [-h] [-s] -t -f [-w] [-r] -a [-k] [-v] [-u] [-p] [-d]',
                                     description="PURPOSE: Share DHIS2 objects (dataElements, programs, ...) "
                                                 "with userGroups")
    parser.add_argument('-s', dest='server', action='store', help="DHIS2 server URL, e.g. 'play.dhis2.org/demo'")
    parser.add_argument('-t', dest='object_type', action='store', required=True,
                        help="DHIS2 object type to apply sharing, e.g. -t=sqlViews")
    parser.add_argument('-f', dest='filter', action='store', required=True,
                        help="Filter on objects with DHIS2 field filter (add "
                             "multiple filters with '&&') e.g. -f='name:like:ABC'")
    parser.add_argument('-w', dest='usergroup_readwrite', action='store', required=False,
                        help="UserGroup filter for Read-Write access (add "
                             "multiple filters with '&&') e.g. -w='name:$ilike:aUserGroup7&&id:!eq:aBc123XyZ0u'")
    parser.add_argument('-r', dest='usergroup_readonly', action='store', required=False,
                        help="UserGroup filter for Read-Only access, (add "
                             "multiple filters with '&&') e.g. -r='id:eq:aBc123XyZ0u'")
    parser.add_argument('-a', dest='publicaccess', action='store', required=True, choices=public_access.keys(),
                        help="publicAccess (with login), e.g. -a=readwrite")
    parser.add_argument('-k', dest='keep', action='store_true', required=False,
                        help="keep current sharing & only replace as specified")
    parser.add_argument('-v', dest='api_version', action='store', required=False, type=int,
                        help='DHIS2 API version e.g. -v=24')
    parser.add_argument('-u', dest='username', action='store', help='DHIS2 username, e.g. -u=admin')
    parser.add_argument('-p', dest='password', action='store', help='DHIS2 password, e.g. -p=district')
    parser.add_argument('-d', dest='debug', action='store_true', default=False, required=False,
                        help="Debug flag - writes more info to log file, e.g. -d")
    return parser.parse_args()


def filter_delimiter(argument, dhis_version):
    if '||' in argument:
        if dhis_version < 25:
            sys.exit("rootJunction 'OR' is only supported 2.25 onwards. Nothing shared.")
        return '||'
    else:
        return '&&'


def main():
    args = parse_args()
    init_logger(args.debug)
    log_start_info(__file__)
    dhis = Sharer(server=args.server, username=args.username, password=args.password, api_version=args.api_version)

    dhis_version = dhis.set_dhis_version()

    # get the real valid object type name
    object_type = dhis.get_object_type(args.object_type)

    user_group_accesses = set()
    if args.usergroup_readwrite:
        delimiter = filter_delimiter(args.usergroup_readwrite, dhis_version)
        # split filter of arguments into list
        rw_ug_filter_list = args.usergroup_readwrite.split(delimiter)
        # get UIDs of usergroups with RW access
        readwrite_usergroup_uids = dhis.get_usergroup_uids(rw_ug_filter_list, 'readwrite', delimiter)
        for ug in readwrite_usergroup_uids:
            user_group_accesses.add(UserGroupAccess(uid=ug, access=public_access['readwrite']))

    if args.usergroup_readonly:
        delimiter = filter_delimiter(args.usergroup_readonly, dhis_version)
        ro_ug_filter_list = args.usergroup_readonly.split(delimiter)
        # get UID(s) of usergroups with RO access
        readonly_usergroup_uids = dhis.get_usergroup_uids(ro_ug_filter_list, 'readonly', delimiter)
        for ug in readonly_usergroup_uids:
            user_group_accesses.add(UserGroupAccess(uid=ug, access=public_access['readonly']))

    # split arguments for multiple filters for to-be-shared objects
    delimiter = filter_delimiter(args.filter, dhis_version)
    object_filter_list = args.filter.split(delimiter)

    # pull objects for which to apply sharing
    data = dhis.get_objects(object_type, object_filter_list, delimiter)

    no_of_obj = len(data[object_type])
    for i, obj in enumerate(data[object_type], 1):

        skip = False
        # strip name to match API (e.g. dataElements -> dataElement)
        if object_type == 'categories':
            object_type_singular = 'category'
        else:
            object_type_singular = object_type[:-1]

        # create a ObjectSharing based on command-line arguments
        submitted = SharingDefinition(uid=obj['id'],
                                      object_type=object_type_singular,
                                      public_access=public_access[args.publicaccess],
                                      usergroup_accesses=list(user_group_accesses))
        if args.keep:
            # create a ObjectSharing based on what is already on the server
            existing = SharingDefinition(uid=obj['id'],
                                         object_type=object_type_singular,
                                         public_access=obj['publicAccess'])
            if obj.get('userGroupAccesses'):
                existing.usergroup_accesses = [UserGroupAccess(uid=x['id'], access=x['access']) for x in obj['userGroupAccesses']]

            if existing == submitted:
                skip = True

        if not skip:
            # apply sharing
            dhis.share_object(submitted)

            try:
                log_info(u"({}/{}) [OK] {} {}".format(i, no_of_obj, obj['id'], obj['name'].encode('utf-8')))
            except (UnicodeEncodeError, UnicodeDecodeError):
                try:
                    log_info(u"({}/{}) [OK] {} {}".format(i, no_of_obj, obj['id'], obj['code']))
                except (UnicodeEncodeError, UnicodeDecodeError, KeyError):
                    log_info(u"({}/{}) [OK] {}".format(i, no_of_obj, obj['id']))

        sys.exit()


if __name__ == "__main__":
    main()

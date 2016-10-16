#!/usr/bin/env python

import argparse
import json
import sys

from profile_desc import PublicProfile, CommunityProfile, MemberProfile, AdminProfile

from elasticsearch_dsl.connections import connections

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', default='-', type=argparse.FileType('r', encoding='utf-8'))
    parser.add_argument('profile_level', default='public', help="Profile acces level: public | community | member | admin")
    parser.add_argument('--es-instance', default='localhost', help="ElasticSearch instance to load into")

    args = parser.parse_args()

    connections.create_connection(hosts=[args.es_instance])

    json_data = json.load(args.infile) 
    total = len(json_data)

    line_template = '%%%dd/%d\r' % (len(str(total)), total)

    if args.profile_level == "public":
        profile_class = PublicProfile
    elif args.profile_level == "community":
        profile_class = CommunityProfile
    elif args.profile_level == "member":
        profile_class = MemberProfile
    elif args.profile_level == "admin":
        profile_class = AdminProfile
    else:
        print("Invalid profile level: {}".format(args.profile_level))
        return

    for i, profile in enumerate(json_data):
        p = profile_class(**profile)
        p.save()
        print(line_template % (i+1), end='')
    
    print("\nDone! :)")

if __name__ == "__main__":
    main()

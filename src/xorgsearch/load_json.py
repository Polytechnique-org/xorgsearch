#!/usr/bin/env python

import argparse
import json
import sys

from profile import Profile

from elasticsearch_dsl.connections import connections

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', default='-', type=argparse.FileType('r', encoding='utf-8'))
    parser.add_argument('--es-instance', default='localhost', help="ElasticSearch instance to load into")

    args = parser.parse_args()

    connections.create_connection(hosts=[args.es_instance])

    json_data = json.load(args.infile) 
    total = len(json_data)

    for (i,profile) in enumerate(json_data):
        p = Profile(**profile)
        p.save()
        print("{}/{}\r".format(i,total), end='')
    
    print("Done! :)")

if __name__ == "__main__":
    main()
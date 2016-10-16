#!/usr/bin/env python

import argparse

from elasticsearch_dsl import Q
from elasticsearch_dsl.connections import connections

from profiles import ProfileSearch

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('search_str', help="search string")
    parser.add_argument('--es-instance', default='localhost', help="ElasticSearch instance to load into")

    args = parser.parse_args()

    connections.create_connection(hosts=[args.es_instance])

    tt = TermTree()

    for s in args.search_str.split():
        if ':' in s:
            [prefix, value] = s.split(':', 2)
            tt.add_term(Term(value), filter=prefix)
        else:
            tt.add_term(Term(s))

    qs = tt.search()

    res = qs.execute()

    print("Search \"{}\" matched {} entries:\n".format(args.search_str, res.hits.total))

    for hit in res:
        print("{} {} (score: {})".format(
            hit.fullname,
            '♂' if hit.sex == "male" else '♀',
            hit.meta.score
        ))
        print("    {} {}".format(hit.section, hit.promo))
        print()

    for facet in res.facets:
        print("filter {}: [ ".format(facet), end='')
        for (val, count, selected) in res.facets[facet]:
            print("{}: {} | ".format(val, count), end='')
        print("]")
        

if __name__ == "__main__":
    main()

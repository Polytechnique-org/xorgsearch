import json

from flask import Flask, request
from flask_restful import Resource, Api, abort

from profile_search import TermTree, Term

from elasticsearch_dsl.connections import connections

app = Flask(__name__)
api = Api(app)

def term_tree_from_json(json_data):
    tt = TermTree()
    for filter, items in json_data['search'].items():
        for item in items:
            tt.add_term(
                Term(item["v"], item["match"], item.get("required", False)),
                filter=filter
            )
    return tt

def response_to_json(response):
    ret = {}
    ret["meta"] = { "hits": response.hits.total }
    ret["facets"] = {
        facet_name: {
            val: count for (val, count, _) in response.facets[facet_name]
        } for facet_name in response.facets
    }
    ret["results"] = [
        {
            "id": str(hit.pid),
            "score": hit.meta.score,
            "data": {
                "hrpid": hit.hrpid,
                "promo": hit.promo,
                "fullname": hit.fullname
            }
        } for hit in response
    ]
    return ret

class Search(Resource):
    def post(self):
        tt = term_tree_from_json(request.get_json())
        qs = tt.search()
        return response_to_json(qs.execute())

api.add_resource(Search, '/search')

if __name__ == '__main__':
    connections.create_connection(hosts=['localhost'])
    app.run(debug=True)

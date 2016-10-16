import json

import jwt

from flask import Flask, request
from flask_restful import Resource, Api, abort

from termtree import TermTree, Term
from profile_desc import PublicProfileSearch, CommunityProfileSearch, MemberProfileSearch, AdminProfileSearch

from elasticsearch_dsl.connections import connections

app = Flask(__name__)
api = Api(app)

JWT_KEY = None
JWT_ALGO = "none"

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

def get_access_level(req):
    auth_header = req.headers.get('Authorization')
    if auth_header is None:
        abort(401)
    _, claims = jwt.verify_jwt(auth_header, JWT_KEY, [JWT_ALGO])
    perms = claims["x-perms"]
    if "admin" in perms:
        return AdminProfileSearch
    elif "directory_private" in perms:
        return MemberProfileSearch
    elif "directory_ax" in perms:
        return CommunityProfileSearch
    else:
        return PublicProfileSearch

class Search(Resource):
    def post(self):
        tt = term_tree_from_json(request.get_json())
        search_class = get_access_level(request)
        qs = tt.search(search_class)
        return response_to_json(qs.execute())

api.add_resource(Search, '/search')

if __name__ == '__main__':
    connections.create_connection(hosts=['localhost'])
    app.run(debug=True)

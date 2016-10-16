from elasticsearch_dsl import Q

class InvalidMatchKind(Exception):
    def __init__(self, kind):
        self.kind = kind
        self.message = "Invalid match kind: {}".format(kind)

class Term:
    def __init__(self, value, matchkind="fuzzy", required=False):
        if not (matchkind == "exact" or matchkind == "fuzzy"):
            raise InvalidMatchKind(self.matchkind)
        self.value = value
        self.required = required
        self.matchkind = matchkind

class TermTree:
    def __init__(self):
        self.terms = {}

    def add_term(self, term, filter="raw"):
        if filter not in self.terms:
            self.terms[filter] = [term]
        else:
            self.terms[filter].append(term)

    def search(self, cls):
        return cls(self)

    def as_query(self, known_fields=[]):
        q = None
        for filter, terms in self.terms.items():
            # ignore unkown filters:
            if not (filter in known_fields or filter == "raw"):
                continue
            q_unreq = None
            q_req = None
            if filter == "raw":
                fields = [ f for f in known_fields if f not in self.terms ]
            else:
                fields = [ filter ]
            for t in terms:
                if t.matchkind == "exact":
                    t_q = Q(
                        "multi_match",
                        query=t.value,
                        fields=fields
                    )
                else: # fuzzy
                    t_q = None
                    for f in fields:
                        t_q = q_or(
                            t_q,
                            Q({ "fuzzy" : { f: t.value }})
                        )
                if t.required:
                    q_req = q_and(q_req, t_q)
                else:
                    q_unreq = q_or(q_unreq, t_q)
            q = q_and(q, q_and(q_unreq, q_req))
        return q

def q_or(q_a, q_b):
    if q_a is None:
        return q_b
    elif q_b is None:
        return q_a
    else:
        return q_a | q_b

def q_and(q_a, q_b):
    if q_a is None:
        return q_b
    elif q_b is None:
        return q_a
    else:
        return q_a & q_b

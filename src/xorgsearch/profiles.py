from elasticsearch_dsl import DocType, String, Integer, FacetedSearch, TermsFacet, Q

class Profile(DocType):
    pid = Integer()
    hrpid = String()
    sex = String()
    resume = String()
    freetext = String()
    section = String()
    fullname = String()
    promo = String()

    class Meta:
        index = "profiles"

class ProfileSearch(FacetedSearch):
    doc_types = [Profile,]
    fields = ['fullname', 'promo', 'section']
    facets = {
        'promo': TermsFacet(field='promo'),
        'section': TermsFacet(field='section'),
        'sex': TermsFacet(field='sex')
    }

    def query(self, search, query):
        (raw_terms, matched) = split_terms(query, self.fields)
        unmatched_fields = [ f for f in self.fields if f not in matched ]

        for term in raw_terms:
            q = None
            for field in unmatched_fields:
                if q is None:
                    q = Q({"fuzzy": { field: term }})
                else:
                    q = q | Q({"fuzzy": { field: term}})
            search = search.query(q)
        for (field, values) in matched.items():
            q = None
            for v in values:
                if q is None:
                    q = Q({"fuzzy": { field: v }})
                else:
                    q = q | Q({"fuzzy": { field: v }})
            search = search.query(q)
        return search

def split_terms(search_string, fields):
    matched = {}
    raw_terms = []
    for term in search_string.split():
        if ':' in term:
            [name, value] = term.split(':', maxsplit=2)
            if name in fields:
                if name not in matched:
                    matched[name] = [value]
                else:
                    matched[name].append(value)
            else:
                raw_terms.append(term)
        else:
            raw_terms.append(term)
    return (raw_terms, matched)

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
        for term in query.split():
            q = None
            for field in self.fields:
                if q is None:
                    q = Q({"fuzzy": { field: term }})
                else:
                    q = q | Q({"fuzzy": { field: term}})
            search = search.query(q)
        return search

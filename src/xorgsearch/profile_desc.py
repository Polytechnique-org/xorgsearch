from elasticsearch_dsl import DocType, String, Integer, FacetedSearch, TermsFacet, Q

#
# Public Profile
#
# Data available publicly to non-logged clients
#

class PublicProfile(DocType):
    pid = Integer()
    hrpid = String()
    sex = String()
    fullname = String()
    promo = String()

    class Meta:
        index = "public_profiles"

class PublicProfileSearch(FacetedSearch):
    doc_types = [PublicProfile,]
    fields = ['fullname', 'promo', 'sex']
    facets = {
        'promo': TermsFacet(field='promo'),
        'section': TermsFacet(field='section'),
        'sex': TermsFacet(field='sex')
    }

    def query(self, search, termtree):
        return search.query(termtree.as_query(self.fields))

#
# Community Profile
#
# Data available to community-related but non-member clients
#

class CommunityProfile(PublicProfile):
    resume = String()
    freetext = String()
    section = String()

    class Meta:
        index = "community_profiles"

class CommunityProfileSearch(PublicProfileSearch):
    doc_types = [CommunityProfile,]

#
# Member Profile
#
# Data available only to other members
#

class MemberProfile(CommunityProfile):

    class Meta:
        index = "member_profiles"

class MemberProfileSearch(CommunityProfileSearch):
    doc_types = [MemberProfile,]

#
# Admin Profile
#
# Data available to administrators
#

class AdminProfile(MemberProfile):

    class Meta:
        index = "admin_profiles"

class AdminProfileSearch(MemberProfileSearch):
    doc_types = [AdminProfile,]


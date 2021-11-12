import os
from typing import Collection, Literal

from SPARQLWrapper import JSON, POST, SPARQLWrapper2

OND_NS = "https://data.meemoo.be/terms/ond/"


def read_query(file_path):
    # check if file is present
    if os.path.isfile(file_path):
        # open text file in read mode
        text_file = open(file_path, "r")

        # read whole file to a string
        data = text_file.read()

        # close file
        text_file.close()
        return data
    return None


class Suggest:
    """A simple api for vocbench data"""

    def __init__(self, endpoint: Literal, user: Literal, password: Literal):
        self.sparql = SPARQLWrapper2(endpoint)
        self.sparql.setMethod(POST)
        self.sparql.setCredentials(user, password)
        self.sparql.setReturnFormat(JSON)

        query_dir = os.getcwd() + "/suggest/queries/"
        self.GET_LIST_QUERY = read_query(query_dir + "get_conceptscheme.sparql")
        self.GET_COLLECTION_QUERY = read_query(query_dir + "get_collection.sparql")
        self.GET_CHILDREN_QUERY = read_query(query_dir + "get_narrower.sparql")
        self.SUGGEST_BY_LABEL_QUERY = read_query(query_dir + "suggest_by_label.sparql")
        self.SUGGEST_BY_ID_QUERY = read_query(query_dir + "suggest_by_id.sparql")

    def __exec_query(self, query: Literal, **kwargs):
        formatted = query.format(**kwargs)
        self.sparql.setQuery(formatted)
        for result in self.sparql.query().bindings:
            yield {
                "id": result["id"].value,
                "label": result["label"].value,
                "definition": result["definition"].value,
            }

    def get_list(self, scheme: Literal):
        """Get a thesaurus concepts by scheme id."""

        for res in self.__exec_query(self.GET_LIST_QUERY, scheme=scheme):
            yield res

    def get_collection(self, collection: Literal):
        """Get a collection members by collection id."""

        for res in self.__exec_query(self.GET_COLLECTION_QUERY, collection=collection):
            yield res

    def get_children(self, concept: Literal):
        """Get the children of a concept."""

        for res in self.__exec_query(self.GET_CHILDREN_QUERY, concept=concept):
            yield res

    def get_vakken(self):
        """Get list 'vakken'."""

        for res in self.get_list(OND_NS + "vak"):
            yield res

    def get_themas(self):
        """Get list 'themas'."""

        for res in self.get_list(OND_NS + "themas"):
            yield res

    def get_graden(self):
        """Get list 'onderwijsgraden'."""

        for res in self.get_collection(OND_NS + "graad"):
            yield res

    def get_niveaus(self):
        """Get list 'onderwijsniveaus'."""

        for res in self.get_collection(OND_NS + "niveau"):
            yield res

    def suggest(self, thema: Literal, graad: Literal):
        """Suggest 'vakken' based on the identifiers of 'onderwijsgraad' and 'thema'."""

        for res in self.__exec_query(
            self.SUGGEST_BY_ID_QUERY, thema=thema, graad=graad
        ):
            yield res

    def suggest_by_label(self, thema: Literal, graad: Literal):
        """Suggest 'vakken' based on 'onderwijsgraad' and 'thema'."""

        for res in self.__exec_query(
            self.SUGGEST_BY_LABEL_QUERY, thema=thema, graad=graad
        ):
            yield res

import os
from typing import List

from SPARQLWrapper import JSON, POST, SPARQLWrapper2

OND_NS = "https://data.meemoo.be/terms/ond/"

def join_ids(ids):
    return ", ".join("<" + str(id) + ">" for id in ids)

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

    def __init__(self, endpoint: str, user: str, password: str):
        self.sparql = SPARQLWrapper2(endpoint)
        self.sparql.setMethod(POST)
        self.sparql.setCredentials(user, password)
        self.sparql.setReturnFormat(JSON)

        query_dir = os.getcwd() + "/suggest/queries/"
        self.GET_LIST_QUERY = read_query(query_dir + "get_conceptscheme.sparql")
        self.GET_COLLECTION_QUERY = read_query(query_dir + "get_collection.sparql")
        self.GET_CHILDREN_QUERY = read_query(query_dir + "get_narrower.sparql")
        self.SUGGEST_BY_LABELS_QUERY = read_query(
            query_dir + "suggest_by_labels.sparql"
        )
        self.SUGGEST_BY_IDS_QUERY = read_query(query_dir + "suggest.sparql")
        self.GET_CONCEPT_BY_ID_QUERY = read_query(query_dir + "get_concept.sparql")
        self.GET_CANDIDATES_QUERY = read_query(query_dir + "candidates.sparql")
        self.GET_RELATED_VAK_QUERY = read_query(query_dir + "get_related_vak.sparql")

    def __exec_query(self, query: str, **kwargs):
        formatted = query.format(**kwargs)
        self.sparql.setQuery(formatted)
        for result in self.sparql.query().bindings:
            yield {
                "id": result["id"].value,
                "label": result["label"].value,
                "definition": result["definition"].value,
            }

    def get_list(self, scheme: str):
        """Get thesaurus concepts by scheme id."""

        for res in self.__exec_query(self.GET_LIST_QUERY, scheme=scheme):
            yield res

    def get_concept(self, concept: str):
        """Get thesaurus concept by id."""

        for res in self.__exec_query(self.GET_CONCEPT_BY_ID_QUERY, concept=concept):
            yield res

    def get_collection(self, collection: str):
        """Get a collection members by collection id."""

        for res in self.__exec_query(self.GET_COLLECTION_QUERY, collection=collection):
            yield res

    def get_children(self, concept: str):
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

    def suggest(self, thema: List[str], graad: List[str]):
        """Suggest 'vakken' based on the identifiers of 'onderwijsgraad' and 'thema'."""

        themas = join_ids(thema)
        graden = join_ids(graad)

        for res in self.__exec_query(
            self.SUGGEST_BY_IDS_QUERY, themas=themas, graden=graden
        ):
            yield res

    def suggest_by_label(self, thema: List[str], graad: List[str]):
        """Suggest 'vakken' based on 'onderwijsgraad' and 'thema'."""

        themas = ", ".join('"' + str(t) + '"' for t in thema)
        graden = ", ".join('"' + str(g) + '"' for g in graad)

        for res in self.__exec_query(
            self.SUGGEST_BY_LABELS_QUERY, themas=themas, graden=graden
        ):
            yield res

    def get_candidates(self, thema: List[str], graad: List[str]):
        """Get all possible 'vakken' based on the identifiers of 'onderwijsgraad' and 'thema'."""

        themas = join_ids(thema)
        graden = join_ids(graad)

        for res in self.__exec_query(
            self.GET_CANDIDATES_QUERY, themas=themas, graden=graden
        ):
            yield res

    def get_related_vak(self, concept: List[str]):
        """Get related vak by concept ids."""

        concepts = join_ids(concept)

        for res in self.__exec_query(self.GET_RELATED_VAK_QUERY, concepts=concepts):
            yield res
import os
from typing import Literal

from SPARQLWrapper import JSON, POST, SPARQLWrapper2


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
        self.VAKKEN_QUERY = read_query(query_dir + "vakken.sparql")
        self.THEMAS_QUERY = read_query(query_dir + "themas.sparql")
        self.GRADEN_QUERY = read_query(query_dir + "onderwijsgraden.sparql")
        self.SUGGEST_QUERY = read_query(query_dir + "suggest.sparql")

    def __exec_query(self, query: Literal, **kwargs):
        formatted = query.format(**kwargs)
        self.sparql.setQuery(formatted)
        for result in self.sparql.query().bindings:
            yield {"id": result["id"].value, "label": result["label"].value}

    def get_vakken(self):
        """Get list 'vakken'."""

        for res in self.__exec_query(self.VAKKEN_QUERY):
            yield res

    def get_themas(self):
        """Get list 'themas'."""

        for res in self.__exec_query(self.THEMAS_QUERY):
            yield res

    def get_graden(self):
        """Get list 'onderwijsgraden'."""

        for res in self.__exec_query(self.GRADEN_QUERY):
            yield res

    def suggest(self, thema: Literal, graad: Literal):
        """Suggest 'vakken' based on 'onderwijsgraad' and 'thema'."""

        for res in self.__exec_query(self.SUGGEST_QUERY, thema=thema, graad=graad):
            yield res

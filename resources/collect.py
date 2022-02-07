#!/usr/bin/env python
# coding: utf-8

import collections
from numpy import NaN
import pandas as pd  # for handling csv and csv contents
from rdflib import Graph, Literal, RDF, URIRef, Namespace  # basic RDF handling
from rdflib.namespace import SKOS  # most common namespaces
from rdflib.term import BNode
import urllib.parse  # for parsing strings to URI's
import argparse

def to_key(label):
    split = label.split(" (")
    if len(split) > 1:
        label = split[0]

    label = label.replace(" ", "-").lower()

    return urllib.parse.quote(label, safe='')


def main(args):
    df = pd.read_csv(args.csv_file)

    g = Graph()
    ond = Namespace(args.ns)
    g.bind("skos", SKOS)

    first = BNode()  # id of collection
    rest = BNode()

    collection = URIRef(args.collection)

    if args.ordered:
        g.add((collection, RDF.type, SKOS.OrderedCollection))
    g.add((collection, RDF.type, SKOS.Collection))

    if args.label is not None:
        g.add((collection, SKOS.prefLabel, Literal(args.label, args.lang)))

    if args.ordered:
        g.add((collection, SKOS.memberList, first))

    labels = df[args.column].dropna().unique()
    for idx, label in enumerate(labels):

        key = to_key(label)
        res = URIRef(ond + key)
        g.add((collection, SKOS.member, res))

        if args.ordered:
            g.add((first, RDF.first, res))

            # if not last one
            if idx < len(labels) - 1:
                g.add((first, RDF.rest, rest))
            else:
                g.add((first, RDF.rest, RDF.nil))

        # reset
        first = rest
        rest = BNode()

    print(g.serialize(format="turtle"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_file", help="csv file to extract order from")
    parser.add_argument("column", help="column where ids are at")
    parser.add_argument("collection", help="URI of the collection")
    parser.add_argument(
        "-n",
        "--ns",
        required=False,
        help="Namespace",
        default="https://data.hetarchief.be/id/onderwijs/",
    )
    parser.add_argument(
        "-l",
        "--label",
        required=False,
        help="Label of the collection"
    )
    parser.add_argument(
        "-g",
        "--lang",
        required=False,
        help="Language of the label",
        default="nl",
    )
    parser.add_argument(
        "-o",
        "--ordered",
        action='store_true',
        required=False,
        help="Flag to indicate that collection should be ordered"
    )

    args = parser.parse_args()

    main(args)

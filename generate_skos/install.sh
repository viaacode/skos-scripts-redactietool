#!/usr/bin/env bash
wget https://github.com/tarql/tarql/releases/download/v1.2/tarql-1.2.tar.gz
tar -xf tarql-1.2.tar.gz
rm tarql-1.2.tar.gz

pip install pandas
pip install argparse

npm install -g ttl-merge
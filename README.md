# skos-scripts-redactietool
Scripts to 

- generate SKOS data from airtable CSV dumps
- get thesauri data

## Run the generation scripts (`./generate_skos`)

You need Python, Pypi and Nodejs.

1. Install the necessary dependencies by running `./install.sh`
2. Put the airtable CSV dumps in the `/data` folder
3. run the `./generate_skos.sh` script
4. find the results in the `/dist` folder
## Use the suggestion library (`./suggest_python`)

```
from suggest.Suggest import Suggest

SPARQL_ENDPOINT = "http://example.org/query"
USER = "user"
PASSWORD = "password"

suggest = Suggest(SPARQL_ENDPOINT, USER, PASSWORD)

for r in suggest.suggest('Recht', 'Secundair 2de graad'):
    print(r)

```




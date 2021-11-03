# skos-scripts-redactietool
Scripts to 
- generate SKOS data from airtable CSV dumps
- get thesauri data

## Run the generation scripts

1. Put the airtable CSV dumps in the `/data` folder
2. run the `./generate_skos.sh` script
3. find the results in the `/dist` folder
## Use the suggestion library

```
from suggest.Suggest import Suggest

SPARQL_ENDPOINT = "http://example.org/query"
USER = "user"
PASSWORD = "password"

suggest = Suggest(SPARQL_ENDPOINT, USER, PASSWORD)

for r in suggest.suggest('Recht', 'Secundair 2de graad'):
    print(r)

```




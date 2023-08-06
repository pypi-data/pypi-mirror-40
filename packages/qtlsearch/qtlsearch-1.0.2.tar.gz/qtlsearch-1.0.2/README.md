# QTLSearch

QTLSearch is piece of software to search for candidate causal genes in QTL studies by combining Gene Ontology annotations across many species, leveraging hierarchical orthologous groups.

First, a QTLSearch database is built (using ``qtlsearch-init``) which contains OMA HOGs annotated with GO / ChEBI terms from the latest releases. This is based on a QTL and mapping file which the user provides.

Then, the search is performed using ``qtlsearch-run``. A single database can be built for multiple QTL and then the search performed on these individually, enabling the use of a job scheduler. See examples [from the paper](https://bitbucket.org/alex-warwickvesztrocy/qtlsearch/downloads/qtlsearch-paper-examples.zip) to see how this was done using LSF.

# Installation
Requires Python >= 3.6. Download the package from the PyPI, resolving the dependencies by using ``pip install qtlsearch``.

Alternatively, clone this repository and install using `pip install .` or `python setup.py install`.
# qtlsearch-init -- Building a QTLSearch Database
Creates a database file ``qtlsearch.db`` in the current directory.
## Usage
Required arguments: ``--species``, ``--qtl``, ``--annotation_map``.

     usage: qtlsearch-init [-h] [--no_api_cache] [--api_cache_path API_CACHE_PATH]
                          [--api_endpoint API_ENDPOINT]
                          [--oma_version OMA_VERSION] [--data_path DATA_PATH]
                          --species SPECIES [SPECIES ...] --qtl QTL [QTL ...]
                          --annotation_map ANNOTATION_MAP [ANNOTATION_MAP ...]

## Arguments
### Quick reference table

| Flag                 | Default                | Description |
|:--------------------|:----------------------|:-----------|
| [``--species``](#markdown-header--species)        |                        | Species to build database for.
| [``--qtl``](#markdown-header--qtl)            |                        | List of paths to QTL files.
| [``--annotation_map``](#markdown-header--annotation_map) |                        | Mapping from trait in QTL file to annotation IDs (e.g., GO, ChEBI).
| [``--data_path``](#markdown-header--data_path)      | ``./data``             | Path to store downloaded data.
| [``--api_cache_path``](#markdown-header--api_cache_path) | ``./api_cache``        | Path to store OMA API cache.
| [``--no_api_cache``](#markdown-header--no_api_cache)   |                        | Boolean whether to cache API calls.
| [``--oma_version``](#markdown-header--oma_version)    | Current                | Enables use of old releases, through database download.


### Descriptions
#### `--species`
List of species to build the database for. Input as UniProt species codes (e.g., ``ARATH`` for *Arabidopsis thaliana*). These **must** be in the same order as the files in ``--qtl``.
#### ``--qtl``
List of paths to QTL file(s). These are tab-separated value files, format: ``<Trait, Chromosome, Start (Mbp), End (Mbp)>``. An optional first column can be added containing QTL IDs, otherwise the ID will correspond to the line number in the results. *_Note_*: the files **must not** have header names; the file names **must** be in the same order as the species in ``--species``.
#### ``--annotation_map``
Mapping from trait in QTL file to annotation IDs (e.g., GO, ChEBI). These are tab-separated value files, format: ``<Trait, GO Term, ChEBI Term>``. *_Note_*: the files **must** have header names "trait", "go", "chebi". The "chebi" column may be omitted if not required.
#### ``--data_path``
Path to store downloaded data. This is safe to share between multiple runs of ``qtlsearch-init``, unless the OMA database has been updated. Any updated species co-ordinates would then be incorrect.
#### ``--api_cache_path``
Path to store OMA API cache. The expectation is to use this to share the data between multiple runs of  ``qtlsearch-init``.
#### ``--no_api_cache``
Boolean whether to cache API calls. If set, this will not create the directory for persistent caching. If you don't expect to build multiple databases, it is best to disable this.
#### ``--oma_version``
Enables use of old releases. Set to string of release, e.g., ``All.Sep2014`` to use the species and HOGs from the September 2014 release of the OMA browser. This will download a *very large* database, instead of using the API.

## Example Database Build
Here, a smaller database shall be built using the QTL, associated with Fructose or Galactose abundance, from the Lisec _et al._ dataset (in _Arabidopsis thaliana_ [`ARATH`]) used in the paper.

Note: as we download (and cache) files from the UniProt-GOA and ChEBI databases, this will take quite some time. These files can be reused for further database builds, however.

Two files are required: one listing our trait to GO / ChEBI terms; the other listing the QTL.

### QTL Listing
The following table shows the QTL listing, this is then stored as a tab seperated value formatted file, **without** headers, as  [``qtl.tsv``](https://bitbucket.org/alex-warwickvesztrocy/qtlsearch/src/development/examples/qtls.tsv).

| QTL ID | Trait (Metabolite) | Chromosome | Start (Mbp) | End (Mbp) |
|:-------|:-------------------|:-----------|:------------|:----------|
| 12  | fructose  | 5 | 21.871688 | 24.169319 |
| 13  | fructose  | 5 | 21.871688 | 23.594912 |
| 63  | galactose | 5 |  8.947509 | 11.245141 |
| 111 | fructose  | 4 |  3.562645 |  7.833454 |
| 112 | fructose  | 5 | 16.414812 | 17.563628 |
 
### Trait Mapping
The following table shows the trait (metabolite) mapping used in the paper, this is then stored as a tab seperated value formatted file, **with** headers, as  [``mapping.tsv``](https://bitbucket.org/alex-warwickvesztrocy/qtlsearch/src/master/examples/mapping.tsv).

| trait | go | chebi |
|:-|:-|:-|
| fructose  | `GO:0046370` | `CHEBI:28757` |
| galactose | `GO:0046369` | `CHEBI:28260` |

### Build
The database can then be built as so:

``qtlsearch-init --species ARATH --qtl qtl.tsv --annotation_map mapping.tsv``

This will retrieve the *current* GO and ChEBI annotations which can be reused to build extra QTLSearch databases. The OMA API will be used to download the species protein co-ordinates required.

A `qtlsearch.db` file will be the output, placed in the current directory. This can then be used to search for your QTL in the next step.

# qtlsearch-run -- Running QTLSearch
It is necessary to build a QTLSearch database prior to running the search. This is explained [above](#qtlsearchinit__Building_a_QTLSearch_Database_9).

*Note*: a single database can be built for multiple QTL and then the search performed on these individually, enabling the use of a job scheduler. See examples [from the paper](https://bitbucket.org/alex-warwickvesztrocy/qtlsearch/downloads/qtlsearch-paper-examples.zip) to see how this was done using LSF.

## Usage
Required arguments: ``--species``, ``--qtl``, ``--db``.

    usage: qtlsearch-run [-h] [--data_path DATA_PATH] --species SPECIES
                     [SPECIES ...] --qtl QTL [QTL ...] --db DB [--with_p]
                     [--replicates REPLICATES] [--results RESULTS]

## Arguments
### Quick reference table

| Flag                 | Default                | Description |
|:--------------------|:----------------------|:-----------|
| [``--db``](#markdown-header--db) | | Path to database created with ``qtlsearch-init``.
| [``--species``](#markdown-header--species_1)        |                        | Species corresponding to QTL files.
| [``--qtl``](#markdown-header--qtl_1)            |                        | List of paths to QTL files.
| [``--results``](#markdown-header--results) | `./results.tsv` | Path to print the results table to.
| [``--with_p``](#markdown-header--with_p) | | Boolean whether to compute empirical _p_-values.
| [``--replicates``](#markdown-header--replicates) | 1,000 | Number of replicates for computing empirical distribution.
| [``--data_path``](#markdown-header--data_path_1)      | ``./data``             | Path where downloaded data was stored.
|

### Descriptions
#### ``--db``
Path to the database that is output from `qtlsearch-init`. If everything is completed in the same directory, without renaming the database file, this will be "`qtlsearch.db`".
#### ``--species``
List of species to build the database for. Input as UniProt species codes (e.g., ``ARATH`` for *Arabidopsis thaliana*). These **must** be in the same order as the files in ``--qtl``.
#### ``--qtl``
List of paths to QTL file(s). These are tab-separated value files, format: ``<Trait, Chromosome, Start (Mbp), End (Mbp)>``. An optional first column can be added containing QTL IDs, otherwise the ID will correspond to the line number in the results. *_Note_*: the files **must not** have header names; the file names **must** be in the same order as the species in ``--species``.
#### ``--results``
Path to print the results table to. Defaults as `./results.tsv`. This is in TSV format and includes a header of column names in the first row.
#### ``--with_p``
Boolean whether to compute the empirical _p_-values. This does take a long time, but the tool may still be useful without running this.
#### ``--replicates``
Number of replicates for computing the empirical distribution, in order to estimate the _p_-values.
#### ``--data_path``
Path to where the downloaded data was stored. This should be set to the same as it was for the call to `qtlsearch-init`.

## Example Run
Following on from the example database build, we can now run to search for potential causal genes in the QTL associated with Fructose / Galactose abundance.

``qtlsearch-run --species ARATH --qtl qtls.tsv --db qtlsearch.db``
    
This will, by default, create the output in a file `results.tsv` in the current directory.

# License
QTLSearch is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or     (at your option) any later version.

QTLSearch is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with QTLSearch.  If not, see <http://www.gnu.org/licenses/>.
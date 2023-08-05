FEC Data Reader
==========================

A quick way to retrieve FEC bulk data from https://www.fec.gov:

``` {.sourceCode .python}
>>> import fec_reader as fec
>>> reader = fec.DataReader(data_dir='/raw') # pick a target directory
>>> reader.get_pac_summary(2010, 2018)
```

Each reader function allows you to specify year ranges for the data downloads. For example, the code below
retrieves 3 data files:

`reader.get_pac_summary(2014, 2018)`

This is because the data in each file spans two calendar years.

This package is a demonstration of ETL skills for Alexus Wong. However, it is also important
that we as a society can efficiently consume the inordinate amount of information available
today. If we can process it, we can take steps in the right direction.

There is a 5 second delay between files to respect FEC.gov's bandwith.

Features
---------------

FEC Reader currently retrieves these data files:

-   PAC Summary - https://www.fec.gov/campaign-finance-data/pac-and-party-summary-file-description/ - `reader.get_pac_summary(start, end)`
-   Candidate Master - https://www.fec.gov/campaign-finance-data/candidate-master-file-description/ - `reader.get_candidate_master(start, end)`
-   Contributions from committees to candidates and independent expenditures - https://www.fec.gov/campaign-finance-data/contributions-committees-candidates-file-description/ - `reader.get_contributions_to_candidates(start, end)`

Installation
------------

To install FEC Reader, simply use pip:

``` {.sourceCode .bash}
$ pip install fec-reader
```

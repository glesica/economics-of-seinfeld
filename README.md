# The Economics of Seinfeld

This version of the site builds itself from a database dump of the original.

To build:

```
./build.py
make site
```

This will read in all of the data from the SQLite DB stored in `data/`. This, in
turn, is constructed from CSV files, but this process doesn't run on each build.

## Dependencies

The build requires Make, Python3, and Pandoc.

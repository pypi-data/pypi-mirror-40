# Polt

Live data visualisation via Matplotlib

[![pipeline status](https://gitlab.com/nobodyinperson/python3-polt/badges/master/pipeline.svg)](https://gitlab.com/nobodyinperson/python3-polt/commits/master)
[![coverage report](https://gitlab.com/nobodyinperson/python3-polt/badges/master/coverage.svg)](https://nobodyinperson.gitlab.io/python3-polt/coverage-report/)
[![documentation](https://img.shields.io/badge/docs-sphinx-brightgreen.svg)](https://nobodyinperson.gitlab.io/python3-polt/)
[![PyPI](https://badge.fury.io/py/polt.svg)](https://badge.fury.io/py/polt)

`polt` is a Python package for live data visualisation via
[Matplotlib](https://matplotlib.org/).

## What can `polt` do?

### Reading Numbers from STDIN

```bash
for i in `seq 1 100`;do echo $i;sleep $i;done | polt live
```

![polt-seq-stdin](https://gitlab.com/nobodyinperson/python3-polt/uploads/b9dffbde872a766c67813dc0257907a1/polt-stdin.png)

### Reading CSV from STDIN

```bash
echo "a,b,c\n1,2,3\n3,4,5\n7,5,8\n" | while read line;do echo $line;sleep 1;done | polt add-source -p CsvParser live
```

![polt-csv-stdin](https://gitlab.com/nobodyinperson/python3-polt/uploads/87522867f0abe42d686d0eb3ec46d139/Bildschirmfoto_2018-12-27_14-36-51.png)

### Reading Live Data from Logfiles

Imagine you have a file `data.txt` where another process constantly writes
lines of numbers into. `polt` can then use the common `tail` program to watch
that data:

```bash
polt add-source -c "tail -fn0 data.txt" live
```

### Further Possibilities

It is possible to split the data into subplots for

- quantity
- unit
- parser
- key

An [example from the documentation](https://nobodyinperson.gitlab.io/python3-polt/) of splitting by unit:

![polt split by units](https://gitlab.com/nobodyinperson/python3-polt/raw/fd2dacc263c96747ac364ef97437a8c9de41d3a5/docs/source/images/polt-live-5-constant-quantities-by-unit.png?inline=false)

See the help page `polt live -h` for further configuration options.

### Configuration Files

`polt` can use configuration files (by default `~/.config/polt/polt.conf` and
`.polt.conf` in the current directory) to simplify invocation. It is also
possible to read and save the current configuration with the `polt config`
command.

### Custom Data Parsers

It is easy to add custom data parsers. Just create a subclass of
`polt.parser.Parser` and specify the import path via the
`polt add-source --parser` option. See the help page
`polt add-source -h` for more details.

## Why on Earth is it called `polt` and not `plot`!?

I am a big fan of swapping syllables or characters around resulting in
ridiculously-sounding words. `polt` is one of those words which I am generating
quite frequently when typing quickly.

## Installation

The `polt` package is best installed via `pip`. Run from anywhere:

```bash
python3 -m pip install --user polt
```

This downloads and installs the package from the [Python Package
Index](https://pypi.org).

You may also install `polt` from the repository root:

```bash
python3 -m pip install --user .
```

## Translations

Currently, the following languages are available:

- English
- German

If you are interested in adding another language, just [open a New Issue
](https://gitlab.com/nobodyinperson/python3-polt/issues/new) and we will get
you going.

## Documentation

Documentation of the `polt` package can be found [here on
GitLab](https://nobodyinperson.gitlab.io/python3-polt/).

Also, the command-line help page `polt -h` is your friend.

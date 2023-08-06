# Menhir

.. image:: https://circleci.com/gh/dialoguemd/menhir.svg?style=svg&circle-token=b8e7721a127637996efff118d0b17aa7522cc96f
    :target: https://circleci.com/gh/dialoguemd/menhir

.. image:: https://codecov.io/gh/dialoguemd/menhir/branch/master/graph/badge.svg?token=Fl2ObQ8DC6
   :target: https://codecov.io/gh/dialoguemd/menhir

Menhir is a build tool for monolithic repositories.  Unlike existing
monolithic build tools, it does not aim at being prescriptive about
how (sub-)projects are built.  It prefers to use established single
project build tools at the project level.

## Documentation

See `ReadTheDocs <https://dialogue-menhir.readthedocs-hosted.com/en/latest/>`_
for documentation.

## Installation

Install using `pip`.

    pip install menhir

## Development

### Dependencies

Assuming that you have a virtual env

```bash
pip install -e .
```

### Tests

For dynamodb connection:

```bash
docker run --rm -p 8000:8000 cnadiminti/dynamodb-local:latest -inMemory
```

```bash
pytest
```

## Release

You need a pypi account to be able to upload the release.

At the top level directory

```bash
bin/release
```

### Caveats

Branch protection needs to be removed temporarly because you wont be able to push to master branch.
The release process should be added to `circleci` and triggered upon a merge to master branch.

# py_vectorbase_rest

Adaptation of [pyEnsemblRest](https://github.com/gawbul/pyEnsemblRest) to work with VectorBase by default.
Offers bindings to VectorBase's Rest API, which is compatible with [ENSEMBL's Rest API](https://rest.ensembl.org/).

## Installation

### Get the latest release with pip

```bash
pip3 install py-vectorbase-rest
```

### Get the latest version from GitLab

```bash
git clone git@gitlab.com:evogenlab/py_vectorbase_rest.git
sudo python3 setup.py install
```

## Usage

Usage is the same as [pyEnsemblRest](https://github.com/gawbul/pyEnsemblRest#usage), with the `EnsemblRest` class replaced by `VectorBaseRest`.
A minimal example is provided in `example.py`.

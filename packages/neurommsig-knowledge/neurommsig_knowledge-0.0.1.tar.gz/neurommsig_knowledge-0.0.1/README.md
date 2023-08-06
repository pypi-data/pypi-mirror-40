<h1 align="center">
  <br>
  NeuroMMSig Knowledge
  </a>
  <br>
</h1>

<p align="center">
This repository contains knowledge curated in Biological Expression Language (BEL)
for NeuroMMSig during the <a href="https://aetionomy.eu">AETIONOMY</a> project.
</p>

## Installation

The latest version can be installed from GitHub with:

```bash
$ pip install git+https://github.com/neurommsig/neurommsig-knowledge.git
```

## Usage

The graph can be loaded with:

```python
from neurommsig_knowledge import repository
from pybel import union

# Get all graphs
graphs = repository.get_graphs()

# Combine them all using pybel.union
graph = union(graphs.values())
```

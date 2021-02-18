# Pyplanning - AI Planning Algorithms in Python

## Introduction
This package represents an implementation of AI Planning algorithms in Python 
including support for processing standard PDDL 1.2 syntax. 

## Dependencies
This code was developed and tested using Python 3.6, though it should run on any
recent version of Python (3+). The library is designed to be lightweight for use
in any existing application, so it does not have any external requirements.

## Installation
To install pyplanning, simply clone the repository and install using pip.

```
git clone https://github.com/kbvatral/pyplanning.git
cd pyplanning
pip install .
```

_Note that this repository is still in active development and is subject to change at any time._
You should consider the current package on the main branch to be an alpha release.
Once the codebase is stable, official releases will be published to PyPI.

## Quickstart
To run the planner using an existing planning problem specified in PDDL format, 
simply load the library and make a few simple function calls to specify 
the domain and problem files. Using some of the included example problems,

```python
import pyplanning as pp

domain_file = "examples/pddl_files/strips/blocksworld.pddl"
problem_file = "examples/pddl_files/strips/stack-blocks.pddl"

domain, problem = pp.load_pddl(domain_file, problem_file)
plan = pp.solvers.search_plan(problem)

if plan is not None:
    print("Plan found:")
    print(plan, "\n")
else:
    print("Planning failed.")
```

For more demonstrations using the included problems, see the `examples/` folder.

## PDDL Support
This package is designed to conform as closely as possible to the PDDL 1.2 standard.
Currently it supports the following requirements extensions:
* `:strips`
* `:typing`
* `:disjunctive-preconditions`

It is highly recommended that the `:typing` extension be used where possible,
as it significantly reduces computation time for most problems in this implementation.

For logic statements, the package currently supports the following operators:
* and
* or
* not

More features will be integrated as development continues, 
focusing on the most commonly used extensions first.
For more information on PDDL, visit [https://planning.wiki/ref/pddl](https://planning.wiki/ref/pddl)

## Solvers
Currently, this package supports solving planning problems through heuristic state-space search (A*).
By default, the serach solver will use a null heuristic, thus performing BFS.
The `pp.solvers.heuristics` package will include the definition of domain agnostic heuristics for
use with any planning problem. However, the solver also supports input of custom heuristic functions
for domain specificity. See the `examples/` folder for example use cases.

Currently, only the ignore delete lists hueristic is implemented to the heuristics package, though
more will be implemented in the future. Note that this heuristic will increase computation time on
some (especially small) problems because of the computational cost of comuting the heuristic.

More solvers (e.g. graphPlan, etc) will be added in future releases.

## License
This package is released under the MIT License. 
See the included license file for details.
# Longtail Large Project Specification

[![PyPi](https://img.shields.io/pypi/v/llps.svg)](https://pypi.org/project/llps/)
[![CircleCI](https://circleci.com/gh/LongTailBio/large_project_specification.svg?style=svg)](https://circleci.com/gh/LongTailBio/large_project_specification)

Bioinformatics projects are often composed of a large number of very heavy flat files. Managing these files is non trivial since operations take a long time and data loss is unacceptable. Because of the size of many of the files involved many typical tools for project management are not viable.

Tracking the files in a project and where they should be found is a core management task. This document details a file specification for tracking the files in a project. The specification file is intended to be placed at a top level directory for the project. The specification file is, itself, lightweight and version controllable.

## Installation

From PyPI
```
pip install llps
```

From Source
```
git clone git@github.com:LongTailBio/large_project_specification.git
cd large_project_specification
python setup.py install
```


## Use

Validate a schema
```
llps validate my-project.llps.yaml
```

Create a new schema
```
llps new <project_name> > my-project.llps.yaml
```

Add files to an existing schema
```
llps add-files <source> my-project.llps.yaml <file>[<file>...] > new-project.llps.yaml
```

## The Specification

A project file is a [YAML](https://yaml.org/spec/1.2/spec.html) file that defines certain metadata about the project, sources for files, and the files themselves. The specification is detailed in `specification.md`

The current version of the specification is `v0.2.0`

## Contributing

Anyone may contibute comments or Suggestions. Please do so using GitHub's issue feature or make a Pull Request.





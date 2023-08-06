# Longtail Large Project Specification

Bioinformatics projects are often composed of a large number of very heavy flat files. Managing these files is non trivial since operations take a long time and data loss is unacceptable. Because of the size of many of the files involved many typical tools for project management are not viable.

Tracking the files in a project and where they should be found is a core management task. This document details a file specification for tracking the files in a project. The specification file is intended to be placed at a top level directory for the project. The specification file is, itself, lightweight and version controllable.

## The Specification

A project file is a [YAML](https://yaml.org/spec/1.2/spec.html) file that defines certain metadata about the project, sources for files, and the files themselves. The specification is detailed in `specification.md`

The current version of the specification is `v0.1.0`

## Contributing

Anyone may contibute comments or Suggestions. Please do so using GitHub's issue feature or make a Pull Request.





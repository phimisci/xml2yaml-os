# XML2YAML-OS

# Introduction
XML2YAML-OS is the open source version of a CLI program initially developed for the journal [Philosophy and the Mind Sciences](https://philosophymindscience.org/). XML2YAML-OS transforms OJS-XML into a YAML format for later use in the pandoc typesetting workflow. The program is written in Python and uses the `lxml` library for XML parsing. The program is designed to be used in a Docker container, but can also be used locally. The program is part of the [Magic Manuscript Maker Typesetting Workflow]() of the journal.

The YAML format in this repository was developed in view of the default template of the [Typesetting-Container-OS](https://github.com/phimisci/typesetting-container-os). If you need to parse different attributes or elements from the OJS XML, you can easily adjust the `xml2yaml.py` script to your needs.

# Installation
There are two ways to use XML2YAML: locally or in a Docker container.

## Local installation
First of all, you need to download this repository using `git clone`. Before using XML2YAML-OS, make sure to install the required dependencies. You can do so via `pip install -r requirements.txt` (assuming that you have Python installed and are executing this command in the XML2YAML folder). When working with Mac or Linux, you might have to use `pip3 install -r requirements.txt` instead.

## Docker installation
You can also use XML2YAML-OS in a Docker container. You can either build the image locally using `docker build -t xml2yaml-os .` from within the repositories' root folder or use the GitHub container registry. When using the GitHub container registry, you can pull the image using `docker pull ghcr.io/phimisci/xml2yaml-os:latest`. 

# How To
Before you can use XML2YAML, you need to have an OJS XML file. You can download this file from the OJS backend via the [Native XML Plugin](https://docs.pkp.sfu.ca/admin-guide/3.3/en/data-import-and-export) which is installed by default from OJS 3.3 onwards. The XML file contains all the metadata of the article, such as title, authors, abstract, keywords, etc. You can start the export of a specific article under `Tools > Import/Export > Native XML Plugin > Export`.

XML2YAML is an easy-to-use CLI program that takes only the filepath to the OJS XML as an input argument. Optionally, you can also pass additional arguments to the program including different metadata fields which might be missing in the XML file. The standard version of XML2YAML-OS assumes that the YAML file should contain the following fields:

```yaml
title: 'The Eternal Boy: A Study in Agelessness and Memory'
subtitle: Exploring Identity, Temporality, and the Philosophy of Neverland
author:
- name: Wendy Darling
  affiliation:
  - organization: University of Oxford
  email: w.darling@oxford.ac.uk
  orcid: 0000-0002-5678-9012
- name: Peter Pan
  affiliation:
  - organization: SOAS London
  - organization: Neverland
  email: peter.pan@neverland.com
  orcid: 0000-1101-1234-5678
keywords:
- Agelessness
- Memory theory
- Identity
- Temporality
- Neverland metaphysics
- Fantasy ontology
- Child psychology
- Flight dynamics
abstract: |-
  How does the notion of agelessness shape identity and memory in an eternal youth like Peter Pan? This article examines the metaphysics of agelessness through the lens of Peter Pan’s unchanging form and his shifting memories, drawing from theories of temporality and identity. We argue that Neverland serves as a temporal vacuum, where time functions differently, creating unique challenges to traditional philosophical concepts of identity and selfhood. The implications of living outside of time, where one remains physically unchanged but psychologically impacted by infinite experiences, are explored. This work also touches on the phenomenology of flight, a central theme in Peter Pan’s existence, as it symbolizes his defiance of physical and temporal limitations. The article situates these discussions within the broader debate on fantasy ontology and its relation to real-world psychological and philosophical frameworks.
date: '2024'
volume: 7
doi: 10.1111/12345678
author-short: Darling & Pan
```

Note that some fields can also have empty values, which will simply cause the fields to be emtpy in the rendered files created with [Typesetting-Container-OS](https://github.com/phimisci/typesetting-container-os) (e.g. `subtitle`).

# Versions

## 1.0.0 (20.11.2024)
- Initial release of XML2YAML-OS
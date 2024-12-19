# XML2YAML-OS

# Introduction
This is the XML2YAML-OS version specifically designed for the needs of the journal [Philosophy and the Mind Sciences](https://philosophymindscience.org/). XML2YAML-OS transforms OJS XML into a YAML format for later use in the pandoc typesetting workflow. The program is written in Python and uses the `lxml` library for XML parsing. The program is designed to be used in a Docker container, but can also be used locally. The program is part of the [Magic Manuscript Maker Typesetting Workflow](https://github.com/phimisci) of the journal. For more information on how to use XML2YAML-OS, please refer to the README.md in the main branch.

# Installation
There are two ways to use XML2YAML: locally or in a Docker container.

## Local installation
First of all, you need to download this repository using `git clone`. Before using XML2YAML-OS, make sure to install the required dependencies. You can do so via `pip install -r requirements.txt` (assuming that you have Python installed and are executing this command in the XML2YAML folder). When working with Mac or Linux, you might have to use `pip3 install -r requirements.txt` instead.

## Docker installation
You can also use XML2YAML-OS in a Docker container. You can either build the image locally using `docker build -t xml2yaml-os .` from within the repositories' root folder or use the GitHub container registry. When using the GitHub container registry, you can pull the image using `docker pull ghcr.io/phimisci/xml2yaml-os:latest`. 

# How To
Before you can use XML2YAML, you need to have an OJS XML file. You can download this file from the OJS backend via the [Native XML Plugin](https://docs.pkp.sfu.ca/admin-guide/3.3/en/data-import-and-export) which is installed by default from OJS 3.3 onwards. The XML file contains all the metadata of the article, such as title, authors, abstract, keywords, etc. You can start the export of a specific article under `Tools > Import/Export > Native XML Plugin > Export`.

XML2YAML is an easy-to-use CLI program that takes only the filepath to the OJS XML as an input argument. Optionally, you can also pass additional arguments to the program including different metadata fields which might be missing in the XML file. The PhiMiSci version of XML2YAML-OS assumes that the YAML file should contain the following fields:

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
author-short: Darling, W., & Pan, P.
```

Note that some fields can also have empty values, which will simply cause the fields to be empty in the rendered files created with [Typesetting-Container-OS](https://github.com/phimisci/typesetting-container-os) (e.g. `subtitle`).

## Local usage
To use XML2YAML locally, you can simply run the `xml2yaml.py` script with the path to the OJS XML file as an argument. For example, if you have an XML file called `article.xml` in the same folder as the `xml2yaml.py` script, you can run the following command:

```bash
python xml2yaml.py article.xml
```

The script will then create a file called `metadata.yaml` in the `yaml_output/` folder. You can use the following additional arguments to the script (note that these arguments overwrite potential values in the XML file):

```bash	
usage: xml2yaml.py [-h] [-y YEAR] [-v VOLUME] [-o ORCID [ORCID ...]] [-d DOI] xml_file

XML2YAML-OS CLI program. Converts OJS XML to YAML.

positional arguments:
  xml_file              Path to the input XML file

options:
  -h, --help            show this help message and exit
  -y YEAR, --year YEAR  Year of publication
  -v VOLUME, --volume VOLUME
                        Volume number
  -o ORCID [ORCID ...], --orcid ORCID [ORCID ...]
                        ORCID key-value pairs of authors (separated via blank space when multiple authors): --orcid
                        <AUTHOR_LASTNAME>=<ORCID> || --orcid Starke=0000-0001-1111-1111 Jurczyk=0000-0002-5943-2305
  -d DOI, --doi DOI     DOI of the article.

```

## Docker usage
If you want to use XML2YAML in a Docker container, you can either use the image from the GitHub container registry or build the image locally. To run the container, you need to (1) mount the XML file into the container, (2) mount you current folder to the `yaml_output` folder in the container, and (3) pass the filename only (!) as an argument to the container. The following command shows how to run the container with the `article.xml` file that is locally stored under the relative path `files/test/article.xml`. To process this file with the container, you can run the following command (note that the syntax might be slightly different when using Windows):

```bash
docker run --rm -v $(pwd)/files/test/article.xml:/app/xml_input/xml_file.xml -v $(pwd):/app/yaml_output xml2yaml-os article.xml
```

In this command, we first mount (`-v`) the `article.xml` file into the container under the path `/app/xml_input/xml_file.xml`. We then mount the current folder into the container under the path `/app/yaml_output` so that the YAML output will be visible in our current working folder. The last argument `article.xml` is the filename only and is used as an argument the `xml2yaml.py` file in the container. The container will then create a file called `metadata.yaml` in the `yaml_output` folder, which should be visible in the current working directory on our local machine (assuming that it has been mounted as previously shown).

Similar to the local usage, you can also pass additional arguments to the container. The following command shows how to run the container with the `article.xml` file and additional arguments:

```bash
docker run --rm -v $(pwd)/files/test/article.xml:/app/xml_input/xml_file.xml -v $(pwd):/app/yaml_output xml2yaml-os article.xml -y 2024 -v 7 -o Darling=0000-0001-1111-1111 Pan=0000-0002-5943-2305 --doi 10.1111/12345678
```

# About
XML2YAML-OS was developed by Thomas Jurczyk ([thomjur](https://github.com/thomjur)) the [Philosophy and the Mind Sciences](https://philosophymindscience.org/) journal. The program is part of the [Magic Manuscript Maker Typesetting Workflow](https://github.com/phimisci) of the journal. If you have any questions or suggestions, feel free to open an issue in this repository.

# Versions

## 1.0.0 (19.12.2024)
- Initial release of XML2YAML-OS for Philosophy and the Mind Sciences
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
---
title: 'Cognitive control and semantic thought variability across sleep and wakefulness'
subtitle: ''
author:
- name: Remington Mallett
  affiliation:
  - organization: Department of Psychology, Northwestern University
  email: mallett.remy@gmail.com
  orcid: 0000-0001-6183-3098
- name: Yasmeen Nahas
  affiliation:
  - organization: Department of Psychology, Northwestern University
  email: yasmeennahas2023@u.northwestern.edu
  orcid: null
- name: Kalina Christoff
  affiliation:
  - organization: Department of Psychology, University of British Columbia
  email: kchristoff@psych.ubc.ca
  orcid: 0000-0003-2841-8647
- name: Ken A. Paller
  affiliation:
  - organization: Department of Psychology, Northwestern University
  email: kap@northwestern.edu
  orcid: 0000-0003-4415-4143
- name: Caitlin Mills
  affiliation:
  - organization: Department of Educational Psychology, University of Minnesota
  email: cmills@umn.edu
  orcid: 0000-0003-4498-0496
authorstex: |
  ```{=latex}
  {\color{black}\noindent \ignorespacesafterend \bfseries \noindent \hskip-3ptRemington Mallett}%
  {\color{blue}\footnote{\label{fn-a}Department of Psychology, Northwestern University.}{\href{https://orcid.org/0000-0001-6183-3098}{\textcolor{orcidlogocol}{\aiOrcid}}}{\color{black}(mallett.remy@gmail.com)}}

  {\color{black}\noindent \ignorespacesafterend \bfseries \noindent Yasmeen Nahas}%
  {\color{blue}\(^{\textnormal{\ref{fn-a}}}\){\color{black}(yasmeennahas2023@u.northwestern.edu)}}

  {\color{black}\noindent \ignorespacesafterend \bfseries \noindent Kalina Christoff}%
  {\color{blue}\footnote{\label{fn-b}Department of Psychology, University of British Columbia.}{\href{https://orcid.org/0000-0003-2841-8647}{\textcolor{orcidlogocol}{\aiOrcid}}}{\color{black}(kchristoff@psych.ubc.ca)}}

  {\color{black}\noindent \ignorespacesafterend \bfseries \noindent Ken A. Paller}%
  {\color{blue}\(^{\textnormal{\ref{fn-a}}}\){\href{https://orcid.org/0000-0003-4415-4143}{\textcolor{orcidlogocol}{\aiOrcid}}}{\color{black}(kap@northwestern.edu)}}

  {\color{black}\noindent \ignorespacesafterend \bfseries \noindent Caitlin Mills}%
  {\color{blue}\footnote{\label{fn-c}Department of Educational Psychology, University of Minnesota.}{\href{https://orcid.org/0000-0003-4498-0496}{\textcolor{orcidlogocol}{\aiOrcid}}}{\color{black}(cmills@umn.edu)}}

  \```
keywords: [Creativity ∙ Dreaming ∙ Mind-wandering ∙ Natural language processing ∙
    Spontaneous thought]
tags:
- Creativity
- Dreaming
- Mind-wandering
- Natural language processing
- Spontaneous thought
abstract: |-
  The flow of thought is persistent, and at times merciless. Mental content is generated throughout the day and into the night, moving forward predictably at times but surprisingly at others. Understanding what influences the trajectory of thought—how thoughts continuously unfold over time—has important implications for the diagnosis and treatment of thought disorders like schizophrenia and recurrent nightmares. Here, we examine whether cognitive control restricts moment-to-moment content shifts across sleep and wakefulness, thus acting as a fundamental constraint on thought variability. Thought variability was measured as the semantic incoherence between sequential thought phrases and was applied to independent datasets of dreaming and waking reports. Our results show that within both sleeping and waking reports, conditions typically marked by higher levels of cognitive control were associated with decreased thought variability (i.e., semantic incoherence). During wakefulness, on-task conditions were associated with reduced levels of thought variability compared to off-task conditions, and thought variability was greater when thoughts wandered around more freely. During sleep, lucid dreams, marked by higher levels of cognitive control, were associated with reduced levels of thought variability compared to non-lucid dreams. Together, these results suggest that cognitive control may limit thought variability across the 24-hour cycle of thought generation. Such findings are consistent with the Dynamic Framework of Thought, where mental states are expected to vary on a continuum of deliberate constraints, with lower cognitive control leading to a categorical cluster of spontaneous thought processes that includes both mind-wandering during wakefulness and non-lucid dreams during sleep. This observation has broad implications for models of cognition, specifically highlighting the continuity of cognitive processes throughout the circadian cycle and the importance of considering varying levels of thought constraint in both waking and dreaming states.
name-short: Mallett, R., Nahas, Y., Christoff, K., Paller, K. A., & Mills, C.
name-long: Mallett, Remington, Yasmeen Nahas, Kalina Christoff, Ken A. Paller, and
  Caitlin Mills
name-hdr: Remington Mallett, Yasmeen Nahas, Kalina Christoff, Ken A. Paller, and Caitlin
  Mills
title-hdr: 'Cognitive control and semantic thought variability across sleep and wakefulness'
date: '2024'
volume: '*7*'
artid: 10307
author-meta: Remington Mallett, Yasmeen Nahas, Kalina Christoff, Ken A. Paller, Caitlin
  Mills
title-meta: 'Cognitive control and semantic thought variability across sleep and wakefulness.'
specialissue: |-
  This article is part of a special issue.
...
```

Note that some fields can also have empty values, which will simply cause the fields to be empty in the rendered files created with [Typesetting-Container-OS](https://github.com/phimisci/typesetting-container-os) (e.g. `subtitle`).

## Local usage
To use XML2YAML locally, you can simply run the `xml2yaml.py` script with the path to the OJS XML file as an argument. For example, if you have an XML file called `article.xml` in the same folder as the `xml2yaml.py` script, you can run the following command:

```bash
python xml2yaml.py article.xml
```

The script will then create a file called `metadata.yaml` in the `yaml_output/` folder. You can use the following additional arguments to the script (note that these arguments overwrite potential values in the XML file):

```bash	
usage: xml2yaml.py [-h] [-y YEAR] [-v VOLUME] [-o ORCID [ORCID ...]] [-s SPECIALISSUE] xml_file

XML2YAML-OS CLI program. Converts OJS XML to YAML.

positional arguments:
  xml_file              Path to the input XML file

optional arguments:
  -h, --help            show this help message and exit
  -y YEAR, --year YEAR  Year of publication
  -v VOLUME, --volume VOLUME
                        Volume number
  -o ORCID [ORCID ...], --orcid ORCID [ORCID ...]
                        ORCID key-value pairs of authors (separated via blank space when multiple authors): --orcid <AUTHOR_LASTNAME>=<ORCID> || --orcid Starke=0000-0001-1111-1111 Jurczyk=0000-0002-5943-2305
  -s SPECIALISSUE, --specialissue SPECIALISSUE
                        The special issue text that appears in the beginnng of an article. Needs to be passed as one string using ".
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
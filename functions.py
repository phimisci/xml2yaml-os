'''
Helper functions for the main script.
'''

import lxml, re, html
import logging
from lxml import etree
from collections import OrderedDict
from typing import List, Union, Literal, OrderedDict, Dict, Optional
from bs4 import BeautifulSoup


def create_author_dict_4yaml() -> OrderedDict:
    '''Helper Function for create_yaml_dict() to create author entries.
    
        Returns
        -------
        OrderedDict
            An empty OrderedDict with keys for name, affiliation, affsymb, email, orcid.
    
    '''
    author_dict: OrderedDict = OrderedDict()
    author_dict["name"] = None
    # Dict {'organization' : <NAME_UNI>} as list entries
    author_dict["affiliation"] = list()
    author_dict["affsymb"] = 2
    author_dict["email"] = None
    author_dict["orcid"] = None

    return author_dict

def create_dict_4yaml() -> OrderedDict:
    '''Function to create an empty YAML dict that can be filled with information form OJS XML.

        Returns
        -------
        OrderedDict
            The empty YAML dict with keys for title, subtitle, author, keywords, tags, abstract, name-short, date, volume, doi.
    '''
    pandoc_yaml_dict: OrderedDict = OrderedDict()
    pandoc_yaml_dict["title"] = None
    pandoc_yaml_dict["subtitle"] = "" # Empty string because otherwise null appears in template
    pandoc_yaml_dict["author"] = list()
    pandoc_yaml_dict["keywords"] = list()
    pandoc_yaml_dict["abstract"] = None
    pandoc_yaml_dict["author-short"] = None
    pandoc_yaml_dict["date"] = None
    pandoc_yaml_dict["volume"] = None
    pandoc_yaml_dict["doi"] = None

    return pandoc_yaml_dict
    
def create_keywords_4yaml(xml: lxml.etree._Element) -> List[str]:
    '''Function to create a sorted tags list with separate keywords.

        Parameters
        ----------
        xml: lxml.etree._Element
            The node "keywords" from parent tree.

        Returns
        -------
        List[str]
            The sorted list for YAML and later JATS output.

    '''
    l: List[str] = list()
    if len(xml) > 0:
        for child in xml:
            text: str = child.text.strip().capitalize() if child.text else ""
            l.append(text)
    l.sort()
    return l

def escape_html(input: str) -> str:
    '''Function to clean text coming from OJS (title, abstract) of HTML elements etc.

        Parameters
        ----------
        input: str
            The raw text coming form OJS XML.

        Returns
        -------
        str
            The clean abstract or title.
    '''
    input = html.unescape(input)
    # Removing linebreaks
    input = re.sub(r"\n|\t", "", input)
    # Removing unnecessary whitespace
    input = re.sub(r"\s{2,}", " ", input)
    # Replacing html <b> and <em> with markdown equivalents
    input = re.sub(r"<em>|</em>", r"*", input)
    input = re.sub(r"<b>|</b>", r"**", input)
    # Remove remaining HTML tags using BeautifulSoup
    soup = BeautifulSoup(input, "html.parser")
    input = soup.get_text()

    return input

def parse_given_name(given_name: str, abbr_style: Union[Literal["full"], Literal["light"]] = "light") -> str:
    '''Function to parse a given name string and transform it into an abbreviated format for PhiMiSci pandoc YAML.

        Parameters
        ----------
        given_name: str
            The given name as one string.

        abbr_style: str (default: "light")
            Can be either "light" or "full". "light" means that given name "Adam Susan" is returned as "Adam S.", "full" results in "A. S.".

        Returns
        -------
        str
            A string of the format (1) Adam S. or (2) A. S. depending on argument of abbr_style.
    '''
    gn_list = given_name.split()
    if len(gn_list) > 1:
        name_str: str = ""
        if abbr_style == "light":
            for idx, name in enumerate(gn_list):
                if idx == 0:
                    name_str = name
                else:
                    name_str += " " + name[0] + "."
        else:
            for idx, name in enumerate(gn_list):
                if idx == 0:
                    name_str = name[0] + "."
                else:
                    name_str += " " + name[0] + "."
        return name_str
    elif len(gn_list) == 0:
        logging.warning("Given_name field seems to be empty.")
        return ""
    else:
        if abbr_style == "light":
            return given_name
        else:
            return given_name[0]+"."
        
def parse_orcid(author_orcid_list: List[str]) -> Dict[str, str]:
    '''Function to parse AUTHOR=ORCID pair string from argparse.

        Parameters
        ----------
            author_orcid_string: List[str]
                The list of strings received as an argument from command line interface via argparse.

        Returns
        -------
            Dictionary with author lastname (key) and ORCID (value).
    '''
    # Parsing author_orcid pairs from list
    author_orcid_dict = dict()
    for author_orcid_pair in author_orcid_list:
        # Try to split entries on "="
        split_pairs = author_orcid_pair.split("=")
        if len(split_pairs) != 2:
            logging.warning(f"Something went wrong when splitting {author_orcid_pair}. Ignoring this entry.")
        else:
            author_name = split_pairs[0].strip()
            orcid = split_pairs[1].strip()
            # Adding entry to dict
            author_orcid_dict[author_name] = orcid
    return author_orcid_dict

    

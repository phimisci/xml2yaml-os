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
    author_dict["email"] = None
    author_dict["orcid"] = None

    return author_dict

def create_dict_4yaml() -> OrderedDict:
    '''Function to create an empty YAML dict that can be filled with information form OJS XML.'''
    pandoc_yaml_dict: OrderedDict = OrderedDict()
    pandoc_yaml_dict["title"] = None
    pandoc_yaml_dict["subtitle"] = "" # Empty string because otherwise null appears in template
    pandoc_yaml_dict["author"] = list()
    pandoc_yaml_dict["authorstex"] = None
    pandoc_yaml_dict["keywords"] = None
    pandoc_yaml_dict["tags"] = list()
    pandoc_yaml_dict["abstract"] = None
    pandoc_yaml_dict["name-short"] = None
    pandoc_yaml_dict["name-long"] = None
    pandoc_yaml_dict["name-hdr"] = None
    pandoc_yaml_dict["title-hdr"] = None
    pandoc_yaml_dict["date"] = None
    pandoc_yaml_dict["volume"] = None
    pandoc_yaml_dict["artid"] = None
    pandoc_yaml_dict["author-meta"] = None
    pandoc_yaml_dict["title-meta"] = None

    return pandoc_yaml_dict

def create_keyword_list_4yaml(xml: lxml.etree._Element) -> List[str]:
    '''Function to create a key word list style [<KW> <KW> <KW> ... <KW>] for YAML output.

        Parameters
        ----------
            xml: lxml.etree._Element
                The node "keywords" from parent tree.

        Returns
        -------
            list(str)
                The str for YAML output.

    '''
    string = ""
    if len(xml) > 0:
        keyword_list: List[str] = list()
        for child in xml:
            # Get all keywords from XML
            keyword_list.append(child.text.strip().capitalize() if child.text else "NONE")
        # Sort keywords alphabetically
        keyword_list.sort()
        # Create string
        for idx,kw in enumerate(keyword_list):
            if idx < len(keyword_list)-1:
                string += kw + " ∙ "    
            else:
                string += kw
        return [string]
    else:
        return ["NO KEYWORDS"]

def create_tags_list_4yaml(xml: lxml.etree._Element) -> List[str]:
    '''Function to create a tags list with separate keywords for later JATS output.

        Parameters
        ----------
            xml: lxml.etree._Element
                The node "keywords" from parent tree.

        Returns
        -------
            list(str)
                The list for YAML and later JATS output.

    '''
    l: List[str] = list()
    if len(xml) > 0:
        for child in xml:
            text: str = child.text.strip().capitalize() if child.text else ""
            l.append(text)
    l.sort()
    return l


def create_latex_string(author_dict: OrderedDict) -> str:
    '''Create latex string for pandoc yaml.

        Pretty complex. First, collect all affiliations in OrderedDict and create latex footnotes. Afterwards, iterate over authors and create LaTeX based on information from author_dict plus footnote for affiliation from previous OrderedDict. 

        Parameters
        ----------
            author_dict: OrderedDict
                OrderedDict with author data.
            
        Returns
        -------
            Latex str for YAML output.

    '''
    ##### create affiliation dict (LaTeX footnotes plus authors)
    # because latex footnotes have style fn-a, fn-b etc.
    abc = "abcdefghijklmnopqrstuvwxyz"
    aff_index = 0

    affiliations_fn_dict: OrderedDict = OrderedDict()

    # collect affiliations
    for author in author_dict:
        for aff in author["affiliation"]:
            if aff["organization"] not in affiliations_fn_dict.keys():
                affiliations_fn_dict[aff["organization"]] = {
                    "latex_fn": fr"\footnote{{\label{{fn-{abc[aff_index]}}}{aff['organization']}.}}",
                    "label": f"fn-{abc[aff_index]}",
                    "authors": [author["name"]]
                }
                aff_index += 1
            else:
                affiliations_fn_dict[aff["organization"]]["authors"].append(author["name"])
            
    test_string = r'```{=latex}' + '\n'

    # to check if new footnote or ref should be created
    already_used_fn = list()

    for idx,author in enumerate(author_dict):
        ### adding NAME
        if idx == 0:
            test_string += fr'{{\color{{black}}\noindent \ignorespacesafterend \bfseries \noindent \hskip-3pt{author["name"]}}}%'+'\n'+ fr'{{\color{{blue}}'
        else:
            test_string += fr'{{\color{{black}}\noindent \ignorespacesafterend \bfseries \noindent {author["name"]}}}%'+'\n'+ fr'{{\color{{blue}}'

        ### adding AFFILIATION
        ##### necessary to add "," after refs in case there are more than one
        citation_counter = 0
        for aff in affiliations_fn_dict:
            for aff2 in author["affiliation"]:
                if aff in aff2["organization"]:
                    if affiliations_fn_dict[aff]["label"] not in already_used_fn:
                        if citation_counter > 0:
                            # add , first
                            test_string += r"\(^\textnormal{,}\)"
                        test_string += affiliations_fn_dict[aff]["latex_fn"]
                        already_used_fn.append(affiliations_fn_dict[aff]["label"])
                        citation_counter += 1
                    else:
                        if citation_counter > 0:
                            # add , first
                            test_string += r"\(^\textnormal{,}\)"
                        test_string += fr"\(^{{\textnormal{{\ref{{{affiliations_fn_dict[aff]['label']}}}}}}}\)"
                        citation_counter += 1

        ### adding ORCID
        if author["orcid"] is not None:
            test_string += fr'{{\href{{https://orcid.org/{author["orcid"]}}}{{\textcolor{{orcidlogocol}}{{\aiOrcid}}}}}}'

        ### adding EMAIL
        test_string += fr"{{\color{{black}}({author['email']})}}}}" + "\n\n"
    
    test_string += "```\n"

    return test_string

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

    

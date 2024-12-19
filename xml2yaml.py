'''
Main file to convert OJS XML to PhiMiSci-YAML for file creation with Typesetting-Container-OS.
Copyright (c) 2024 Thomas Jurczyk and Philosophy and the Mind Sciences.
Version: 1.0.0 (2024-12-19)
'''

from yaml_setup import *
from lxml import etree
from xml.etree.ElementTree import Element
import html
import argparse
import os, re
from functions import *
import logging
from typing import Optional, Tuple

def parse_arguments() -> Tuple[Optional[str], Optional[str], Optional[int], Optional[List[str]], Optional[str], Optional[str]]:
    parser = argparse.ArgumentParser(description='XML2YAML-OS CLI program. Converts OJS XML to YAML.')
    parser.add_argument('xml_file', type=str, help='Path to the input XML file')
    # Additional year field might be necessary if the year is not present in the XML file
    parser.add_argument("-y", "--year", type=str, help="Year of publication")
    parser.add_argument("-v", "--volume", type=str, help="Volume number")
    # Sometimes, the ORCID is not present in the XML file. In this case, the ORCID can be passed as a command line argument
    # Example: --orcid Starke=0000-0001-1111-1111 Jurczyk=0000-0002-5943-2305
    parser.add_argument("-o", "--orcid", type=str, nargs="+", help="ORCID key-value pairs of authors (separated via blank space when multiple authors): --orcid <AUTHOR_LASTNAME>=<ORCID> || --orcid Starke=0000-0001-1111-1111 Jurczyk=0000-0002-5943-2305")
    parser.add_argument("-s", "--specialissue", type=str, help="The special issue text that appears in the beginnng of an article. Needs to be passed as one string using \".")
    # Parse arguments
    args = parser.parse_args()
    # The path to the XML file can be accessed using the args.xml_file attribute
    xml_file_path = args.xml_file
    return (xml_file_path, args.year, args.volume, args.orcid,args.specialissue)

def main(xml_filepath: Optional[str], year: Optional[str], volume: Optional[str], orcid: Optional[List[str]], special_issue: Optional[str]) -> None:
    '''Main program logic to convert XML2YAML.

        Parameters
        ----------
            xml_filepath: Optional[str]
                The path to the XML file (cannot be None actually because of required positional argument).
            year: Optional[str]
                Publishing year of the article (str or None).
            volume: Optional[str]
                Number of the volume in which the article appears (int or None).
            orcid: Optional[str]
                String with key-value pairs of <AUTHOR_LASTNAME> and <ORCID>. Example: --orcid Starke=0000-0001-1111-1111 Jurczyk=0000-0002-5943-2305 (this string needs to be parsed later on.
            special_issue: Optional[str]
                A string with information about special issue. Used in articles that are part of a special issue. 

    '''
    # OJS XML file should be in the xml folder
    if os.environ.get("IS_CONTAINER") == "true":
        xml_filepath = "xml_input/"+xml_filepath
    else:
        xml_filepath = xml_filepath
    # Check if file exists
    if not os.path.isfile(xml_filepath):
        print("ERROR_NO_FILE_FOUND")
        exit()
    ### Parse XML
    xml_data = etree.parse(xml_filepath)
    root = xml_data.getroot()
    # Dropping submission files from XML
    for child in root:
        if child.tag == "{http://pkp.sfu.ca}submission_file":
            root.remove(child)
    # Find publication node
    publication_data = root.find("{http://pkp.sfu.ca}publication")
    # Exiting if publication_data not found
    if publication_data is None:
        logging.error("NO_PUBLICATION_DATA_FOUND. EXIT.")
        exit()
    # Initialize dictionary for yaml
    data_dict = create_dict_4yaml()
    ### Parse title
    if publication_data.find("{http://pkp.sfu.ca}title") is not None:
        # Parsing main title
        title_element = publication_data.find("{http://pkp.sfu.ca}title")
        assert title_element is not None, "Title element not found"
        title: str = title_element.text if title_element.text else "NO_TITLE_FOUND"
        title = escape_html(title)
        # Parsing subtitle
        subtitle: Optional[str] = None
        subtitle_element = publication_data.find("{http://pkp.sfu.ca}subtitle")
        if subtitle_element is not None:
            subtitle = subtitle_element.text if subtitle_element.text else None
            if subtitle is not None:
                subtitle = escape_html(subtitle)
                data_dict["subtitle"] = subtitle
        # Parsing title
        ## There are different cases:
        ##      1. Normal title ("This is an article title")
        ##      2. Title with main title and subtitle("This is an article: It is interesting" or "Is this an article? If so, it is interesting")
        # Split on either : or ?
        title_list = [title.strip() for title in re.split(r"(:|\?)", title.strip(), maxsplit=1) if title != ""]
        if len(title_list) > 3 and len(title_list) == 0: # the title seems to be missing or is incorrect
            logging.warning("There seems to be an issue with the title parsing. Please check manually.")
            data_dict["title"] = SingleQuotedString(title)
            data_dict["title-hdr"] = SingleQuotedString(title)
            if subtitle:
                data_dict["title-meta"] = SingleQuotedString(f"{title}: {subtitle}.")
            else:
                data_dict["title-meta"] = SingleQuotedString(f"{title}.")
        else:
            # First case: main title + subtitle
            if len(title_list) == 3: 
                data_dict["title"] = SingleQuotedString(title_list[0]) if title_list[1] == ":" else SingleQuotedString(title_list[0]+title_list[1])
                data_dict["subtitle"] = SingleQuotedString(title_list[2])
                data_dict["title-hdr"] = SingleQuotedString(title_list[0]) if title_list[1] == ":" else SingleQuotedString(title_list[0]+title_list[1])
                data_dict["title-meta"] = SingleQuotedString(title_list[0] + f"{title_list[1]} " + title_list[2] + ".")
            # Second case: main title ending with ?
            elif len(title_list) == 2:
                if title_list[1] == "?":
                    data_dict["title"] = SingleQuotedString(title_list[0]+title_list[1])
                    data_dict["title-hdr"] = SingleQuotedString(title_list[0]+title_list[1])
                    if subtitle:
                        data_dict["title-meta"] = SingleQuotedString(f"{title_list[0]}? {subtitle}.")
                    else:
                        data_dict["title-meta"] = SingleQuotedString(f"{title_list[0]}?")
                else:
                    data_dict["title"] = SingleQuotedString(title_list[0])
                    data_dict["title-hdr"] = SingleQuotedString(title_list[0])
                    if subtitle:
                        data_dict["title-meta"] = SingleQuotedString(f"{title_list[0]}: {subtitle}.")
                    else:
                        data_dict["title-meta"] = SingleQuotedString(f"{title_list[0]}.")
            # Third case: only main title in title field
            else:
                data_dict["title"] = SingleQuotedString(title_list[0])
                data_dict["title-hdr"] = SingleQuotedString(title_list[0])
                if subtitle:
                    data_dict["title-meta"] = SingleQuotedString(f"{title_list[0]}: {subtitle}.")
                else:
                    data_dict["title-meta"] = SingleQuotedString(f"{title_list[0]}.")        
    else:
        logging.warning("No title field found in XML. Replacing with NO_TITLE_FIELD_FOUND_IN_XML.")
        data_dict["title"] = SingleQuotedString("NO_TITLE_FIELD_FOUND_IN_XML")
        data_dict["title-hdr"] = SingleQuotedString("NO_TITLE_FIELD_FOUND_IN_XML")
        data_dict["title-meta"] = SingleQuotedString("NO_TITLE_FIELD_FOUND_IN_XML"+".")

    ### Parse abstract
    if publication_data.find("{http://pkp.sfu.ca}abstract") is not None:
        abstract_element = publication_data.find("{http://pkp.sfu.ca}abstract")
        abstract: str = abstract_element.text if abstract_element.text else "NO_ABSTRACT_FOUND"
        data_dict["abstract"] = escape_html(abstract)
        data_dict["abstract"] = LiteralString(data_dict["abstract"])
    else:
        logging.warning("No abstract field found in XML. Replacing with NO_ABSTRACT_FIELD_FOUND_IN_XML.")
        data_dict["abstract"] = LiteralString("NO_ABSTRACT_FIELD_FOUND_IN_XML")
    
    ##### Parse article id
    if root.find("{http://pkp.sfu.ca}id[@type='internal']") is not None:
        artid_element = root.find("{http://pkp.sfu.ca}id[@type='internal']")
        assert artid_element is not None, "Article id not found found"
        artid: str = artid_element.text if artid_element.text else "NO_ART_ID"
        data_dict["artid"] = html.unescape(artid)
        data_dict["artid"] = PlainInt(data_dict["artid"])
    else:
        logging.warning("No article ID found in XML. Replacing with -999999999.")
        data_dict["artid"] = PlainInt(-999999999)

    ### Parse volume number (take XML volume if present and no arg given; arg volume always overwrites XML volume)
    if (publication_data.find(".//{http://pkp.sfu.ca}volume") is not None) and (volume is None):
        volume_element = publication_data.find(".//{http://pkp.sfu.ca}volume")
        volume_no: str = volume_element.text if volume_element.text else "NO_VOL_NUMBER"
        data_dict["volume"] = html.unescape(volume_no)
        data_dict["volume"] = "*"+data_dict["volume"]+"*"
        data_dict["volume"] = data_dict["volume"]
    elif volume is not None:
        data_dict["volume"] = html.unescape(volume)
        data_dict["volume"] = "*"+data_dict["volume"]+"*"
        data_dict["volume"] = data_dict["volume"]
    else:
        data_dict["volume"] = "NO_VOL_NUMBER_FOUND"

    ### Parse keywords
    if publication_data.find(".//{http://pkp.sfu.ca}keywords") is not None:
        keyword_node = publication_data.find(".//{http://pkp.sfu.ca}keywords")
        data_dict["keywords"] = PlainList(create_keyword_list_4yaml(keyword_node))
         ####### Parse keywords for tags metadata field for later JATS output
        data_dict["tags"] = create_tags_list_4yaml(keyword_node)

    else:
        data_dict["keywords"] = PlainList(["NO_KEYWORDS_FOUND"])

    ### Parse year
    if year is not None:
        # Check if argument is a valid year
        if re.match(r"\d{4}", year):
            data_dict["date"] = SingleQuotedString(year)
            # If the date is valid put appears to be strange as year of publication, send warning
            if int(year) < 2018 or int(year) > 2100:
                logging.warning(f"The passed year {year} is valid but appears to be strange as date of publication. Please verify if the year is correct.")
        else:
            logging.warning(f"No year was added to yaml. The year argument {year} cannot be parsed. Is it really a year with four digits?")

    ### Parse ORCID (IMPORTANT: NEEDS TO BE DONE BEFORE AUTHOR PARSING!)
    orcid_dict: Optional[dict] = None
    if orcid is not None:
        orcid_dict = parse_orcid(orcid)

    ##### PARSE AUTHOR DATA & CREATE LATEX - TODO: catch missing entries
    authors_node = publication_data.find(".//{http://pkp.sfu.ca}authors")
    assert authors_node is not None, "No authors node found"
    # counter to find first author
    auth_index: int = 0 # enumerate not working?!
    for author in authors_node:
        # init author dict
        author_dict = create_author_dict_4yaml()
        # create full name
        given_name_node = author.find(".//{http://pkp.sfu.ca}givenname")
        family_name_node = author.find(".//{http://pkp.sfu.ca}familyname")
        assert given_name_node is not None, "Given name node not found"
        assert family_name_node is not None, "Family name node not found"
        given_name = given_name_node.text
        family_name = family_name_node.text
        assert given_name is not None, "Given name not found"
        assert family_name is not None, "Family name not found"
        given_name = given_name.strip()
        family_name = family_name.strip()
        full_name = given_name + " " + family_name
        # add orcid from CLI arg if present
        if orcid_dict is not None:
            for k,v in orcid_dict.items():
                if k.lower() in family_name.lower():
                    author_dict["orcid"] = v
        # add orcid from OJS XML (if present) for entries with no explicitly set ORCID via CLI arg
        orcid_node = author.find(".//{http://pkp.sfu.ca}orcid")
        if (orcid_node is not None) and (author_dict["orcid"] is None):
            if orcid_node.text is not None:
                author_dict["orcid"] = orcid_node.text.split(r"/")[-1]
        # add name
        author_dict["name"] = full_name
        # find and add email
        email_node = author.find(".//{http://pkp.sfu.ca}email")
        assert email_node is not None, "Email node not found"
        email = email_node.text if email_node.text is not None else "NO_EMAIL_FOUND"
        author_dict["email"] = email
        # find affiliations
        aff_str: str = ""
        affiliations = author.findall(".//{http://pkp.sfu.ca}affiliation")
        if affiliations is not None:
            for idx, aff in enumerate(author.findall(".//{http://pkp.sfu.ca}affiliation")):
                # try to split on ;
                if aff.text is not None:
                    aff_list = aff.text.split(";")
                    aff_list = [aff.strip() for aff in aff_list if aff.strip() != ""]
                    for aff_ in aff_list:
                        author_dict["affiliation"].append({"organization": aff_})
        
        ## create author hdf string and short name

        #### first we need to create two abbreviated versions of name (part. if given name has multiple parts)
        given_name_parsed_light: str = parse_given_name(given_name, abbr_style="light")
        given_name_parsed_full: str = parse_given_name(given_name, abbr_style="full")

        #### layout for "middle" author (in case authors > 2)
        if auth_index > 0 and auth_index < len(authors_node)-1:
            data_dict["name-hdr"] += ", " + SingleQuotedString(given_name_parsed_light + " " + family_name)
            data_dict["author-meta"] += ", " + SingleQuotedString(given_name_parsed_light + " " + family_name)
            data_dict["name-short"] += ", " + SingleQuotedString(family_name + ", " + given_name_parsed_full)
            data_dict["name-long"] += ", " + SingleQuotedString(given_name + " " + family_name)
        #### layout for "last" author (in case authors > 2)
        elif auth_index > 0 and auth_index == len(authors_node)-1 and auth_index != 1:
            data_dict["name-hdr"] += ", and " + SingleQuotedString(given_name_parsed_light + " " + family_name)
            data_dict["author-meta"] += ", " + SingleQuotedString(given_name_parsed_light + " " + family_name)
            data_dict["name-short"] += ", & " + SingleQuotedString(family_name + ", " + given_name_parsed_full)
            data_dict["name-long"] += ", and " + SingleQuotedString(given_name + " " + family_name)
        #### layout second author of exactly two authors
        elif auth_index == 1 and auth_index == len(authors_node)-1:
            data_dict["name-hdr"] += " and " + SingleQuotedString(given_name_parsed_light + " " + family_name)
            data_dict["author-meta"] += ", " + SingleQuotedString(given_name_parsed_light + " " + family_name)
            data_dict["name-short"] += ", & " + SingleQuotedString(family_name + ", " + given_name_parsed_full)
            data_dict["name-long"] += ", and " + SingleQuotedString(given_name + " " + family_name)
        #### layout for first or only one author
        else:
            data_dict["name-hdr"] = SingleQuotedString(given_name_parsed_light + " " + family_name)
            data_dict["author-meta"] = SingleQuotedString(given_name_parsed_light + " " + family_name)
            data_dict["name-short"] = SingleQuotedString(family_name + ", " + given_name_parsed_full)
            data_dict["name-long"] = SingleQuotedString(family_name + ", " + given_name)

        ### add author information to data_dict
        data_dict["author"].append(author_dict)

        # increment auth idx
        auth_index += 1

        
    #### Create LaTeX for all authors in author dicts
    latex_author = create_latex_string(data_dict["author"])
    data_dict["authorstex"] = LiteralString(latex_author)

    ##### PARSE SPECIAL ISSUE STRING
    if special_issue is not None:
        data_dict["specialissue"] = LiteralString(special_issue)  

    ### Save YAML metadata
    with open("yaml_output/metadata.yaml", "w", encoding="utf-8") as f:
        yaml.dump(data_dict, f, allow_unicode=True, default_flow_style=False, explicit_start=True, explicit_end=True, default_style="")

if __name__ == "__main__":
    # Parse arguments
    xml_file_path, year, volume, orcid, special_issue = parse_arguments()
    # Run main program
    main(xml_file_path, year, volume, orcid, special_issue)

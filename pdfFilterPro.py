# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 10:43:05 2023

@author: chcuk
"""

import os
from PyPDF2 import PdfReader
import shutil
import configparser
import re


def readConfig(configFile="pdfFilter.ini"):
    config = {}
    cfg = configparser.ConfigParser(inline_comment_prefixes="#", allow_no_value=True)
    cfg.read(configFile)

    config["IFP"] = cfg.get("Config", "InputFolderPath")
    config["OFP"] = cfg.get("Config", "OutputFolderPath")
    config["Key"] = cfg.get("Config", "Keyword")
    return config

def parse_keywords(keywords_string):
    keywords = [set(kw.strip().lower().split('+')) for kw in keywords_string.split(';')]
    return keywords

def check_keywords(text, keywords):
    text_words = set(text.lower().split())
    for keyword_set in keywords:
        if keyword_set.issubset(text_words):
            keyword_string = str(keyword_set)[1:-1].replace(',', '+').replace('\'', '').replace('+', ' + ')
            print(f"'{keyword_string}' found")
            return True
    return False

config = readConfig()

input_directory = config['IFP']
output_directory = config['OFP']
keywords = parse_keywords(config['Key'])

print("Starting Process")

# Loop through the PDF files in the input directory
for filename in os.listdir(input_directory):
    if filename.endswith('.pdf'):
        file_path = os.path.join(input_directory, filename)
        
        print(f"Reading {filename}")
        # Open the PDF file
        with open(file_path, 'rb') as pdf_file:
            # Create a PdfReader object
            pdf_reader = PdfReader(pdf_file)
            
            # Extract text from the first 4 pages only
            text = " ".join([pdf_reader.pages[i].extract_text() for i in range(min(4, len(pdf_reader.pages)))])
            
            # Attempt to find the abstract
            abstract_start_pattern = re.compile('a[^a-z]*b[^a-z]*s[^a-z]*t[^a-z]*r[^a-z]*a[^a-z]*c[^a-z]*t', re.IGNORECASE)
            match = abstract_start_pattern.search(text)
            if match:
                abstract_start = text[:match.start()].count(' ')
                abstract = " ".join(text.lower().split()[abstract_start:abstract_start+500])
                # Check the keywords in the abstract
                if check_keywords(abstract, keywords):
                    # Copy the file to the output directory
                    output_path = os.path.join(output_directory, filename)
                    shutil.copyfile(file_path, output_path)
                    print(f"File '{filename}' copied.")
            else:
                print(f"Abstract not found in {filename}")
                abstract = ""
            
            
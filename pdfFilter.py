# -*- coding: utf-8 -*-
"""
Created on Mon May 22 14:21:19 2023

@author: chcuk
"""

import os
from PyPDF2 import PdfReader
import shutil
import configparser


def readConfig(configFile="pdfFilter.ini"):
    """
    Parameters
    ----------
    configFile : file
        configFile is config file name with extension.

    Returns
    -------
    config : dict
    """
    config = {}
    cfg = configparser.ConfigParser(inline_comment_prefixes="#", allow_no_value=True)
    cfg.read(configFile)

    config["IFP"] = cfg.get("Config", "InputFolderPath")
    config["OFP"] = cfg.get("Config", "OutputFolderPath")
    config["Key"] = cfg.get("Config", "Keyword")
    config["CC"] = cfg.getint("Config", "CharacterCount")
    return config

config = readConfig()

input_directory = config['IFP']
output_directory = config['OFP']
keyword = config['Key'].strip().lower()
characterCount = config['CC']

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
            
            # Get the first page
            first_page = pdf_reader.pages[0]
            
            # Extract text from the first page
            text = first_page.extract_text()
            
            # Check if the word 'integrity' is in the title
            if keyword in text.lower()[:characterCount]:
                # Copy the file to the output directory
                output_path = os.path.join(output_directory, filename)
                shutil.copyfile(file_path, output_path)
                print(f"File '{filename}' copied.")
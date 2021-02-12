# L5X-Parsing
Script to help parse L5X files

This might need some manual working to get your output just right. This is more of a scratch project, but has worked well. This will be refined the next time I need it. Pull requests welcome.

## Overview

This script is to process L5X files to gather information from the IO trees of the plc files.

## Requirements

- python3 (3.9)
- anytree
- pyyaml
- xml


## Usage

- Place your .L5X files in ./input
- Run the parser `python3.9 ./IOTreeParser.py`
- This will output directly to the console, modify the code to output how you need it.
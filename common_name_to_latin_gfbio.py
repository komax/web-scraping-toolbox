#!/usr/bin/env python

import argparse
import csv
import re

import requests
import json

def set_up_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('inputfile', help="input file containing common names of species")
    parser.add_argument("-o", "--output", help="output file containing latin names of species")
    return parser

def read_common_names_from_csv(file_name):
    common_names = list()
    with open(file_name, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in csvreader:
            common_names.append(*row)
    return common_names

def normalize_common_name(common_name):
    words = re.split("[- ]", common_name)
    return " ".join((word.lower() for word in words))


def common_name_to_latin_name(common_name):
    gfbio_url = 'https://terminologies.gfbio.org/api/terminologies/search'
    #query = normalize_common_name(common_name)
    parameters = {
        'query':common_name,
        'internal_only':'true'
    }
    response = requests.get(gfbio_url, params=parameters)
    results = response.json()['results']
    if results:
        first_result = results[0]
        latin_name = first_result['label']
        return latin_name
    else:
        return None


def write_names_as_csv(outfile_name, common_names):
    with open(outfile_name, 'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        csvwriter.writerow(["Common name", "Latin name"])
        for common_name in common_names:
            latin_name = common_name_to_latin_name(common_name)
            #print((common_name, latin_name))
            if latin_name:
                entry = latin_name
            else:
                entry = "NA"
            csvwriter.writerow([common_name, entry])
    return


def main():
    parser = set_up_argparser()
    args = parser.parse_args()
    
    # Read files
    common_names = read_common_names_from_csv(args.inputfile)

    # Dump results.
    write_names_as_csv(args.output, common_names)


if __name__ == "__main__":
    main()
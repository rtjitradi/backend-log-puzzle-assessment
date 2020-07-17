#!/usr/bin/env python2
"""
Log Puzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Given an Apache logfile, find the puzzle URLs and download the images.

Here's what a puzzle URL looks like (spread out onto multiple lines):
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg
HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US;
rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""

__author__ = "Reggy Tjitradi guided by Stew with support from Ramon and Ruth"


import os
import re
import sys
import urllib.request
import argparse
from collections import defaultdict
# https://docs.python.org/3/library/collections.html#collections.defaultdict


def read_urls(filename):
    """Returns a list of the puzzle URLs from the given log file,
    extracting the hostname from the filename itself, sorting
    alphabetically in increasing order, and screening out duplicates.
    """

    #  https://www.youtube.com/watch?v=Nn2KQmVF5Og&feature=emb_logo
    #  We need a dictionary lists to use the key and value
    #  so import collections and use defaultdict
    list_of_puzzle = []
    puzzle = defaultdict(list)
    pattern = r"\S*\Spuzzle\S*"
    temp = filename.split("_")
    address = "HTTP://" + temp[1]
    with open(filename)as f:
        for line in f:
            url_found = re.search(pattern, line)
            if url_found:
                puzzle[line[url_found.start():url_found.end()]]
                # https://docs.python.org/3/library/re.html#re.match.start
    for key in puzzle.keys():
        list_of_puzzle.append(address + key)
    if temp[0] == "animal":
        return sorted(list_of_puzzle)
    else:
        return sorted(list_of_puzzle, key=lambda x: x.split("-")[4])


def html_tag(tag):
    def wrap_text(file, msg):
        with open(file, "a") as f:
            f.write('<{0} src="{1}" />'.format(tag, msg))
    return wrap_text


def download_images(img_urls, dest_dir):
    """Given the URLs already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory with an <img> tag
    to show each local image file.
    Creates the directory if necessary.
    """

    # https://docs.python.org/3/library/os.html
    img_count = 0
    try:
        os.mkdir(dest_dir)
    except OSError as err:
        print(err)
        exit(1)
    img_tag = html_tag("img")
    for url in img_urls:
        img_filename = os.path.join(dest_dir, "img" + str(img_count) + ".jpg")
        urllib.request.urlretrieve(url, img_filename)
        img_tag("index.html", img_filename)
        img_count += 1


def create_parser():
    """Creates an argument parser object."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--todir',
                        help='destination directory for downloaded images')
    parser.add_argument('logfile', help='apache logfile to extract urls from')

    return parser


def main(args):
    """Parses args, scans for URLs, gets images from URLs."""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    img_urls = read_urls(parsed_args.logfile)

    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main(sys.argv[1:])

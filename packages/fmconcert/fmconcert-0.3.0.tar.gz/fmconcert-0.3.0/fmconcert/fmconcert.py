#!/usr/bin/env python

"""Download France Musique concert file by scrapping on broadcast webpage"""

# For python2/python3 compatibility
from __future__ import print_function
try:
    from urllib.request import urlretrieve, urlopen
except ImportError:
    from urllib import urlretrieve, urlopen

import argparse
from bs4 import BeautifulSoup
import progressbar


def query_yes_no(question, default="no"):
    """
    (From https://gist.github.com/hrouault/1358474)
    Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    # For python2/python3 compatibility
    try:
        get_input = raw_input
    except NameError:
        get_input = input

    while True:
        print(question + prompt)
        choice = get_input().lower()
        if default and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            print("Please respond with 'yes' or 'no' (or 'y' or 'n').\n")



def get_file_info(page_url):
    """Parse page_url to return name and url of the mp3 file to download"""
    page = urlopen(page_url)
    soup = BeautifulSoup(page.read(), "html.parser")
    try:
        cover = soup.find('div', class_="cover-diffusion-main-info-replay-button")
        player = cover.find('button', class_='replay-button playable')
    except AttributeError:
        cover = soup.find('div', class_="content-body")
        player = cover.find('button', class_='media-button media-button-audio playable')

    # page slug is used as file name
    diffusion_path = player['data-diffusion-path']
    file_name = diffusion_path.split('/')[-1] + '.mp3'
    file_url = player['data-url']
    return file_name, file_url


class MyProgressBar():
    """A progress bar for downloading"""
    def __init__(self):
        self.pbar = None

    def __call__(self, block_num, block_size, total_size):
        if not self.pbar:
            self.pbar=progressbar.ProgressBar(maxval=total_size)
            self.pbar.start()

        downloaded = block_num * block_size
        if downloaded < total_size:
            self.pbar.update(downloaded)
        else:
            self.pbar.finish()


def main(page_url):
    file_name, file_url = get_file_info(page_url)

    question = "Download {}\nto {}\n?".format(file_url, file_name)
    if query_yes_no(question, default="yes"):
        urlretrieve(file_url, file_name, MyProgressBar())
        print(file_name, "downloaded.")
    else:
        exit("Aborting.")


def parse_cl_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Download file from "France Musique" broadcast page')
    parser.add_argument("url", help="Broadcast page URL")
    args = parser.parse_args()
    return args.url


if __name__ == '__main__':
    main(parse_cl_args())

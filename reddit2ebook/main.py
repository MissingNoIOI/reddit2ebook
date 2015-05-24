__author__ = 'gerrit'
import sys

import praw
import pypandoc
import warnings
import os
from yaml import load
from pyprind import ProgBar

def main():
    check_argv()
    initfile = sys.argv[1]
    directory = sys.argv[2]

    # Check if the directory has a trailing slash
    if os.name == 'nt' or os.name == 'os2':
            if directory.split('\\')[-1] != '':
                directory += '\\'
    else:
            if directory.split('/')[-1] != '':
                directory += '/'

    # Disable warnings due to a bug in praw
    warnings.filterwarnings("ignore")

    reader = praw.Reddit(user_agent="reddit2ebook")
    config = read_init_file(initfile)

    for bookname in config.keys():
        text = "\n\n\n\n\n" + "#" + bookname + "\n\n\n\n\n" + "-----------------" + "\n\n\n\n\n"
        print("Downloading markdown")
        bar = ProgBar(len(config[bookname]))
        for url in config[bookname]:
            bar.update()
            # Check if the link is a comment or a submission
            # Submissions have a trailing slash
            if url.split('/')[-1] == '':
                text += get_submission_text(reader, url)
            else:
                text += get_comment_text(reader, url)

        create_ebook(text, directory, bookname)


def check_argv():
    '''
    Check if there are enough arguments, otherwise print the help
    :return:
    '''
    # TODO: Use real command line parser
    if len(sys.argv) != 3:
        print('''
        Usage:

            reddit2ebook initfile output_directory

        For the structure of the initfile please refer to https://github.com/MissingNoIOI/reddit2ebook
        ''')
        sys.exit(0)


def read_init_file(initfile):
    '''
    Load the initfile using YAML
    :param initfile:
    :return:
    '''
    with open(initfile, 'r') as file:
        config = load(file)
    return config


def get_comment_text(reader, url):
    submission = reader.get_submission(url)
    comment = submission.comments[0]
    text = "##" + "Comment by user " + comment.author.name + "\n\n" + comment.body + "\n\n\n\n" + "-----------------" + "\n\n\n\n\n"
    return text


def get_submission_text(reader, url):
    submission = reader.get_submission(url)
    text = "##" + submission.title + "\n\n" + submission.selftext + "\n\n\n\n" + "-----------------" + "\n\n\n\n\n"
    return text


def create_ebook(markdown_string, directory, ebook_name):
    # TODO: Get extra_args to work so that i can include Metadata, Cover Image and Stylesheet
    print("\nCreating ebook, please wait")
    pypandoc.convert(markdown_string,
                     'epub',
                     format="md",
                     outputfile=directory + ebook_name + '.epub')
    print("\nSuccessfully created ebook at " + directory + ebook_name + ".epub\n")


if __name__ == "__main__":
    main()

__author__ = 'gerrit'
import sys

import praw
import pypandoc
import warnings
from yaml import load


def main():
    get_initfile()
    initfile = sys.argv[1]
    directory = sys.argv[2]
    if directory.split('/')[-1] != '':
        directory = directory + '/'
    warnings.filterwarnings("ignore")
    reader = praw.Reddit(user_agent="reddit2ebook")
    config = read_init_file(initfile)
    for key in config.keys():
        text = "\n\n\n\n\n" + "#" + key + "\n\n\n\n\n" + "-----------------" + "\n\n\n\n\n"
        for url in config[key]:
            if url.split('/')[-1] == '':
                text = text + get_submission_text(reader, url)
            else:
                text = text + get_comment_text(reader, url)

        create_ebook(text, directory, key)


def get_initfile():
    if len(sys.argv) != 3:
        print('''
        Usage:

            reddit2ebook initfile output_directory

        For the structure of the initfile please refer to https://github.com/MissingNoIOI/reddit2ebook
        ''')
        sys.exit(0)


def read_init_file(initfile):
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
    pypandoc.convert(markdown_string, 'epub', format="md", outputfile=directory + ebook_name + '.epub')
    print("\nSuccessfully created ebook at " + directory + ebook_name + ".epub\n")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import sys
import praw
import warnings
import argparse
from yaml import load
from pyprind import ProgBar
import mistune
# TODO: Rewrite it for ebooklib since pypub doesnt support python3
import pypub


def main():
    parser = argparse.ArgumentParser(
        description="Create epubs from Reddit")
    parser.add_argument('config_file',
                        help="The file containing the links, formatted in YAML")
    parser.add_argument('output_directory')
    args = parser.parse_args()

    config_file = args.configfile
    directory = args.output_directory

    # Disable warnings due to a bug in praw
    warnings.filterwarnings("ignore")

    reader = praw.Reddit(user_agent="reddit2ebook")
    config = read_config_file(config_file)
    renderer = mistune.Renderer(use_xhtml=True, escape=True)
    markdown = mistune.Markdown(renderer=renderer)

    for bookname in config.keys():
        epub = pypub.Epub(bookname)
        print("Creating ebook")
        bar = ProgBar(len(config[bookname]))
        for url in config[bookname]:
            bar.update()
            # Check if the link is a comment or a submission
            # Submissions have a trailing slash
            if url.split('/')[-1] == '':
                submission = get_submission_text(reader, url)
                chapter = pypub.create_chapter_from_string(
                    markdown(submission[1]),
                    title=submission[0]
                )
            else:
                comment = get_comment_text(reader, url)
                chapter = pypub.create_chapter_from_string(
                    markdown(comment[1]),
                    title="Comment by " + comment[0]
                )

            epub.add_chapter(chapter)

        epub.create_epub(directory, epub_name=bookname)


def read_config_file(config_file):
    '''
    Load the config_file using YAML
    :param config_file:
    :return:
    '''
    try:
        with open(config_file, 'r') as file:
            config = load(file)
    except OSError:
        print("Config file not found")
        sys.exit(0)

    return config


def get_comment_text(reader, url):
    submission = reader.get_submission(url)
    comment = submission.comments[0]
    name = comment.author.name
    text = comment.body
    return (name, text)


def get_submission_text(reader, url):
    submission = reader.get_submission(url)
    title = submission.title
    text = submission.selftext
    return (title, text)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import sys
import praw
import warnings
import argparse
import os
from yaml import load
from pyprind import ProgBar
import mistune
import uuid
from ebooklib import epub


def main():
    parser = argparse.ArgumentParser(
        description="Create epubs from Reddit")
    parser.add_argument('config_file',
                        help="The file containing the links, formatted in YAML")
    parser.add_argument('output_directory')
    args = parser.parse_args()

    config_file = args.config_file
    directory = args.output_directory

    # Disable warnings due to a bug in praw
    warnings.filterwarnings("ignore")

    reader = praw.Reddit(user_agent="reddit2ebook")
    config = read_config_file(config_file)
    renderer = mistune.Renderer(use_xhtml=True, escape=True)
    markdown = mistune.Markdown(renderer=renderer)

    for bookname in config.keys():
        print("Creating ebook")
        bar = ProgBar(len(config[bookname]))

        book = epub.EpubBook()
        # The epub standard requires an unique identifier, this is normally
        # the ISBN, but since we dont have one we generate an UUID
        book.set_identifier(uuid.uuid4().hex)
        # TODO: Find a nice way to specify the language
        book.set_language('en')
        book.set_title(bookname)

        chapter_number = 1
        chapters = []

        for url in config[bookname]:
            bar.update()
            # Check if the link is a comment or a submission
            # Submissions have a trailing slash
            if url.split('/')[-1] == '':
                submission = get_submission_text(reader, url)
                chapter = create_chapter(
                    body=markdown(submission[1]),
                    title=submission[0],
                    filename="chapter" + str(chapter_number) + ".xhtml"
                )
            else:
                comment = get_comment_text(reader, url)
                chapter = create_chapter(
                    body=markdown(comment[1]),
                    title="Comment by " + comment[0],
                    filename="chapter" + str(chapter_number) + ".xhtml"
                )

            chapters.append(chapter)

            book.add_item(chapter)

            chapter_number += 1

        book.toc = chapters
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())

        style = load_css()
        default_css = epub.EpubItem(
            uid="style_default",
            file_name="style/default.css",
            media_type="text/css",
            content=style)
        book.add_item(default_css)

        nav_css = epub.EpubItem(
            uid="style_nav",
            file_name="style/nav.css",
            media_type="text/css",
            content=style)
        book.add_item(nav_css)

        spine = ['nav'] + chapters

        book.spine = spine

        epub.write_epub(os.path.join(directory, bookname + ".epub"), book, {})


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


def create_chapter(title, body, filename):
    chapter = epub.EpubHtml(title=title, file_name=filename)
    chapter.content = body
    return chapter


def load_css():
    with open("base.css", 'r') as f:
        style = f.read()
    return style

if __name__ == "__main__":
    main()

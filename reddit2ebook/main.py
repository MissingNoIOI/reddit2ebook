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
from .ebooklib_patched import epub
from PIL import Image
from pkg_resources import resource_string


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
    # We have to use xhtml here for Epubs
    renderer = mistune.Renderer(use_xhtml=True, escape=True)
    markdown = mistune.Markdown(renderer=renderer)

    for bookname in config.keys():
        book = epub.EpubBook()
        # The epub standard requires an unique identifier, this is normally
        # the ISBN, but since we dont have one we generate an UUID
        book.set_identifier(uuid.uuid4().hex)

        chapter_number = 1
        chapters = []

        if "links" in config[bookname]:
            bar = ProgBar(
                len(config[bookname]["links"]),
                title="Creating ebook " + bookname + ".epub",
                bar_char='█')

            links = config[bookname]["links"]

            if "cover" in config[bookname]:
                convert_to_jpeg(config[bookname]["cover"])
                with open("cover.jpg", 'rb') as f:
                    book.set_cover("cover.jpg", f.read())
                os.remove("cover.jpg")

            if "author" in config[bookname]:
                book.add_author(config[bookname]["author"])

            if "lang" in config[bookname]:
                book.set_language(config[bookname]["lang"])
            else:
                book.set_language('en')

            if "title" in config[bookname]:
                book.set_title(config[bookname]["title"])
            else:
                book.set_title(bookname)

        else:
            links = config[bookname]
            book.set_language('en')
            book.set_title(bookname)
            bar = ProgBar(len(config[bookname]),
                          title="Creating ebook " + bookname + ".epub",
                          bar_char='█')

        for url in links:
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

        spine = ['cover', 'nav'] + chapters

        book.spine = spine

        epub.write_epub(os.path.join(directory, bookname + ".epub"), book, {})

        print("Finished writing " + bookname + ".epub\n")


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
    # Currently uses the Epub CSS starter kit as a sane default
    # https://github.com/mattharrison/epub-css-starter-kit/
    style = resource_string(__name__, 'base.css')
    return style


def convert_to_jpeg(file_name):
    im = Image.open(file_name)
    im.save('cover.jpg')

if __name__ == "__main__":
    main()

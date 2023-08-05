# -*- coding: utf-8 -*-
import os
import argparse
import xml.etree.ElementTree
import time
import datetime

import dateutil
import dateutil.parser
import jinja2
from bs4 import BeautifulSoup
from logzero import logger


def clean_title(title):
    return (
        title.replace("'", "")
        .replace('"', "")
        .replace("?", "")
        .replace("’", "")
        .replace("/", "")
        .replace(",", "")
        .replace(".", "")
        .replace(" ", "_")
    )


def clean_content(content):
    soup = BeautifulSoup(content, features="html.parser")
    return soup.get_text().replace("\n", "\n\n")


def created_format(tm):
    utc_offset_sec = time.altzone if time.localtime().tm_isdst else time.timezone
    utc_offset = datetime.timedelta(seconds=-utc_offset_sec)
    return (
        tm.replace(microsecond=0)
        .replace(tzinfo=datetime.timezone(offset=utc_offset))
        .isoformat()
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("enex_file", help="path to enex file")
    parser.add_argument("-z", "--zim", help="path to Zim Notebook")
    args = parser.parse_args()

    logger.info("Importing %s into %s", args.enex_file, args.zim)
    notes = []

    enex = xml.etree.ElementTree.parse(args.enex_file).getroot()
    for note in enex.findall("note"):
        title = note.find("title").text
        content = note.find("content").text
        created = dateutil.parser.parse(note.find("created").text)
        tags = []
        for tag in note.findall("tag"):
            tags.append(tag.text)
        logger.info("Found %s (%s)", title, created)
        notes.append((title, created, tags, content))

    if not notes:
        logger.info("Nothing found, bye")
        return

    logger.info("Loading jinja2...")
    jinja2_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(
            os.path.join(os.path.dirname(__file__), "templates")
        )
    )
    zim_template = jinja2_env.get_template("zim.template")

    if not os.path.exists("%s.txt" % args.zim):
        logger.info("Creating root note %s.txt", args.zim)
        root_note = zim_template.render(
            title=os.path.basename(args.zim),
            created=created_format(datetime.datetime.now()),
            content="Imported from Evernote.",
        )
        with open("%s.txt" % args.zim, "w") as note_file:
            note_file.write(root_note)
    if not os.path.isdir(args.zim):
        logger.info("Creating root directory %s", args.zim)
        os.makedirs(args.zim)

    for title, created, tags, content in notes:
        logger.info("Creating %s...", title)
        zim_note = zim_template.render(
            title=title,
            created=created_format(created),
            content=clean_content(content),
            tags=", ".join(tags),
        )
        with open("%s/%s.txt" % (args.zim, clean_title(title)), "w") as note_file:
            note_file.write(zim_note)

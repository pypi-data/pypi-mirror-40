#!/usr/bin/python
# encoding = utf-8
"""
Generate the HTML for the #ITPE master post.

Usage:
  itpe_generator.py --input <INPUT> [--output <OUTPUT>] [--width=<width>]
  itpe_generator.py (-h | --help)
  itpe_generator.py --version

Options:
  -h --help        Show this screen.
  --input          CSV file containing the ITPE data.
  --output         HTML file for writing the generated HTML.
  --width=<width>  Width of the cover art in px [default: 500px].

"""

import collections
import os
import re

import csv23

from .jinja_helpers import get_jinja2_template


# Headings for the CSV fields. These don't have to exactly match the spelling/
# spacing of the CSV, but the order should be the same. We define a set of
# heading names here so that we have consistent names to use in the script
HEADINGS = [
    'from_user',
    'for_user',
    'cover_art',
    'cover_artist',
    'editor',
    'title',
    'title_link',
    'authors',
    'fandom',
    'pairing',
    'warnings',
    'length',
    'mp3_link',
    'podbook_link',
    'podbook_compiler',
]

Podfic = collections.namedtuple('Podfic', HEADINGS)


def csv_reader(path):
    with csv23.open_reader(path, encoding="utf-8") as reader:
        # Skip the first row, which only contains headings.
        next(reader)

        for row in reader:
            yield row


def get_podfics_from_rows(rows):
    for idx, r in enumerate(rows):
        try:
            yield Podfic(*r)
        except TypeError:
            raise ValueError("Row %d has the wrong number of entries" % idx)


def get_podfics(input_file):
    """Read a CSV file and return a list of Podfic instances."""
    podfics = []

    rows = csv_reader(input_file)

    for idx, podfic in enumerate(get_podfics_from_rows(rows)):
        print("Reading row %d..." % idx)
        podfics.append(podfic)

    return podfics


def generate_html(all_podfics, width):
    template = get_jinja2_template()
    for podfic in all_podfics:
        yield template.render(podfic=podfic, width=width)


def main():

    from docopt import docopt
    arguments = docopt(__doc__, version="ITPE 2019.1")

    # Strip everything except the digits from the width option, then append
    # 'px' for the CSS attribute
    arguments['--width'] = re.sub(r'[^0-9]', '', arguments['--width']) + "px"

    # If the caller doesn't give us an output path, guess one based on the
    # input file
    if arguments['<OUTPUT>'] is None:
        basepath, _ = os.path.splitext(arguments['<INPUT>'])
        arguments['<OUTPUT>'] = basepath + '.html'

    # Get a list of podfics from the input CSV file
    all_podfics = get_podfics(arguments['<INPUT>'])

    # Turn those podfics into HTML
    podfic_html = generate_html(
        all_podfics=all_podfics,
        width=arguments['--width']
    )

    # Write the output HTML, with a <br /> between items to add space
    # in the rendered page.
    html_to_write = u'\n<br />\n'.join(podfic_html)
    html_bytes = html_to_write.encode("utf8")
    with open(arguments['<OUTPUT>'], "wb") as outfile:
        outfile.write(html_bytes)

    print("HTML has been written to %s." % arguments['<OUTPUT>'])


if __name__ == "__main__":  # pragma: no cover
    main()

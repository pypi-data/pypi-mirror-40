# -*- encoding: utf-8

from jinja2 import Environment, PackageLoader

from .dreamwidth import render_user_links


def condense_into_single_line(text):
    """
    Remove all the newlines from a block of text, compressing multiple
    lines of HTML onto a single line.  Used as a Jinja2 filter.
    """
    lines = [line.lstrip() for line in text.split('\n')]
    return ''.join(lines)


def get_jinja2_template():
    """Set up the Jinja2 environment."""
    env = Environment(
        loader=PackageLoader('itpe', 'templates'),
        trim_blocks=True
    )

    env.filters['condense'] = condense_into_single_line
    env.filters['userlinks'] = render_user_links

    template = env.get_template('podfic_template.html')

    return template

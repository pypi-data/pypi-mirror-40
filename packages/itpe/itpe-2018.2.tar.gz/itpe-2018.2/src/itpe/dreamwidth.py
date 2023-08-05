#!/usr/bin/env python
"""
If you want to link to another user on Dreamwidth, you can use a
<user> tag, which gets annotated with a small icon to show that
it's another Dreamwidth account:

    <user name=amplificathon>

You can also specify a site attribute with a variety of services, which
add service-appropriate icons:

    <user name=itpe_mod site=twitter.com>

See the Dreamwidth FAQs: http://www.dreamwidth.org/support/faqbrowse?faqid=87

The ITPE template uses a compact syntax, prefixing a username with an
abbreviation and a slash, e.g. "tum/staff" or "tw/support".

This file contains a function for turning these templae strings into
the full <user> tags.
"""

from jinja2 import Template
import termcolor


SITE_PREFIXES = {
    'ao3':  'archiveofourown.org',
    'blog': 'blogspot.com',
    'dj':   'deadjournal.com',
    'del':  'delicious.com',
    'dev':  'deviantart.com',
    'dw':   'dreamwidth.org',
    'da':   'da',
    'etsy': 'etsy.com',
    'ff':   'fanfiction.net',
    'ink':  'inksome.com',
    'ij':   'insanejournal.com',
    'jf':   'journalfen.com',
    'last': 'last.fm',
    'lj':   'livejournal.com',
    'pin':  'pinboard.in',
    'pk':   'plurk.com',
    'rvl':  'ravelry.com',
    'tw':   'twitter.com',
    'tum':  'tumblr.com',
    'wp':   'wordpress.com'
}

USERLINK = Template("<user name={{ name }}{% if site and "
                    "site != 'dreamwidth.org' %} site={{ site }}{% endif %}>")

SPECIAL_CASE_NAMES = [
    '(various)',
    'anonymous'
]


def warn(message):
    termcolor.cprint(message, color='yellow')


def _single_user_link(user_str):
    """Renders a short username string into an HTML <user> link."""

    if not user_str.strip():
        warn("Skipping empty user string.")
        return ''

    # If there's a space in the user string, then we drop through a raw
    # string (e.g. "the podfic community")
    if (' ' in user_str) or (user_str.lower() in SPECIAL_CASE_NAMES):
        warn("Skipping user string '%s'" % user_str)
        return user_str

    # If there aren't any slashes, then treat it as a Dreamwidth user
    if '/' not in user_str:
        warn("No site specified for '%s'; assuming Dreamwidth" % user_str)
        return USERLINK.render(name=user_str)

    # If there's one slash, split the string and work out the site name.
    # Throws a ValueError if there's more than one slash.
    try:
        short_site, name = user_str.split('/')
    except ValueError:
        raise ValueError("Invalid user string '%s'" % user_str)

    try:
        site = SITE_PREFIXES[short_site]
    except KeyError:
        raise ValueError("Invalid site prefix in string '%s'" % user_str)

    # If it's a Dreamwidth user, we don't need to specify the site attribute
    return USERLINK.render(name=name, site=site)


def render_user_links(name_str):
    """
    Takes a string of names, possibly separated with commas or ampersands,
    and returns an appropriate string of <user> tags.
    """
    if '&' in name_str:
        components = (render_user_links(part.strip())
                      for part in name_str.split('&'))
        return ' & '.join(c for c in components if c)
    else:
        components = (_single_user_link(name.strip())
                      for name in name_str.split(','))
        return ', '.join(c for c in components if c)

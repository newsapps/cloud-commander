"""
Misc utilities
"""
import re
import sys
import time
import string
import random
import unicodedata


def random_string(length=6):
    """
    Generate a random string of letters and numbers
    """
    return ''.join(random.choice(string.letters + string.digits) for i in xrange(length))


def draw_ascii_spinner(delay=0.2):
    for char in '/-\|': # there should be a backslash in here.
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
        sys.stdout.write('\r') # this should be backslash r.

def require_input(prompt):
    i = None
    while not i:
        i = raw_input(prompt.strip()+' ')
        if not i:
            print '  I need this, please.'
    return i


_slugify_strip_re = re.compile(r'[^\w\s-]')
_slugify_hyphenate_re = re.compile(r'[-\s]+')
def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    
    From Django's "django/template/defaultfilters.py".
    """
    if not isinstance(value, unicode):
        value = unicode(value)
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(_slugify_strip_re.sub('', value).strip().lower())
    return _slugify_hyphenate_re.sub('-', value)


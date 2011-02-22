# -*- coding: utf-8 -*-
def get_version():
    """
    Get the Cloud Commander version number
    """
    import pkg_resources
    d = pkg_resources.get_distribution('cloud_commander')
    return unicode(d._version)

RECIPES_REPO = 'https://github.com/newsapps/cloud-commander-recipes.git'

# These constants are used to generate the config.yml for a project.

# Tree for picking images. Feel free to change, but be careful.
IMAGES = {
    "us-east-1": {
        "ubuntu": {
            '10.10': {
                '64bit': 'ami-548c783d',
                '32bit': 'ami-508c7839',
            },
            '10.04': {
                '64bit': 'ami-4a0df923',
                '32bit': 'ami-480df921',
            },
        },
    },
    'us-west-1': {
        'ubuntu': {
            '10.10': {
                '64bit': 'ami-ca1f4f8f',
                '32bit': 'ami-c81f4f8d',
            },
            '10.04': {
                '64bit': 'ami-880c5ccd',
                '32bit': 'ami-8c0c5cc9',
            },
        }
    }
}

# Shortcut names for instance sizes. Because I can never remember 
# what those prefixes are.
SIZES = {
    'micro':   't1.micro',
    'small':   'm1.small',
    'medium':  'c1.medium',
    'large':   'm1.large',
    'xl':      'm1.xlarge',
    'xlcpu':   'c1.xlarge',
    'xlmem':   'm2.xlarge',
    '2xl':     'm2.2xlarge',
    '3xl':     'm2.3xlarge',
}

# Which instances support which architectures
ARCHS = {
    '64bit': ['micro', 'large', 'xl', 'xlcpu', 'xlmem', '2xl', '3xl'],
    '32bit': ['micro', 'small', 'medium', 'large', 'xl', 'xlcpu', 'xlmem', '2xl', '3xl'],
}

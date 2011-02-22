from setuptools import setup, find_packages

setup(
    name    = "Cloud Commander",
    version = "1.0alpha1",

    packages = find_packages(),
    entry_points = {
        'console_scripts': [
            'cloud-commander = cloud_commander.command:execute_from_command_line',
        ],
    },
    install_requires = ["Jinja2>=2.5.5",
                        "PyYAML>=3.09",
                        "boto>=2.0b3",
                        "argparse>=1.1",
                       ],

    # project info
    author       = "Ryan Mark",
    author_email = "ryan@mrk.cc",
    description  = "Write recipes to bootstrap servers in the cloud.",
    long_description = open('README.rst', 'rt').read(),
    url          = "http://github.com/ryanmark/cloud-commander",
    license      = "MIT",
    keywords     = ['Development Status :: 3 - Alpha',
                   'Environment :: Console',
                   'Intended Audience :: System Administrators',
                   'License :: OSI Approved :: MIT License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Utilities',
                   'Topic :: Internet',
                   'Topic :: System :: Installation/Setup',
                   'Topic :: System :: Systems Administration',
                   ],
)


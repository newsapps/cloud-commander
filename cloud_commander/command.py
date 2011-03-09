# -*- coding: utf-8 -*-

import os
import yaml
import argparse
from cloud_commander.misc import random_string
from cloud_commander.recipes import make_recipe
from cloud_commander.config import setup_project

def execute_from_command_line():
    # Parse options
    commands_description = """To make a recipe, use "%(prog)s start RECIPE_NAME". 
                              I'll look in your 'recipes/'. To setup %(prog)s for the 
                              first time, use "%(prog)s setup PROJECT_NAME". I'll create
                              a new project in directory PROJECT_NAME."""
    
    parser = argparse.ArgumentParser(usage="%(prog)s [options] start|setup RECIPE|PROJECT_NAME",
                                     description=commands_description)
    parser.add_argument("-k", "--access-key", dest="access_key",
                        help="Your AWS access key")
    parser.add_argument("-s", "--secret-key", dest="secret_key",
                        help="Your AWS secret key")
    parser.add_argument("-b", "--asset-bucket", dest="asset_bucket",
                        help="S3 bucket that I can use for temp storage")
    parser.add_argument("-r", "--region", dest="region",
                        help="EC2 region")
    parser.add_argument("-z", "--zone", dest="zone",
                        help="EC2 zone")
    parser.add_argument("-p", "--key-pair", dest="key_pair",
                        help="EC2 key pair")
    parser.add_argument("-g", "--security-group", dest="security_group",
                        help="EC2 security group")
    parser.add_argument("command", choices=('setup', 'start'),
                        help="Action for %(prog)s to take: start a recipe or setup a project.")
    parser.add_argument("command_arg", metavar="RECIPE|PROJECT_NAME",
                        help="")
    
    args = parser.parse_args()
    
    if args.command not in ('setup', 'start'):
        parser.error(commands_description)
    
    # Setup cloud commander, if asked
    if args.command == 'setup':
        setup_project(args.command_arg)
        exit()
    
    # Load settings from this project's config.yml and command line args.
    # Command line args overwrite stuff from config.yml
    settings = yaml.load(open('config.yml'))
    for key in args.__dict__.keys():
        if args.__dict__[key]:
            settings[key] = args.__dict__[key]
    
    # Make sure we have enough settings.
    num_settings = 7
    if len(settings) < num_settings + 3:
        parser.error("Missing some required settings. Please use the setup command.")
    
    # Some useful runtime settings
    settings['cc_key'] = "cc-deploy_%s" % random_string()
    settings['assets_s3_url'] = "s3://%s/" % settings['asset_bucket']
    
    # Some useful globals that don't need to end up in the template context
    settings['assets_dir'] = os.path.abspath('assets')
    settings['templates_dir'] = os.path.abspath('boot-scripts')
    
    # fire up a server
    if args.command == 'start' and args.command_arg:
        settings['recipe_name'] = args.command_arg
        make_recipe(settings)
    else:
        parser.error("Please provide a recipe name")


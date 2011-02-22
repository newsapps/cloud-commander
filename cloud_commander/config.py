"""
Cloud commander config
"""
import os
from subprocess import call
import yaml

from cloud_commander import RECIPES_REPO,IMAGES,SIZES,ARCHS
from cloud_commander.misc import require_input

def setup_project(project_name):
    """
    Generate a project directory. Use git to retrieve recipes, then prompt 
    for the configuration options and generate the config file.
    """
    config = {}

    print 'Cloud Commander setup'
    print '====================='
    print ''

    print 'Downloading recipes...'
    call('git clone %s %s' % (RECIPES_REPO, project_name), shell=True)
    print ''

    print 'EC2 configuration'
    print '-----------------'
    print ''
    config['access_key'] = require_input('Your AWS access key:')
    config[ 'secret_key' ] = require_input('Your AWS secret key:')
    config[ 'asset_bucket' ] = require_input('S3 bucket that I can use for temp storage:')
    print ''
    print 'Defaults for launching instances'
    print '--------------------------------'
    config[ 'region' ] = require_input('Region:')
    config[ 'zone' ] = require_input('Zone:')
    config[ 'key_pair' ] = require_input('Key pair:')
    config[ 'security_group' ] = require_input('Security group:')
    print ''

    config_filename = os.path.join(project_name, 'config.yml')
    config_file = open(config_filename, 'w')
    config_file.write('# config.yml\n')
    config_file.write('#\n')
    config_file.write('# EC2 settings\n')
    config_file.write(yaml.dump(config, default_flow_style=False))
    config_file.write('\n')
    config_file.write('# Any key/value defined here is accessible in the templates through\n')
    config_file.write('# the settings variable.\n')
    config_file.write('# e.x.:\n')
    config_file.write('# foo: "bar"\n')
    config_file.write('\n')

    config_file.write('# Tree for picking images. Feel free to change, but be careful.\n')
    config_file.write(yaml.dump({'images': IMAGES}))
    config_file.write('\n')

    config_file.write('# Shortcut names for instance sizes. Because I can never remember\n')
    config_file.write('# what those prefixes are.\n')
    config_file.write(yaml.dump({'sizes':  SIZES}))
    config_file.write('\n')

    config_file.write('# Which instances support which architectures\n')
    config_file.write(yaml.dump({'archs': ARCHS}))

    config_file.close()

    print 'All set up!'
    print 'Configuration is saved in %s' % config_filename
    print ''
    print 'Run "cloud-commander start RECIPE" from %s to get started.' % project_name
    print 'To update your recipes, run "git pull origin master" from %s.' % project_name
    print 'Place your key pair private key at "%s/assets/%s.pem" if you would like it deployed.' % (project_name, config['key_pair'])

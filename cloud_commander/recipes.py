import os
import sys
import yaml
import boto
import boto.ec2
from assets import push_assets
from misc import draw_ascii_spinner, slugify
from assets import remove_assets, open_s3
from jinja2 import Environment, FileSystemLoader


def make_recipe(settings):
    """
    make_recipe
    Fire up a new instance based on a recipe file
    """
    # Load the recipe
    recipe_name = settings['recipe_name']
    if not os.path.exists('recipes/%s.yml' % recipe_name):
        raise Exception('Recipe %s not found' % recipe_name)
    recipe = yaml.load(open('recipes/%s.yml' % recipe_name))
    
    # Push everything up to S3
    push_assets(settings)
    
    print 'Connecting to EC2...'
    # Set the region
    ec2_region = boto.ec2.get_region(
        settings['region'],
        aws_access_key_id=settings['access_key'],
        aws_secret_access_key=settings['secret_key']
    )
    # Make the connection
    ec2_connection = boto.connect_ec2(
        settings['access_key'],
        settings['secret_key'],
        region=ec2_region,
    )
    
    # See how many servers we need for this recipe
    if type(recipe['server']) == type(list()):
        servers = recipe['server']
    else:
        servers = [recipe['server'],]

    # Setup template directory
    env = Environment(loader=FileSystemLoader(settings['templates_dir']))

    reservations = list()
    for server in servers:
        settings['server'] = server

        # Generating bootscript from templates
        boot_script = env.get_template(settings['server']['script'])
        user_data = boot_script.render(settings=settings, server=settings['server'])
    
        # Load ami info
        ami = AMI(settings)

        # Run server
        print 'Starting instance %s...' % server.get('name', server.get('type', ""))
        reservations.append((server, ec2_connection.run_instances(
            image_id=ami.id,
            key_name=settings['key_pair'],
            user_data=user_data,
            security_groups=[server.get('security_group', settings['security_group'])],
            instance_type=ami.size,
        )))
        
    # First setup our status flag and EC2 tags
    for server, reservation in reservations:
        for instance in reservation.instances:
            
            # Set status flag
            set_status(settings, instance.id)

            # Add tags to instance
            instance.add_tag('Name', server.get('name', 'untitled'))
            instance.add_tag('Hosts', server.get('hosts', ''))
            instance.add_tag('Type', server.get('type', recipe_name))
            instance.add_tag('OS', ami.os)
            instance.add_tag('Version', ami.version)
            instance.add_tag('Arch', ami.arch)
            instance.add_tag('Cluster', server.get('cluster', ''))
            
    
    # Monitor the booting servers, let the user know when they're running
    for server, reservation in reservations:
        for instance in reservation.instances:
            
            # Wait for the instance to come up
            while instance.state != 'running':
                draw_ascii_spinner(1)
                instance.update()
            sys.stdout.write('\r')
            
            print 'Server %s is booting. It will be available in a few minutes.' % instance.id

    # Now let us know when they finish
    for server, reservation in reservations:
        for instance in reservation.instances:
            
            # Check cloud commander status
            while check_status(settings, instance.id):
                draw_ascii_spinner(1)
            sys.stdout.write('\r')

            print '%s is at attention.' % server['name']
            print '  ssh -l USERNAME %s' % instance.public_dns_name

    # cleanup
    remove_assets(settings)


class AMI(object):
    """
    An Amazon EC2 AMI image.
    """
    
    def __init__(self, settings):
        # Fill in all the vars
        d =  settings['server']
        self.os = d['os']
        self.version = d['version']
        self.arch = d['arch']
        self.region = settings['region']
        self.size = settings['sizes'][d['size']]
        self.id = settings['images'][self.region][self.os][self.version][self.arch]
        
        # Validate that the size and arch can play nice
        if not d['size'] in settings['archs'][d['arch']]:
            print "The %s instance doesn't support %sbit" % (self.size, self.arch)
            exit()

def set_status(settings, instance_id):
    """
    Set a instance build status semaphore in s3
    """
    # Get s3 bucket & key
    bucket, key = open_s3(settings, settings['asset_bucket'], 
                          "%s._cc_" % instance_id)

    # set plain text headers
    headers = {'Content-Type':'text/plain'}

    try:
        key.set_contents_from_string('running', headers, replace=True)
    except boto.s3.connection.S3CreateError, e:
        print "Failed: %s" % e
    except Exception, e:
        print e
        raise

def check_status(settings, instance_id):
    """
    Check the build status semaphore for an instance
    """
    # Get s3 bucket & key
    bucket, key = open_s3(settings, settings['asset_bucket'], 
                          "%s._cc_" % instance_id)

    if key.exists() and key.get_contents_as_string() == 'running':
        return True
    else: return False



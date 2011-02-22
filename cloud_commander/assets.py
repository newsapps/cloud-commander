"""
Asset upload and deletion
# from http://django-command-extensions.googlecode.com/svn/trunk/django_extensions/management/commands/sync_media_s3.py
"""
import boto
import subprocess

def push_assets(settings):
    """
    Push the assets directory to s3
    """
    print "Stashing assets folder someplace safe..."
    process=subprocess.Popen("tar -c -z -s/assets/cloud-commander/ assets", 
                             shell=True, executable='/bin/bash',
                             stdout=subprocess.PIPE)

    tarball, err = process.communicate()

    bucket, key = open_s3(settings, settings['asset_bucket'], "%s-assets.tgz" % settings['cc_key'])
    key.set_contents_from_string(tarball)

def open_s3(settings, bucket_name, key_name):
    """
    Open a connection to S3 and return a bucket and a key
    """
    conn = boto.connect_s3(settings['access_key'], settings['secret_key'])
    bucket = conn.get_bucket(bucket_name)
    key = boto.s3.key.Key(bucket, key_name)
    return bucket, key

def remove_assets(settings):
    """
    Remove the temporary assets dir from the S3 bucket
    """
    print "Clearing assets..."
    bucket, key = open_s3(settings, settings['asset_bucket'], settings['cc_key']+"-assets.tgz")
    key.delete()


Cloud Commander
===============

Scripts and scripts you can use to quickly launch and build ec2 instances.

The goal of this thing is to allow you to replace the specialized public AMI with a script that configures a vanilla OS installation for a specific service or task. The benefit is that a script is agnostic to the service provider.

Currently Cloud Commander only supports Amazon's cloud, but the techniques should work for any provider. However, one script can configure servers in any region on Amazon's cloud, which makes it a hell of a lot more useful than a public AMI. It also allows you to launch and configure a fleet of specialized instances at the push of a button.

Installation
------------

To begin, you will need git, python and python setuptools.

You can install Cloud Commander from pypi with <code>easy_install</code> or <code>pip</code>. Or you can download the source and install it by hand. I would recommend installing to a virtualenv, although it's totally optional.

<pre><code>
$ easy_install cloud_commander
</code></pre>
or
<pre><code>
$ pip install cloud_commander
</code></pre>
or
<pre><code>
$ git clone https://github.com/ryanmark/cloud-commander.git
$ cd cloud-commander
$ python setup.py install
</code></pre>

Setup
-----

Alright, you've got the commander installed now lets get started.

Create a new project directory somewhere:

<pre><code>
$ cd ~
$ cloud-commander setup my_servers
</code></pre>

The commander will pull a directory structure full of recipes from a central git repository and prompt you for various bits of information it needs to interact with Amazon web services.

You're all ready to launch some servers!

A couple other things related to configuration:

Recipes will look for a private key in your <code>my_servers/assets</code> directory. It looks for a file named *.pem, where * is the case-sensitive name of your key pair. Recipes will also look for <code>known_hosts</code> and <code>authorized_keys</code> files in the assets directory. If found, the contents of these files will be added to the new instances. 

Launching servers
-----------------

Switch to your project directory:

<pre><code>
$ cd my_servers
$ cloud-commander start newsapps-kitchensink
</code></pre>

That's all there is to it! Whatever instances are called for in the newsapps-kitchensink recipe will be started and configured.

Run-down of the project directory
---------------------------------

* assets/
  The contents of this folder will be pushed to S3 and pulled down on every instance that is launched. The contents of bin subdirectory will be installed in /usr/local/bin on the instance. The contents of known_hosts and authorized_keys will be added to the primary user's ~/.ssh directory, along with the the private key used to launch the instance (only if you add it to the assets directory).
* boot-scripts/
  Contains shell scripts that get passed to the instance at boot. These scripts are run as root and do all the work of configuring the instances. Cloud commander uses the Jinja2 template library to generate the final script. So you can use any of the Jinja2 template syntax in the bootscripts.
* recipes/
  Where all of the recipes are defined. A recipe is a YAML file with a 'server' array. 
* config.yml
  Where all your EC2 and Cloud Commander project configuration is stored. Also contains the list of AMIs that will be used by your recipes.

Contributing
------------

If you've written a recipe and bootscripts that you would like to share, simply fork ryanmark/cloud-commander-recipes on github, commit your project directory to your fork, and send me a pull request. Exactly like homebrew, if you're familiar.

Contributors
------------

Ryan Mark <ryan@mrk.cc>, Chicago Tribune
Ben Welsh, LA Times

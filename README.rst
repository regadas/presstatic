presstatic
----------

by Filipe Regadas (`@regadas <http://twitter.com/regadas>`_)

This is a little CLI utility that helps deploying static websites to Amazon S3.

Usage
-----

.. code-block:: shell

	$> pip install presstatic

	$> pstatic -h

	usage: presstatic [-h] [-http HOST:PORT] [-s3 bucket] directory

	positional arguments:
		directory        directory containing the static website.

	optional arguments:
		-h, --help       show this help message and exit
		-http HOST:PORT  creates an HTTP Server with <directory> as root dir.
		-s3 bucket       deploy on the specified S3 bucket.
  		
* upload your website:

.. code-block:: shell

	$> export AWS_ACCESS_KEY_ID=<Your Key id>

	$> export AWS_SECRET_ACCESS_KEY=<Your Secret>

	$> pstatic -s3 example.com ~/projects/example.com
  	
* preview your website while you develop it:

	Any change in files/directories will trigger the builder. Because of this and other reasons this http server is intended for development only.

.. code-block:: shell
	
	$> pstatic -http ~/projects/example.com


Templates
---------

We use the awesome `Jinja <http://jinja.pocoo.org/>`_ template engine.

Assets
------

We are using `webassets <https://github.com/miracle2k/webassets>`_ for asset bundling.

If you intend to use assets you need to add a configuration file (YAML) to your root project.
Please see the webassets docs to see for more details.

Here's an example:

.. code-block:: yaml

	url: /static
	debug: True
	bundles:
	    all_css:
	        filters: yui_css
	        output: static/css/packed.css
	        contents:
	            - static/css/style.css
	            - static/css/jquery.fancybox.css
	    all_js:
	        filters: yui_js
	        output: static/js/packed.js
	        contents:
	            - static/js/jquery-latest.min.js
	            - static/js/jquery.fancybox.pack.js
	            - static/js/app.js

TODO
----

* Add Template support [DRAFT]
* Add Asset support [DRAFT]
* Add watcher support [DRAFT]

License
_______

presstatic is under MIT license. See the `LICENSE <https://github.com/regadas/presstatic/blob/master/LICENSE>`_ file for details.


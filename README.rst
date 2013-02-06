presstatic
----------

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
  	
* serve your website: (the provided http server is intended for development only)

.. code-block:: shell
	
	$> pstatic -http ~/projects/example.com

TODO
----

* Add Template support
* Add Asset support
* Add watcher support 
* Upload only modified files [DONE]

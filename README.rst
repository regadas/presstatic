presstatic
----------

This is a little CLI utility that helps deploying static websites to Amazon S3.

Usage
-----

	$> pip install presstatic

	$> pstatic -h

	usage: presstatic [-h] [-http HOST:PORT] [-s3 bucket] directory
  		
* upload your website:

	$> pstatic -s3 example.com ~/projects/example.com
  	
* serve your website: (the provided http server is intended for development only)
	
	$> pstatic -http ~/projects/example.com

TODO
----

* Add Template support
* Add Asset support
* Add watcher support 
* Upload only modified files [DONE]

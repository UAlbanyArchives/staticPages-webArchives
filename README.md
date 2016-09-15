# staticPages-webArchives
Python scripts to generate static navigation pages from collection list and insert Web Archives records using the Archive-It CDX

There are three scripts here:


basicSample.py
--------------
+ A sample example script for making requests from the Archive-It CDX

+ by default this requests http://www.albany.edu/history/course-descriptions.shtml from the www.albany.edu Archive-it collection 3308

To look for a different URL just change Line 3 that begins with "requestURL = ":

	import requests
	
	requestURL = "http://wayback.archive-it.org/3308/timemap/cdx?url=http://www.albany.edu/history/course-descriptions.shtml"
	

Set `requestURL` as `http://wayback.archive-it.org/[Collection#]/timemap/cdx?url=[URL]` with your own URL and collection number.

CDX.py
------
+ A basic command line script for getting the number of captures and a date range from Archive-It URLS

Run in the command line as: `python CDX.py`

+ You will be prompted for a URL and an Archive-It collection number

staticPages.py
--------------
+ An example of the script we are using to make static pages while updating Web Archives records from the Archive-It and Wayback CDX API

[Wayback CDX API Documentation](https://github.com/internetarchive/wayback/tree/master/wayback-cdx-server)
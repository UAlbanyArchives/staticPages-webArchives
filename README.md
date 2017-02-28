# UWM Web Archives EAD update code

This is, as shown below, a fork of the University of Albany's code to generate subject and collection pages for their web archives collections. (My infinite gratitude to Greg for sharing this code with the community via the Archive-It blog.)

Since I am basically an amateur at this, I have eliminated the sections of code that make updates to HTML and am focusing on updates to EAD only.

Other major changes from the original (other than localization changes):
+ The Web Archives series is written to c02 rather than c01 because of the way we describe our unprocessed accessions.

+ Added additional information about the Archive-It harvester to the Phystech notes, and modified code to append to existing phystech notes if present

+ Added code to generate a scope/content note, pulling from a field in the CollectionsList spreadsheet.

+ Added code to generate a Revision Description change note whenever the script is run. (For right now this also lets me track how many times I have to run the code before I get it right!)



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
+ collectionList.xslx is also included as a sample of the spreadsheet we are used to provide the data for this script

[Wayback CDX API Documentation](https://github.com/internetarchive/wayback/tree/master/wayback-cdx-server)

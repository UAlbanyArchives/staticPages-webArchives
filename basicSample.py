import requests

requestURL = "http://wayback.archive-it.org/3308/timemap/cdx?url=http://www.albany.edu/history/course-descriptions.shtml"

response = requests.get("http://wayback.archive-it.org/3308/timemap/cdx?url=http://www.albany.edu/history/course-descriptions.shtml")
responseText  = response.text

#variable to count number of captures:
aiCount = 0
#if lenght of HTTP response is greater than 5, aribitrary value to check for any captures
if len(responseText) < 5:
	print "ERROR: no captures found for "
	
	responseLines = responseText.split("\n")
	firstPage = responseLines[0]
	for textLine in responseLines:
		aiCount = aiCount + 1
		if len(textLine) > 5:
			lastPage = textLine
	#get date range of captures
	firstDate = firstPage.split(" ")[1][:8]
	lastDate = lastPage.split(" ")[1][:8]
	
print str(aiCount) + " captures"
print "from " + firstDate + " to " + lastDate
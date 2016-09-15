import requests

webUrl = raw_input("What URL would you like to look for?")
archiveItCollection = raw_input("Which Archive-it collection would you like to look in?: ")

if len(archiveItCollection) < 1:
	archiveItCollection = "3308"
if len(webUrl) < 1:
	webUrl = "http://www.albany.edu/history/course-descriptions.shtml"
elif not webUrl.lower().startswith("http://"):
	webUrl = "http://" + webUrl


#Function to make DACS and Normal (ISO) dates from CDX timestamp
def makeDate(stamp):
	calendar = {"01": "January", "02": "February", "03": "March", "04": "April", "05": "May", "06": "June", "07": "July", "08": "August", "09": "September", "10": "October", "11": "November", "12": "December"}
	year = stamp[:4]
	month = stamp[4:6]
	day = stamp[-2:]
	normal = year + "-" + month + "-" + day
	if day.startswith("0"):
		day = day[-1:]
	dacs = year + " " + calendar[month] + " " + day
	return dacs, normal

requestURL = "http://wayback.archive-it.org/" + archiveItCollection + "/timemap/cdx?url=" + webUrl

print "Asking Archive it for captures of " + webUrl
response = requests.get(requestURL)
responseText  = response.text

#variable to count number of captures:
aiCount = 0
#if lenght of HTTP response is greater than 5, aribitrary value to check for any captures
if len(responseText) < 5:
	print "ERROR: no captures found for " + webUrl + " in Archive-it collection " + archiveItCollection
else:
	responseLines = responseText.split("\n")
	firstPage = responseLines[0]
	for textLine in responseLines:
		aiCount = aiCount + 1
		if len(textLine) > 5:
			lastPage = textLine
	#get date range of captures
	firstDate = firstPage.split(" ")[1][:8]
	lastDate = lastPage.split(" ")[1][:8]
	
	
	dateRange = [firstDate, lastDate]
	seriesMax = max(dateRange)
	seriesMin = min(dateRange)
	seriesMaxDacs, seriesMaxNormal = makeDate(seriesMax)
	seriesMinDacs, seriesMinNormal = makeDate(seriesMin)
	seriesDacs = seriesMinDacs + "-" + seriesMaxDacs
	seriesNormal = seriesMinNormal + "/" + seriesMaxNormal
	
	print "Found " + str(aiCount) + " captures"
	print "DACS date range: " + seriesDacs
	print "Normal (ISO) date range: " + seriesNormal
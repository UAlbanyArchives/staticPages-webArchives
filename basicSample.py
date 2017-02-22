import requests

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

requestURL = "http://wayback.archive-it.org/3368/timemap/cdx?url=http://www.uwm.edu/arts/"

response = requests.get(requestURL)
responseText  = response.text

#variable to count number of captures:
aiCount = 0
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

dateRange = [firstDate, lastDate]
seriesMax = max(dateRange)
seriesMin = min(dateRange)
seriesMaxDacs, seriesMaxNormal = makeDate(seriesMax)
seriesMinDacs, seriesMinNormal = makeDate(seriesMin)
seriesDacs = seriesMinDacs + "-" + seriesMaxDacs
seriesNormal = seriesMinNormal + "/" + seriesMaxNormal
print "DACS date range: " + seriesDacs
print "Normal (ISO) date range: " + seriesNormal

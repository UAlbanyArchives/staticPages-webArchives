# -*- coding: utf-8 -*-

from lxml import etree as ET
from openpyxl import load_workbook
from operator import itemgetter
import os
import copy
import requests


#lxml parser for parsing XML files from strings
parser = ET.XMLParser(remove_blank_text=True)

if os.name == "nt":
	#Windows Directory Names
	
	#Finding Aid Directory
	faDir = "g:\WebArch"
	#Collection and Subject spreadsheets directory
	spreadDir = "C:\Users\houstobn\Documents\GitHub\staticPages-webArchives"
	#static pages directory on public webserver
	staticDir = "C:\Users\houstobn\Documents\Test"
	

#parse Collection List spreadsheet
collectionListFile = os.path.join(spreadDir, "collectionList.xlsx")
collectionWorkbook = load_workbook(filename = collectionListFile, use_iterators=True, read_only=True)
collectionList = collectionWorkbook.get_sheet_by_name('collectionList')

		
def makeLink(collection, pageContent):
	if collection[3] == "ead":
		id = collection[1]
		title = collection[4]
		type = collection[5]
		eadFile = os.path.join(faDir, id + ".xml")
		eadInput = ET.parse(eadFile, parser)
		ead = eadInput.getroot()
		date = ead.find("archdesc/did/unittitle/unitdate").text
		abstract = ead.find("archdesc/did/abstract").text
		link = "http://meg.library.albany.edu:8080/archive/view?docId=" + id + ".xml"
	elif collection[3] == "html":
		id = collection[1]
		title = collection[4]
		type = collection[5]
		date = collection[6]
		link = "http://library.albany.edu/speccoll/findaids/" + id + ".htm"
	elif collection[3] == "null":
		id = collection[1]
		title = collection[4]
		type = collection[5]
		date = collection[6]
		if id.startswith("apap"):
			link = "http://library.albany.edu/speccoll/findaids/eresources/static/apap.html#" + id
		elif id.startswith("ger"):
			link = "http://library.albany.edu/speccoll/findaids/eresources/static/ger.html#" + id
		elif id.startswith("mss"):
			link = "http://library.albany.edu/speccoll/findaids/eresources/static/mss.html#" + id
		elif id.startswith("ua"):
                        link = "http://library.albany.edu/speccoll/findaids/eresources/static/ua.html#" + id

	
	
def alphaNav(contentDiv, collection):
	leftNav = contentDiv.find("div[@class='row no-gutter']/div[@id='browseNav']/div[@class='panel panel-default']/div[@class='nav list-group']")
	alphaContent = contentDiv.find("div[@class='row no-gutter']/div[@class='col-md-9 col-md-offset-3 alphaContent']")
	letter = collection[4][:1]
	if leftNav.find("li/a[@id='link-" + letter + "']") is None:
		navLi =ET.Element("li")
		navLink = ET.Element("a")
		navLink.set("id", "link-" + letter)
		navLi.set("class", "list-group-item")
		navLink.set("href", "#" + letter)
		navLink.text = letter.upper()
		navLi.append(navLink)
		leftNav.append(navLi)
	if alphaContent.find("div[@id='" + letter + "']") is None:
		anchor = ET.Element("div")
		anchor.set("id", letter)
		anchor.set("class", "anchor")
		alphaContent.append(anchor)
	else:
		anchor = alphaContent.find("div[@id='" + letter + "']")
	if contentDiv.find("div[@title='alphaList']") is None:
		anchor = makeAbstract(collection, anchor)
	else:
		alphaContent = makeLink(collection, alphaContent)
	return contentDiv
	
#############################################################
#end functions to make compontents for static pages
#############################################################	
		
		
#Parse List of Collections to list of lists
rowIndex = 0
collections = []
for row in collectionList.rows:
	rowIndex = rowIndex + 1
	if rowIndex > 1:
		collection = [str(rowIndex), row[0].value, row[1].value, row[2].value, row[3].value, row[4].value, row[5].value, row[6].value, row[7].value, row[8].value, row[9].value, row[10].value, row[11].value]
		collections.append(collection)
	
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
						
		
		###################################################################################	
		#Web Archives Section
		###################################################################################
		
		# if collection has EAD file and a Web Archives series listed
if not collection[10] is None and str(collection[3]).lower() == "ead":
	#Archive-It CDX API request
	webUrl = str(collection[12])
	archiveItCollection = str(collection[11])
	print "looking for web archives captures for collection  " + str(collection[1])
	archiveIt = False
	wayback = False
	requestURL = "http://wayback.archive-it.org/" + archiveItCollection + "/timemap/cdx?url=" + webUrl
	#for debugging:
	#print requestURL
	response = requests.get(requestURL)
	responseText  = response.text
			
		#variable to count number of captures:
	aiCount = 0
		#if lenght of HTTP response is greater than 5, aribitrary value to check for any captures
	if len(responseText) > 5:
		archiveIt = True
		responseLines = responseText.split("\n")
		firstPage = responseLines[0]
		for textLine in responseLines:
			aiCount = aiCount + 1
			if len(textLine) > 5:
				lastPage = textLine
					#get date range of captures
		firstDate = firstPage.split(" ")[1][:8]
		lastDate = lastPage.split(" ")[1][:8]

				
				#general Wayback CDX API request
	wayRequestURL = "http://web.archive.org/cdx/search/cdx?url=" + webUrl
				#for debugging:
				#print wayRequestURL
	wayResponse = requests.get(wayRequestURL)
	wayResponseText  = wayResponse.text
	waybackCount = 0
	if len(wayResponseText) > 120:
		wayback = True
		wayResponseLines = wayResponseText.split("\n")
		wayFirstPage = wayResponseLines[0]
		for wayLine in wayResponseLines:
			if len(wayLine) > 5:
				waybackCount = waybackCount + 1
				wayLastPage = wayLine
					#get date range of captures
		wayFirstDate = wayFirstPage.split(" ")[1][:8]
		wayLastDate = wayLastPage.split(" ")[1][:8]

				#check if actually found any captures and convert to DACS and Normal (ISO) dates
	if archiveIt == False and wayback == False:
		pass
	else:
		if archiveIt == False:
						#get DACS and normal dates
			dateRange = [wayFirstDate, wayLastDate]
			seriesMax = max(dateRange)
			seriesMin = min(dateRange)
			seriesMaxDacs, seriesMaxNormal = makeDate(seriesMax)
			seriesMinDacs, seriesMinNormal = makeDate(seriesMin)
			seriesDacs = seriesMinDacs + "-" + seriesMaxDacs
			seriesNormal = seriesMinNormal + "/" + seriesMaxNormal
					
		elif wayback == False:
				#get DACS and normal dates
			dateRange = [firstDate, lastDate]
			seriesMax = max(dateRange)
			seriesMin = min(dateRange)
			seriesMaxDacs, seriesMaxNormal = makeDate(seriesMax)
			seriesMinDacs, seriesMinNormal = makeDate(seriesMin)
			seriesDacs = seriesMinDacs + "-" + seriesMaxDacs
			seriesNormal = seriesMinNormal + "/" + seriesMaxNormal
					
		else:
			dateRange = [firstDate, lastDate, wayFirstDate, wayLastDate]
			seriesMax = max(dateRange)
			seriesMin = min(dateRange)
			seriesMaxDacs, seriesMaxNormal = makeDate(seriesMax)
			seriesMinDacs, seriesMinNormal = makeDate(seriesMin)
			seriesDacs = seriesMinDacs + "-" + seriesMaxDacs
			seriesNormal = seriesMinNormal + "/" + seriesMaxNormal
				
					#Show feedback for web archvies
		print "found Web Archives for " + str(collection[1])
					
					#parse EAD file for collection
		eadFile = os.path.join(faDir, str(collection[1]) + ".xml")
		faInput = ET.parse(eadFile, parser)
		fa = faInput.getroot()
					
					#Get Web Archvies Series Semantic ID
		webArchSeries = "nam_" + str(collection[1]) + "-" + str(collection[10])
					#Add Web Archives not in <phystech>
		if fa.find("archdesc/phystech") is None:
			phystech = ET.Element("phystech")
			phystechP = ET.SubElement(phystech, "p")
			phystechP.text = "Web Archives"
			fa.find("archdesc").insert(1, phystech)
					#for debugging:
					#print "Series " + webArchSeries
					
					#find or create Web Archvies Series
		if fa.find("archdesc/dsc") is None:
			print "creating web archives series"
			dsc = ET.Element("dsc")
			fa.find("archdesc").append(dsc)
			series = ET.Element("c01")
			series.set("id", webArchSeries)
			series.set ("level", "otherlevel")
			series.set ("otherlevel", "Web")
			dsc.append(series)
		else:
			match = False
			for series in fa.find("archdesc/dsc"):
				if series.tag == "c01":
					if series.attrib["id"] == webArchSeries:
						match = True
                                        if match == False:
                                                newSeries = ET.Element("c01")
						newSeries.set("id", webArchSeries)
						fa.find("archdesc/dsc").append(newSeries)

					#iterate though EAD and find matching series
		for series in fa.find("archdesc/dsc"):
			if series.tag == "c01":
				if series.attrib["id"] == webArchSeries:
							#for debugging:
								#print "found series"
					series.set("level", "series")\
								#find or create <did>
					if series.find("did") is None:
						did = ET.Element("did")
						series.insert(0, did)
								#find or create <unitid>
					if series.find("did/unitid") is None:
						unitid = ET.Element("unitid")
						unitid.text = str(collection[10])
						series.find("did").insert(0, unitid)
								#update <unittitle>
					if series.find("did/unittitle") is None:
						unittitle = ET.Element("unittitle")
						unittitle.text = "Web Archives"
						series.find("did").insert(1, unittitle)
								#remove existing <unitdate>s
					if not series.find("did/unitdate") is None:
						series.find("did").remove(series.find("did/unitdate"))
								#Add new <unitdate>
					unitdate = ET.Element("unitdate")
					unitdate.set("type", "inclusive")
					unitdate.set("era", "ce")
					unitdate.set("calendar", "gregorian")
					unitdate.set("normal", seriesNormal)
					unitdate.text = seriesDacs
					series.find("did").insert(2, unitdate)
							#remove existing <physdesc>
					if not series.find("did/physdesc") is None:
						series.find("did").remove(series.find("did/physdesc"))
							#Add new <physdesc> with count of captures
					physdescElement = ET. Element ("physdesc")
					extentElement = ET.Element("extent")
					extentElement.text = str(aiCount + waybackCount)
					extentElement.set("unit", "captures")
					physdescElement.append(extentElement)
					series.find("did").append(physdescElement)
							#remove existing <phystech>
					if not series.find("phystech") is None:
						series.remove(series.find("phystech"))
							#add new <phystech>
					if series.find("phystech") is None:
						phystech = ET.Element("phystech")
						phystechP = ET.SubElement(phystech, "p")
						phystechP.text = "Web Archives"
						series.insert(1, phystech)
							#remove existing <acqinfo>
					if not series.find("acqinfo") is None:
						series.remove(series.find("acqinfo"))
							#add new <acqinfo>
					if series.find("acqinfo") is None:
						acqinfo = ET.Element("acqinfo")
						acqP1 = ET.SubElement(acqinfo, "p")
						acqP2 = ET.SubElement(acqinfo, "p")
								#default <acqinfo> text
						acqP1.text = "Web crawling is managed through the Internet Archive's Archive-It service. This page includes links to both the university's collection and the Internet Archive's public collection."
								#Albany.edu <acqinfo> text
						if archiveItCollection == "3368":
							acqP2.text = "All UWM websites are crawled on a semi-annual basis. Additional crawls may be performed on an as-needed basis to account for collections processing, major website changes, etc."
						series.insert(1, acqinfo)
								
								#remove existing web archives links
					
								#add general Wayback <c02>
						if wayback == True:
							idCount = idCount + 1
							wayFile = ET.Element("c02")
							wayFile.set("id", webArchSeries + "_" + str(idCount))
							wayDid = ET.SubElement(wayFile, "did")
							wayContainer = ET.SubElement(wayDid, "container")
							wayContainer.set("type", "Web-Archive")
							wayContainer.text = "2"
							wayUnittitle = ET.SubElement(wayDid, "unittitle")
							wayUnittitle.text = webUrl + " - Internet Archive collection"
							wayUnitdate = ET.SubElement(wayDid, "unitdate")
							wayUnitdate.set("calendar", "gregorian")
							wayUnitdate.set("era", "ce")
							firstDacs, firstNormal = makeDate(wayFirstDate)
							lastDacs, lastNormal = makeDate(wayLastDate)
							wayUnitdate.set("normal", firstNormal + "/" + lastNormal)
							wayUnitdate.text = firstDacs + "-" + lastDacs
							wayDao = ET.SubElement(wayDid, "dao")
							wayDao.set("actuate", "onrequest")
							wayDao.set("linktype", "simple")
							wayDao.set("show", "new")
							wayDao.set("href", "https://web.archive.org/web/*/" + webUrl)
							series.append(wayFile)
					
					#remove existing Web Archives access headings
			
									
                faString = ET.tostring(fa, pretty_print=True, xml_declaration=True, encoding="utf-8")
                faFile = open(eadFile, "w")
                faFile.write(faString)
                faFile.close()
       
		###################################################################################	
		#End Web Archives Section
		###################################################################################


				



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
	faDir = "\\\\romeo\\Collect\\spe\\Greg\\EAD_Validator"
	#Collection and Subject spreadsheets directory
	spreadDir = "\\\\romeo\\Collect\spe\\Tools\\CollectionList"
	#static pages directory on public webserver
	staticDir = "\\\\romeo\\wwwroot\\eresources\\static"
else:
	#Unix directory names
	
	#Finding Aid Directory
	faDir = "/media/bcadmin/Collect/spe/Greg/EAD_Validator"
	#Collection and Subject spreadsheets directory
	spreadDir = "/media/bcadmin/Collect/spe/Tools/CollectionList"
	#static pages directory on public webserver
	staticDir = "/media/bcadmin/wwwroot/eresources/static"
	

#parse Collection List spreadsheet
collectionListFile = os.path.join(spreadDir, "collectionList.xlsx")
collectionWorkbook = load_workbook(filename = collectionListFile, use_iterators=True, read_only=True)
collectionList = collectionWorkbook.get_sheet_by_name('collectionList')

#parse Local Subject Lists spreadsheet
subjectGuidesFile =  os.path.join(spreadDir, "subjectGuides.xlsx")
subjectWorkbook = load_workbook(filename = subjectGuidesFile, use_iterators=True, read_only=True)
subjectGuides = subjectWorkbook.get_sheet_by_name('subjectGuides')

#load basic HTML template file
templateFile = os.path.join(staticDir, "templates", "template.html")
tempateInput = ET.parse(templateFile, parser)
tempate = tempateInput.getroot()

#add additional JS file for fixed header
affixHead = ET.Element("script")
affixHead.set("type", "text/javascript")
affixHead.set("src", "http://library.albany.edu/speccoll/findaids/eresources/static/js/headerAffix.js")
tempate.find("head").append(affixHead)



#############################################################
#load and parse specific templates for each static page
alpha = copy.copy(tempate)
alpha.find("head/title").text = "A-Z Complete List of Collections"
alphaContent = alpha.find("body/div[@id='mainContent']")
alphaTemplateFile = os.path.join(staticDir, "templates", "browseAlpha.xml")
alphaTempateInput = ET.parse(alphaTemplateFile, parser)
alphaTempate = alphaTempateInput.getroot()
alphaContent.append(alphaTempate)

apap = copy.copy(tempate)
apap.find("head/title").text = "New York State Modern Political Archive"
apapContent = apap.find("body/div[@id='mainContent']")
apapTemplateFile = os.path.join(staticDir, "templates", "browseAPAP.xml")
apapTempateInput = ET.parse(apapTemplateFile, parser)
apapTempate = apapTempateInput.getroot()
apapContent.append(apapTempate)

ger = copy.copy(tempate)
ger.find("head/title").text = u"German and Jewish Intellectual Émigré"
gerContent = ger.find("body/div[@id='mainContent']")
gerTemplateFile = os.path.join(staticDir, "templates", "browseGER.xml")
gerTempateInput = ET.parse(gerTemplateFile, parser)
gerTempate = gerTempateInput.getroot()
gerContent.append(gerTempate)

mss = copy.copy(tempate)
mss.find("head/title").text = u"Business, Literary, and Miscellaneous Manuscripts"
mssContent = mss.find("body/div[@id='mainContent']")
mssTemplateFile = os.path.join(staticDir, "templates", "browseMSS.xml")
mssTempateInput = ET.parse(mssTemplateFile, parser)
mssTempate = mssTempateInput.getroot()
mssContent.append(mssTempate)

ua = copy.copy(tempate)
ua.find("head/title").text = u"University Archives"
uaContent = ua.find("body/div[@id='mainContent']")
uaTemplateFile = os.path.join(staticDir, "templates", "browseUA.xml")
uaTempateInput = ET.parse(uaTemplateFile, parser)
uaTempate = uaTempateInput.getroot()
uaContent.append(uaTempate)

subjects = copy.copy(tempate)
subjects.find("head/title").text = u"Subjects"
subjectsContent = subjects.find("body/div[@id='mainContent']")
subjectsTemplateFile = os.path.join(staticDir, "templates", "browseSubjects.xml")
subjectsTempateInput = ET.parse(subjectsTemplateFile, parser)
subjectsTempate = subjectsTempateInput.getroot()
subjectsContent.append(subjectsTempate)
#############################################################



#############################################################
#Functions to make each component of static pages
#############################################################
def makePanel(id, title, type, date, extent, units, abstract, link):
	panel = ET.Element("div")
	panel.set("class", "panel panel-default")
	panelHead = ET.Element("div")
	panelHead.set("class", "panel-heading")
	panelTitle = ET.Element("div")
	panelTitle.set("class", "panel-title pull-left")
	panelBody = ET.Element("div")
	panelBody.set("class", "panel-body")
	h3 = ET.Element("h3")
	h5 = ET.Element("h5")
	quantity = ET.Element("p")
	strong = ET.Element("strong")
	strong.text = "Quantity:"
	
	
	p = ET.Element("p")
	
	h3.text = title
	h5.text = str(type) + ", " + str(date)
	strong.tail = " " + str(extent) + " " + units + " (about " + str(extent) + " boxes)"
	p.text = abstract
	
	if len(link) > 0:
		collectionLink = ET.Element("a")
		collectionLink.set("href", link)
		collectionLink.append(panelTitle)
		panelHead.append(collectionLink)
	else:
		panelHead.append(panelTitle)
		requestButton = ET.Element("button")
		requestButton.set("class", "btn btn-primary requestModel pull-right")
		requestButton.set("id", "nam_" + id + ": " + title)
		requestButton.set("type", "button")
		requestButton.set("data-toggle", "modal")
		requestButton.set("data-target", "#requestBrowse")
		icon = ET.Element("i")
		icon.set("class", "glyphicon glyphicon-folder-close")
		panelHead.append(requestButton)
		requestButton.append(icon)
		icon.tail = " Request"
		
	clearFloat = ET.Element("div")
	clearFloat.set("style", "clear:both;")
	panelHead.append(clearFloat)
	panel.append(panelHead)
	panelTitle.append(h3)
	panelTitle.append(h5)
	quantity.append(strong)
	panelBody.append(quantity)
	panelBody.append(p)
	panel.append(panelBody)
	return panel
	

def makeAbstract(collection, pageContent):
	if collection[3] == "ead":
		id = collection[1]
		title = collection[4]
		type = collection[5]
		eadFile = os.path.join(faDir, id + ".xml")
		eadInput = ET.parse(eadFile, parser)
		ead = eadInput.getroot()
		date = ead.find("archdesc/did/unittitle/unitdate").text
		if ead.find("archdesc/did/physdesc/extent") is None:
			try:
				extent = ead.find("archdesc/did/physdesc/physfacet").text
				units = ""
			except:
				extent = ead.find("archdesc/did/physdesc/dimensions").text
				units = ead.find("archdesc/did/physdesc/dimensions").attrib["unit"]
		else:
			extent = ead.find("archdesc/did/physdesc/extent").text
			units = ead.find("archdesc/did/physdesc/extent").attrib["unit"]
		abstract = ead.find("archdesc/did/abstract").text
		link = "http://meg.library.albany.edu:8080/archive/view?docId=" + id + ".xml"
		
		panel = makePanel(id, title, type, date, extent, units, abstract, link)
		collectionAnchor = ET.Element("a")
		collectionAnchor.set("name", id)
		collectionAnchor.set("class", "anchor")
		pageContent.append(collectionAnchor)
		pageContent.append(panel)
		return pageContent
	elif collection[3] == "html":
		id = collection[1]
		title = collection[4]
		type = collection[5]
		date = collection[6]
		extent = collection[7]
		units = collection[8]
		abstract = collection[9]
		link = "http://library.albany.edu/speccoll/findaids/" + id + ".htm"
		panel = makePanel(id, title, type, date, extent, units, abstract, link)
		collectionAnchor = ET.Element("a")
		collectionAnchor.set("name", id)
		collectionAnchor.set("class", "anchor")
		pageContent.append(collectionAnchor)
		pageContent.append(panel)
		return pageContent
	elif collection[3] == "null":
		id = collection[1]
		title = collection[4]
		type = collection[5]
		date = collection[6]
		extent = collection[7]
		units = collection[8]
		abstract = collection[9]
		panel = makePanel(id, title, type, date, extent, units, abstract, "")
		collectionAnchor = ET.Element("a")
		collectionAnchor.set("name", id)
		collectionAnchor.set("class", "anchor")
		pageContent.append(collectionAnchor)
		pageContent.append(panel)
		return pageContent
	else:
		print "error with " + collection[3] + ", line " + str(rowIndex)
		return pageContent
		
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

	alphaLink = ET.Element("a")
	alphaLink.set("href", link)
	alphaLink.set("class", "alphaLink")
	alphaLink.text = str(title) + "; " + str(type) + ", " + str(date)
	pageContent.append(alphaLink)
	br = ET.Element("br")
	pageContent.append(br)
	return pageContent


	
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
					
# Iterate through each collection
sortedCollections = sorted(collections, key=itemgetter(4))
for collection in sortedCollections:
	if not collection[2] is None:
		#for non-public collections
		pass
	else:
		#sort collections in to catagories by ID prefix
		alphaContent = alphaNav(alphaContent, collection)
		if collection[1].startswith("apap"):
			apapContent = alphaNav(apapContent, collection)
		elif collection[1].startswith("ger"):
			gerContent = alphaNav(gerContent, collection)
		elif collection[1].startswith("mss"):
			mssContent = alphaNav(mssContent, collection)
		elif collection[1].startswith("ua"):
			uaContent = alphaNav(uaContent, collection)
		
		
		###################################################################################	
		#Web Archives Section
		###################################################################################
		
		# if collection has EAD file and a Web Archives series listed
		if not collection[10] is None and str(collection[3]).lower() == "ead":
		
			try:
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
									if archiveItCollection == "3308":
										acqP2.text = "Surface-level crawling of www.albany.edu is performed daily which should includes most top-level webpages. Separate targeted crawls of every albany.edu subdomain are performed monthly to attempt to gather all content. This includes: www.albany.edu, www.rna.albany.edu, www.ctg.albany.edu, www.ualbanysports.com, www.albany.edu/rockefeller, www.albany.edu/cela, www.albany.edu/asrc, m.albany.edu,	library.albany.edu,	events.albany.edu,	cstar.cestm.albany.edu, csda.albany.edu, and alumni.albany.edu"
									#NYCLU <acqinfo> text
									elif archiveItCollection == "7081":
										acqP2.text = "The following seeds are crawled monthly: www.nyclu.org, www.facebook.com/NYCLU, www.twitter.com/NYCLU, and en.wikipedia.org/wiki/New_York_Civil_Liberties_Union. The domains en.wikipedia.org, twitter.com, and upload.wikimedia.org are subjected to a 1,000 document limit."
									series.insert(1, acqinfo)
									
								#remove existing web archives links
								for oldc02 in series:
									if oldc02.tag == "c02":
										series.remove(oldc02)
								#variable to make new semantic IDs
								idCount = 0
								
								#Make Archive-it <c02>
								if archiveIt == True:
									idCount = idCount + 1
									aiFile = ET.Element("c02")
									aiFile.set("id", webArchSeries + "_" + str(idCount))
									aiDid = ET.SubElement(aiFile, "did")
									aiContainer = ET.SubElement(aiDid, "container")
									aiContainer.set("type", "Web-Archive")
									aiContainer.text = "1"
									aiUnittitle = ET.SubElement(aiDid, "unittitle")
									aiUnittitle.text = webUrl + " - University Archives collection"
									aiUnitdate = ET.SubElement(aiDid, "unitdate")
									aiUnitdate.set("calendar", "gregorian")
									aiUnitdate.set("era", "ce")
									firstDacs, firstNormal = makeDate(firstDate)
									lastDacs, lastNormal = makeDate(lastDate)
									aiUnitdate.set("normal", firstNormal + "/" + lastNormal)
									aiUnitdate.text = firstDacs + "-" + lastDacs
									aiDao = ET.SubElement(aiDid, "dao")
									aiDao.set("actuate", "onrequest")
									aiDao.set("linktype", "simple")
									aiDao.set("show", "new")
									aiDao.set("href", "http://wayback.archive-it.org/" + archiveItCollection + "/*/" + webUrl)
									series.append(aiFile)
									
									#make WARC <c02>
									idCount = idCount + 1
									warcFile = ET.Element("c02")
									warcFile.set("id", webArchSeries + "_" + str(idCount))
									warcDid = ET.SubElement(warcFile, "did")
									warcContainer = ET.SubElement(warcDid, "container")
									warcContainer.set("type", "WARC")
									warcContainer.text = "1"
									warcUnittitle = ET.SubElement(warcDid, "unittitle")
									warcUnittitle.text = "WARC file for " + webUrl + ", (please see https://en.wikipedia.org/wiki/Web_ARChive for more details)"
									warcUnitdate = ET.SubElement(warcDid, "unitdate")
									warcUnitdate.set("calendar", "gregorian")
									warcUnitdate.set("era", "ce")
									warcUnitdate.set("normal", firstNormal + "/" + lastNormal)
									warcUnitdate.text = firstDacs + "-" + lastDacs
									accessRestrict = ET.Element("accessrestrict")
									restrictP = ET.SubElement(accessRestrict, "p")
									#WARC restriction Text
									restrictP.text = "WARC files are very large and difficult to work with. Your request may take time to process, and we may be unable to deliver your request remotely. Please consult an archivist if you are interested in researching with web archives."
									warcFile.append(accessRestrict)
									series.append(warcFile)
								
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
					accessHeadCount = 0
					for heading in fa.find("archdesc/controlaccess"):
						if heading.tag == "genreform":
							if heading.attrib["source"] == "meg":
								if heading.text == "Web Archives":
									accessHeadCount = accessHeadCount + 1
					#add new Web Archives access headings
					if accessHeadCount < 1:
						genreform = ET.Element("genreform")
						genreform.text = "Web Archives"
						genreform.set("source", "meg")
						genreform.set("encodinganalog", "655")
						fa.find("archdesc/controlaccess").append(genreform)
									
					faString = ET.tostring(fa, pretty_print=True, xml_declaration=True, encoding="utf-8")
					faFile = open(eadFile, "w")
					faFile.write(faString)
					faFile.close()
			
			except:
				#for exceptions
				print "Issue with Archive-it API?"
				continue

		###################################################################################	
		#End Web Archives Section
		###################################################################################


				
###################################################
#Create Static Subject Pages
###################################################
#iterate through subjects spreadsheet
subjectRowNumber = 0
for subjectRow in subjectGuides.rows:
	subjectRowNumber = subjectRowNumber + 1
	if subjectRowNumber == 1:
		subjectIndex = 0
		for subject in subjectRow:
			leftNav = subjectsContent.find("div[@class='row no-gutter']/div[@id='browseNav']/div[@class='panel panel-default']/div[@class='nav list-group']")
			if subjectIndex == 0:
				leftNav.remove(leftNav[0])
			rightContent = subjectsContent.find("div[@class='row no-gutter']/div[@class='col-md-9 col-md-offset-3 alphaContent']")
			letter = subject.value[:1]
			subjectName = subject.value
			subjectColumn = subjectGuides.columns[subjectIndex]
			subjectIndex = subjectIndex + 1
			subjectLinkName = subjectColumn[1].value
			if leftNav.find("li/a[@id='link-" + letter + "']") is None:
				navLi =ET.Element("li")
				navLink = ET.Element("a")
				navLink.set("id", "link-" + letter)
				navLi.set("class", "list-group-item")
				navLink.set("href", "#" + letter)
				navLink.text = letter.upper()
				navLi.append(navLink)
				leftNav.append(navLi)
			if rightContent.find("div[@id='" + letter + "']") is None:
				anchor = ET.Element("div")
				anchor.set("id", letter)
				anchor.set("class", "anchor")
				rightContent.append(anchor)
			else:
				anchor = rightContent.find("div[@id='" + letter + "']")
			subjectPara = ET.Element("p")
			subjectLink = ET.Element("a")
			subjectLink.text = subjectName
			subjectLink.set("href", "http://library.albany.edu/speccoll/findaids/eresources/static/" + subjectLinkName + ".html")
			subjectPara.append(subjectLink)
			anchor.append(subjectPara)
			
			print "creating subject page for " + subjectName
			
			if subjectLinkName == "ndpa":
				page = copy.copy(tempate)
				page.find("head/title").text = u"National Death Penalty Archive"
				pageContent = page.find("body/div[@id='mainContent']")
				pageTemplateFile = os.path.join(staticDir, "templates", "browseNDPA.xml")
				pageTempateInput = ET.parse(pageTemplateFile, parser)
				pageTempate = pageTempateInput.getroot()
				pageContent.append(pageTempate)
			else:
				page = copy.copy(tempate)
				page.find("head/title").text = subjectName
				pageContent = page.find("body/div[@id='mainContent']")
				pageTemplateFile = os.path.join(staticDir, "templates", "browseSubjects.xml")
				pageTempateInput = ET.parse(pageTemplateFile, parser)
				pageTempate = pageTempateInput.getroot()
				pageTempate.find("div/div[@class='jumbotron']/h2").text = subjectName
				pageContent.append(pageTempate)
						
			print subjectName
			columnIndex = 0
			for collectionIdCell in subjectColumn:
				collectionId = collectionIdCell.value
				if not collectionId is None:
					columnIndex = columnIndex + 1
					if columnIndex > 2:
										
						for collection in sortedCollections:
							if collection[1] == collectionId:
							
								#add Local Subject Heading to EAD if missing
								#for debugging:
								#print collectionId
								eadFile = os.path.join(faDir, str(collectionId) + ".xml")
								if os.path.isfile(eadFile):
									faInput = ET.parse(eadFile, parser)
									fa = faInput.getroot()
									subjectHeadCount = 0
									if fa.find("archdesc/controlaccess") is None:
										controlaccess = ET.Element("controlaccess")
										fa.find("archdesc").insert(1, controlaccess)
									for heading in fa.find("archdesc/controlaccess"):
										if heading.tag == "subject":
											if not "source" in heading.attrib:
												pass
											elif heading.attrib["source"] == "meg":
												if heading.text == subjectName:
													subjectHeadCount = subjectHeadCount + 1
									if subjectHeadCount < 1:
										megSubject = ET.Element("subject")
										megSubject.text = subjectName
										megSubject.set("source", "meg")
										megSubject.set("encodinganalog", "650")
										fa.find("archdesc/controlaccess").insert(1, megSubject)
											
									#write Updated EAD to file
									faString = ET.tostring(fa, pretty_print=True, xml_declaration=True, encoding="utf-8")
									faFile = open(eadFile, "w")
									faFile.write(faString)
									faFile.close()
									
															
								leftNav = pageContent.find("div[@class='row no-gutter']/div[@id='browseNav']/div[@class='panel panel-default']/div[@class='nav list-group']")
								rightContent = pageContent.find("div[@class='row no-gutter']/div[@class='col-md-9 col-md-offset-3 alphaContent']")
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
								if rightContent.find("div[@id='" + letter + "']") is None:
									anchor = ET.Element("div")
									anchor.set("id", letter)
									anchor.set("class", "anchor")
									rightContent.append(anchor)
								else:
									anchor = rightContent.find("div[@id='" + letter + "']")
								
								anchor = makeAbstract(collection, anchor)
			
			#write static subject pages
			pageString = ET.tostring(page, pretty_print=True, method='html', xml_declaration=False, doctype="<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">")
			pageFile = open(os.path.join(staticDir, subjectLinkName + ".html"), "w")
			pageFile.write(pageString)
			
	
#Write static pages to web server
apapString = ET.tostring(apap, method='html', xml_declaration=False, doctype="<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">")
apapFile = open(os.path.join(staticDir, "apap.html"), "w")
apapFile.write(apapString)

gerString = ET.tostring(ger, method='html', xml_declaration=False, doctype="<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">")
gerFile = open(os.path.join(staticDir, "ger.html"), "w")
gerFile.write(gerString)

mssString = ET.tostring(mss, method='html', xml_declaration=False, doctype="<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">")
mssFile = open(os.path.join(staticDir, "mss.html"), "w")
mssFile.write(mssString)

uaString = ET.tostring(ua, method='html', xml_declaration=False, doctype="<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">")
uaFile = open(os.path.join(staticDir, "ua.html"), "w")
uaFile.write(uaString)

subjectsString = ET.tostring(subjects, method='html', xml_declaration=False, doctype="<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">")
subjectsFile = open(os.path.join(staticDir, "subjects.html"), "w")
subjectsFile.write(subjectsString)

alphaString = ET.tostring(alpha, method='html', xml_declaration=False, doctype="<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">")
alphaFile = open(os.path.join(staticDir, "alpha.html"), "w")
alphaFile.write(alphaString)
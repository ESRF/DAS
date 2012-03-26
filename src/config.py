#!/usr/bin/env python

#
# Generated Mon Mar 26 02:25::47 2012 by EDGenerateDS.
#

import os, sys
from xml.dom import minidom
from xml.dom import Node





#
# Support/utility functions.
#

# Compabiltity between Python 2 and 3:
if sys.version.startswith('3'):
	unicode = str
	from io import StringIO
else:
	from StringIO import StringIO


def showIndent(outfile, level):
	for idx in range(level):
		outfile.write(unicode('    '))


def checkType(_strClassName, _strMethodName, _value, _strExpectedType):
	if not _strExpectedType in ["float", "double", "string", "boolean", "integer"]:
		if _value != None:
			if _value.__class__.__name__ != _strExpectedType:
				strMessage = "ERROR! %s.%s argument is not %s but %s" % (_strClassName, _strMethodName, _strExpectedType, _value.__class__.__name__)
				print(strMessage)
				#raise BaseException(strMessage)
#	elif _value is None:
#		strMessage = "ERROR! %s.%s argument which should be %s is None" % (_strClassName, _strMethodName, _strExpectedType)
#		print(strMessage)
#		#raise BaseException(strMessage)


def warnEmptyAttribute(_strName, _strTypeName):
	if not _strTypeName in ["float", "double", "string", "boolean", "integer"]:
		print("Warning! Non-optional attribute %s of type %s is None!" % (_strName, _strTypeName))

class MixedContainer(object):
	# Constants for category:
	CategoryNone = 0
	CategoryText = 1
	CategorySimple = 2
	CategoryComplex = 3
	# Constants for content_type:
	TypeNone = 0
	TypeText = 1
	TypeString = 2
	TypeInteger = 3
	TypeFloat = 4
	TypeDecimal = 5
	TypeDouble = 6
	TypeBoolean = 7
	def __init__(self, category, content_type, name, value):
		self.category = category
		self.content_type = content_type
		self.name = name
		self.value = value
	def getCategory(self):
		return self.category
	def getContenttype(self, content_type):
		return self.content_type
	def getValue(self):
		return self.value
	def getName(self):
		return self.name
	def export(self, outfile, level, name):
		if self.category == MixedContainer.CategoryText:
			outfile.write(self.value)
		elif self.category == MixedContainer.CategorySimple:
			self.exportSimple(outfile, level, name)
		else:	 # category == MixedContainer.CategoryComplex
			self.value.export(outfile, level, name)
	def exportSimple(self, outfile, level, name):
		if self.content_type == MixedContainer.TypeString:
			outfile.write(unicode('<%s>%s</%s>' % (self.name, self.value, self.name)))
		elif self.content_type == MixedContainer.TypeInteger or \
				self.content_type == MixedContainer.TypeBoolean:
			outfile.write(unicode('<%s>%d</%s>' % (self.name, self.value, self.name)))
		elif self.content_type == MixedContainer.TypeFloat or \
				self.content_type == MixedContainer.TypeDecimal:
			outfile.write(unicode('<%s>%f</%s>' % (self.name, self.value, self.name)))
		elif self.content_type == MixedContainer.TypeDouble:
			outfile.write(unicode('<%s>%g</%s>' % (self.name, self.value, self.name)))

#
# Data representation classes.
#


class DASConfig(object):
	def __init__(self, Workflow=None, EDNA=None, pollingTime=None, contactEmail=None):
	
	
		checkType("DASConfig", "Constructor of DASConfig", contactEmail, "string")
		self._contactEmail = contactEmail
		checkType("DASConfig", "Constructor of DASConfig", pollingTime, "float")
		self._pollingTime = pollingTime
		checkType("DASConfig", "Constructor of DASConfig", EDNA, "Server")
		self._EDNA = EDNA
		checkType("DASConfig", "Constructor of DASConfig", Workflow, "Server")
		self._Workflow = Workflow
	def getContactEmail(self): return self._contactEmail
	def setContactEmail(self, contactEmail):
		checkType("DASConfig", "setContactEmail", contactEmail, "string")
		self._contactEmail = contactEmail
	def delContactEmail(self): self._contactEmail = None
	# Properties
	contactEmail = property(getContactEmail, setContactEmail, delContactEmail, "Property for contactEmail")
	def getPollingTime(self): return self._pollingTime
	def setPollingTime(self, pollingTime):
		checkType("DASConfig", "setPollingTime", pollingTime, "float")
		self._pollingTime = pollingTime
	def delPollingTime(self): self._pollingTime = None
	# Properties
	pollingTime = property(getPollingTime, setPollingTime, delPollingTime, "Property for pollingTime")
	def getEDNA(self): return self._EDNA
	def setEDNA(self, EDNA):
		checkType("DASConfig", "setEDNA", EDNA, "Server")
		self._EDNA = EDNA
	def delEDNA(self): self._EDNA = None
	# Properties
	EDNA = property(getEDNA, setEDNA, delEDNA, "Property for EDNA")
	def getWorkflow(self): return self._Workflow
	def setWorkflow(self, Workflow):
		checkType("DASConfig", "setWorkflow", Workflow, "Server")
		self._Workflow = Workflow
	def delWorkflow(self): self._Workflow = None
	# Properties
	Workflow = property(getWorkflow, setWorkflow, delWorkflow, "Property for Workflow")
	def export(self, outfile, level, name_='DASConfig'):
		showIndent(outfile, level)
		outfile.write(unicode('<%s>\n' % name_))
		self.exportChildren(outfile, level + 1, name_)
		showIndent(outfile, level)
		outfile.write(unicode('</%s>\n' % name_))
	def exportChildren(self, outfile, level, name_='DASConfig'):
		pass
		if self._contactEmail is not None:
			showIndent(outfile, level)
			outfile.write(unicode('<contactEmail>%s</contactEmail>\n' % self._contactEmail))
		if self._pollingTime is not None:
			showIndent(outfile, level)
			outfile.write(unicode('<pollingTime>%e</pollingTime>\n' % self._pollingTime))
		if self._EDNA is not None:
			self.EDNA.export(outfile, level, name_='EDNA')
		else:
			warnEmptyAttribute("EDNA", "Server")
		if self._Workflow is not None:
			self.Workflow.export(outfile, level, name_='Workflow')
	def build(self, node_):
		for child_ in node_.childNodes:
			nodeName_ = child_.nodeName.split(':')[-1]
			self.buildChildren(child_, nodeName_)
	def buildChildren(self, child_, nodeName_):
		if child_.nodeType == Node.ELEMENT_NODE and \
			nodeName_ == 'contactEmail':
			value_ = ''
			for text__content_ in child_.childNodes:
				if text__content_.nodeValue is not None:
					value_ += text__content_.nodeValue
			self._contactEmail = value_
		elif child_.nodeType == Node.ELEMENT_NODE and \
			nodeName_ == 'pollingTime':
			if child_.firstChild:
				sval_ = child_.firstChild.nodeValue
				try:
					fval_ = float(sval_)
				except ValueError:
					raise ValueError('requires float (or double) -- %s' % child_.toxml())
				self._pollingTime = fval_
		elif child_.nodeType == Node.ELEMENT_NODE and \
			nodeName_ == 'EDNA':
			obj_ = Server()
			obj_.build(child_)
			self.setEDNA(obj_)
		elif child_.nodeType == Node.ELEMENT_NODE and \
			nodeName_ == 'Workflow':
			obj_ = Server()
			obj_.build(child_)
			self.setWorkflow(obj_)
	#Method for marshalling an object
	def marshal( self ):
		oStreamString = StringIO()
		oStreamString.write(unicode('<?xml version="1.0" ?>\n'))
		self.export( oStreamString, 0, name_="DASConfig" )
		oStringXML = oStreamString.getvalue()
		oStreamString.close()
		return oStringXML
	#Only to export the entire XML tree to a file stream on disk
	def exportToFile( self, _outfileName ):
		outfile = open( _outfileName, "w" )
		outfile.write(unicode('<?xml version=\"1.0\" ?>\n'))
		self.export( outfile, 0, name_='DASConfig' )
		outfile.close()
	#Deprecated method, replaced by exportToFile
	def outputFile( self, _outfileName ):
		print("WARNING: Method outputFile in class DASConfig is deprecated, please use instead exportToFile!")
		self.exportToFile(_outfileName)
	#Method for making a copy in a new instance
	def copy( self ):
		return DASConfig.parseString(self.marshal())
	#Static method for parsing a string
	def parseString( _inString ):
		doc = minidom.parseString(_inString)
		rootNode = doc.documentElement
		rootObj = DASConfig()
		rootObj.build(rootNode)
		# Check that all minOccurs are obeyed by marshalling the created object
		oStreamString = StringIO()
		rootObj.export( oStreamString, 0, name_="DASConfig" )
		oStreamString.close()
		return rootObj
	parseString = staticmethod( parseString )
	#Static method for parsing a file
	def parseFile( _inFilePath ):
		doc = minidom.parse(_inFilePath)
		rootNode = doc.documentElement
		rootObj = DASConfig()
		rootObj.build(rootNode)
		return rootObj
	parseFile = staticmethod( parseFile )
# end class DASConfig

class ServerData(object):
	def __init__(self, stopScriptPath=None, startScriptPath=None, host=None):
	
	
		checkType("ServerData", "Constructor of ServerData", host, "string")
		self._host = host
		checkType("ServerData", "Constructor of ServerData", startScriptPath, "string")
		self._startScriptPath = startScriptPath
		checkType("ServerData", "Constructor of ServerData", stopScriptPath, "string")
		self._stopScriptPath = stopScriptPath
	def getHost(self): return self._host
	def setHost(self, host):
		checkType("ServerData", "setHost", host, "string")
		self._host = host
	def delHost(self): self._host = None
	# Properties
	host = property(getHost, setHost, delHost, "Property for host")
	def getStartScriptPath(self): return self._startScriptPath
	def setStartScriptPath(self, startScriptPath):
		checkType("ServerData", "setStartScriptPath", startScriptPath, "string")
		self._startScriptPath = startScriptPath
	def delStartScriptPath(self): self._startScriptPath = None
	# Properties
	startScriptPath = property(getStartScriptPath, setStartScriptPath, delStartScriptPath, "Property for startScriptPath")
	def getStopScriptPath(self): return self._stopScriptPath
	def setStopScriptPath(self, stopScriptPath):
		checkType("ServerData", "setStopScriptPath", stopScriptPath, "string")
		self._stopScriptPath = stopScriptPath
	def delStopScriptPath(self): self._stopScriptPath = None
	# Properties
	stopScriptPath = property(getStopScriptPath, setStopScriptPath, delStopScriptPath, "Property for stopScriptPath")
	def export(self, outfile, level, name_='ServerData'):
		showIndent(outfile, level)
		outfile.write(unicode('<%s>\n' % name_))
		self.exportChildren(outfile, level + 1, name_)
		showIndent(outfile, level)
		outfile.write(unicode('</%s>\n' % name_))
	def exportChildren(self, outfile, level, name_='ServerData'):
		pass
		if self._host is not None:
			showIndent(outfile, level)
			outfile.write(unicode('<host>%s</host>\n' % self._host))
		else:
			warnEmptyAttribute("host", "string")
		if self._startScriptPath is not None:
			showIndent(outfile, level)
			outfile.write(unicode('<startScriptPath>%s</startScriptPath>\n' % self._startScriptPath))
		else:
			warnEmptyAttribute("startScriptPath", "string")
		if self._stopScriptPath is not None:
			showIndent(outfile, level)
			outfile.write(unicode('<stopScriptPath>%s</stopScriptPath>\n' % self._stopScriptPath))
		else:
			warnEmptyAttribute("stopScriptPath", "string")
	def build(self, node_):
		for child_ in node_.childNodes:
			nodeName_ = child_.nodeName.split(':')[-1]
			self.buildChildren(child_, nodeName_)
	def buildChildren(self, child_, nodeName_):
		if child_.nodeType == Node.ELEMENT_NODE and \
			nodeName_ == 'host':
			value_ = ''
			for text__content_ in child_.childNodes:
				if text__content_.nodeValue is not None:
					value_ += text__content_.nodeValue
			self._host = value_
		elif child_.nodeType == Node.ELEMENT_NODE and \
			nodeName_ == 'startScriptPath':
			value_ = ''
			for text__content_ in child_.childNodes:
				if text__content_.nodeValue is not None:
					value_ += text__content_.nodeValue
			self._startScriptPath = value_
		elif child_.nodeType == Node.ELEMENT_NODE and \
			nodeName_ == 'stopScriptPath':
			value_ = ''
			for text__content_ in child_.childNodes:
				if text__content_.nodeValue is not None:
					value_ += text__content_.nodeValue
			self._stopScriptPath = value_
	#Method for marshalling an object
	def marshal( self ):
		oStreamString = StringIO()
		oStreamString.write(unicode('<?xml version="1.0" ?>\n'))
		self.export( oStreamString, 0, name_="ServerData" )
		oStringXML = oStreamString.getvalue()
		oStreamString.close()
		return oStringXML
	#Only to export the entire XML tree to a file stream on disk
	def exportToFile( self, _outfileName ):
		outfile = open( _outfileName, "w" )
		outfile.write(unicode('<?xml version=\"1.0\" ?>\n'))
		self.export( outfile, 0, name_='ServerData' )
		outfile.close()
	#Deprecated method, replaced by exportToFile
	def outputFile( self, _outfileName ):
		print("WARNING: Method outputFile in class ServerData is deprecated, please use instead exportToFile!")
		self.exportToFile(_outfileName)
	#Method for making a copy in a new instance
	def copy( self ):
		return ServerData.parseString(self.marshal())
	#Static method for parsing a string
	def parseString( _inString ):
		doc = minidom.parseString(_inString)
		rootNode = doc.documentElement
		rootObj = ServerData()
		rootObj.build(rootNode)
		# Check that all minOccurs are obeyed by marshalling the created object
		oStreamString = StringIO()
		rootObj.export( oStreamString, 0, name_="ServerData" )
		oStreamString.close()
		return rootObj
	parseString = staticmethod( parseString )
	#Static method for parsing a file
	def parseFile( _inFilePath ):
		doc = minidom.parse(_inFilePath)
		rootNode = doc.documentElement
		rootObj = ServerData()
		rootObj.build(rootNode)
		return rootObj
	parseFile = staticmethod( parseFile )
# end class ServerData

class Server(object):
	def __init__(self, alternativeServer=None, principalServer=None, tangoServerName=None, tangoHost=None, tangoDevice=None):
	
	
		checkType("Server", "Constructor of Server", tangoDevice, "string")
		self._tangoDevice = tangoDevice
		checkType("Server", "Constructor of Server", tangoHost, "string")
		self._tangoHost = tangoHost
		checkType("Server", "Constructor of Server", tangoServerName, "string")
		self._tangoServerName = tangoServerName
		checkType("Server", "Constructor of Server", principalServer, "ServerData")
		self._principalServer = principalServer
		if alternativeServer is None:
			self._alternativeServer = []
		else:
			checkType("Server", "Constructor of Server", alternativeServer, "list")
			self._alternativeServer = alternativeServer
	def getTangoDevice(self): return self._tangoDevice
	def setTangoDevice(self, tangoDevice):
		checkType("Server", "setTangoDevice", tangoDevice, "string")
		self._tangoDevice = tangoDevice
	def delTangoDevice(self): self._tangoDevice = None
	# Properties
	tangoDevice = property(getTangoDevice, setTangoDevice, delTangoDevice, "Property for tangoDevice")
	def getTangoHost(self): return self._tangoHost
	def setTangoHost(self, tangoHost):
		checkType("Server", "setTangoHost", tangoHost, "string")
		self._tangoHost = tangoHost
	def delTangoHost(self): self._tangoHost = None
	# Properties
	tangoHost = property(getTangoHost, setTangoHost, delTangoHost, "Property for tangoHost")
	def getTangoServerName(self): return self._tangoServerName
	def setTangoServerName(self, tangoServerName):
		checkType("Server", "setTangoServerName", tangoServerName, "string")
		self._tangoServerName = tangoServerName
	def delTangoServerName(self): self._tangoServerName = None
	# Properties
	tangoServerName = property(getTangoServerName, setTangoServerName, delTangoServerName, "Property for tangoServerName")
	def getPrincipalServer(self): return self._principalServer
	def setPrincipalServer(self, principalServer):
		checkType("Server", "setPrincipalServer", principalServer, "ServerData")
		self._principalServer = principalServer
	def delPrincipalServer(self): self._principalServer = None
	# Properties
	principalServer = property(getPrincipalServer, setPrincipalServer, delPrincipalServer, "Property for principalServer")
	def getAlternativeServer(self): return self._alternativeServer
	def setAlternativeServer(self, alternativeServer):
		checkType("Server", "setAlternativeServer", alternativeServer, "list")
		self._alternativeServer = alternativeServer
	def delAlternativeServer(self): self._alternativeServer = None
	# Properties
	alternativeServer = property(getAlternativeServer, setAlternativeServer, delAlternativeServer, "Property for alternativeServer")
	def addAlternativeServer(self, value):
		checkType("Server", "setAlternativeServer", value, "ServerData")
		self._alternativeServer.append(value)
	def insertAlternativeServer(self, index, value):
		checkType("Server", "setAlternativeServer", value, "ServerData")
		self._alternativeServer[index] = value
	def export(self, outfile, level, name_='Server'):
		showIndent(outfile, level)
		outfile.write(unicode('<%s>\n' % name_))
		self.exportChildren(outfile, level + 1, name_)
		showIndent(outfile, level)
		outfile.write(unicode('</%s>\n' % name_))
	def exportChildren(self, outfile, level, name_='Server'):
		pass
		if self._tangoDevice is not None:
			showIndent(outfile, level)
			outfile.write(unicode('<tangoDevice>%s</tangoDevice>\n' % self._tangoDevice))
		else:
			warnEmptyAttribute("tangoDevice", "string")
		if self._tangoHost is not None:
			showIndent(outfile, level)
			outfile.write(unicode('<tangoHost>%s</tangoHost>\n' % self._tangoHost))
		else:
			warnEmptyAttribute("tangoHost", "string")
		if self._tangoServerName is not None:
			showIndent(outfile, level)
			outfile.write(unicode('<tangoServerName>%s</tangoServerName>\n' % self._tangoServerName))
		else:
			warnEmptyAttribute("tangoServerName", "string")
		if self._principalServer is not None:
			self.principalServer.export(outfile, level, name_='principalServer')
		else:
			warnEmptyAttribute("principalServer", "ServerData")
		for alternativeServer_ in self.getAlternativeServer():
			alternativeServer_.export(outfile, level, name_='alternativeServer')
	def build(self, node_):
		for child_ in node_.childNodes:
			nodeName_ = child_.nodeName.split(':')[-1]
			self.buildChildren(child_, nodeName_)
	def buildChildren(self, child_, nodeName_):
		if child_.nodeType == Node.ELEMENT_NODE and \
			nodeName_ == 'tangoDevice':
			value_ = ''
			for text__content_ in child_.childNodes:
				if text__content_.nodeValue is not None:
					value_ += text__content_.nodeValue
			self._tangoDevice = value_
		elif child_.nodeType == Node.ELEMENT_NODE and \
			nodeName_ == 'tangoHost':
			value_ = ''
			for text__content_ in child_.childNodes:
				if text__content_.nodeValue is not None:
					value_ += text__content_.nodeValue
			self._tangoHost = value_
		elif child_.nodeType == Node.ELEMENT_NODE and \
			nodeName_ == 'tangoServerName':
			value_ = ''
			for text__content_ in child_.childNodes:
				if text__content_.nodeValue is not None:
					value_ += text__content_.nodeValue
			self._tangoServerName = value_
		elif child_.nodeType == Node.ELEMENT_NODE and \
			nodeName_ == 'principalServer':
			obj_ = ServerData()
			obj_.build(child_)
			self.setPrincipalServer(obj_)
		elif child_.nodeType == Node.ELEMENT_NODE and \
			nodeName_ == 'alternativeServer':
			obj_ = ServerData()
			obj_.build(child_)
			self.alternativeServer.append(obj_)
	#Method for marshalling an object
	def marshal( self ):
		oStreamString = StringIO()
		oStreamString.write(unicode('<?xml version="1.0" ?>\n'))
		self.export( oStreamString, 0, name_="Server" )
		oStringXML = oStreamString.getvalue()
		oStreamString.close()
		return oStringXML
	#Only to export the entire XML tree to a file stream on disk
	def exportToFile( self, _outfileName ):
		outfile = open( _outfileName, "w" )
		outfile.write(unicode('<?xml version=\"1.0\" ?>\n'))
		self.export( outfile, 0, name_='Server' )
		outfile.close()
	#Deprecated method, replaced by exportToFile
	def outputFile( self, _outfileName ):
		print("WARNING: Method outputFile in class Server is deprecated, please use instead exportToFile!")
		self.exportToFile(_outfileName)
	#Method for making a copy in a new instance
	def copy( self ):
		return Server.parseString(self.marshal())
	#Static method for parsing a string
	def parseString( _inString ):
		doc = minidom.parseString(_inString)
		rootNode = doc.documentElement
		rootObj = Server()
		rootObj.build(rootNode)
		# Check that all minOccurs are obeyed by marshalling the created object
		oStreamString = StringIO()
		rootObj.export( oStreamString, 0, name_="Server" )
		oStreamString.close()
		return rootObj
	parseString = staticmethod( parseString )
	#Static method for parsing a file
	def parseFile( _inFilePath ):
		doc = minidom.parse(_inFilePath)
		rootNode = doc.documentElement
		rootObj = Server()
		rootObj.build(rootNode)
		return rootObj
	parseFile = staticmethod( parseFile )
# end class Server



# End of data representation classes.



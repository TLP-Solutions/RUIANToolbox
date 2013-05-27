# -*- coding: cp1250 -*-
#-------------------------------------------------------------------------------
# Name:        parseRUIANfile
# Purpose:     Parsov�n� souboru ve form�tu v�m�nn�ho souboru RUIAN
#
# Author:      Radek August�n
#
# Created:     27/04/2013
# Copyright:   (c) Radek August�n 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os, xml.parsers.expat, gzip, math
import configRUIAN, DBHandlers, textFile_DBHandler, postGIS_DBHandler, configGUI

# @TODO Do�e�it duplicitn� vno�en� n�zvy coi:Kod vs obi:Kod
# @TODO Jak vy�e�it UTF-8

removeTables = False
DATA_XML_PATH = "VymennyFormat/Data"
XML_PATH_SEPARATOR = "/"

def getTabs(numTabs):
    result = ""
    for i in range(1, numTabs):
        result = result + "\t"

    return result

def removeFileExt(fileName):
    lastDotIndex = fileName.rfind(".")
    if lastDotIndex >= 0:
        return fileName[0:lastDotIndex]
    else:
        return fileName

def isImportedTable(tableName):
    result = False
    if configRUIAN.tableDef.has_key(tableName):
        treeViewSet = configGUI.configData['treeViewSet']
        if treeViewSet.has_key(tableName):
            tableSettings = treeViewSet[tableName]
            for fieldName in tableSettings:
                if tableSettings[fieldName] == "True":
                    return True
    return result

class RUIANParser:
    """ T��da implementuj�c� konverzi z exportn�ho form�tu R�IAN. """
    def __init__(self):
        ''' Nastavuje prom�nnou databasePath a inicializuje seznam otev�en�ch
        soubor�'''
        self.buildXMLSubPaths()
        pass

    def buildXMLSubPaths(self):
        ''' Vytvo�� vlastnost xmlSubPath pro ka�dou definici polo�ky v ka�d� tabulce.
        Z�rove� vytvo�� pole se seznamem xmlSubPath-s pro ka�dou tabulku.
        '''
        for tableDef in configRUIAN.tableDef.values():
            xmlSubPaths = {}
            fieldDefs = tableDef[configRUIAN.FIELDS_KEY_NAME]
            for fieldName in fieldDefs:
                fieldDef = fieldDefs[fieldName]
                if not fieldDef.has_key(configRUIAN.XMLSUBPATH_KEYNAME):
                    fieldDef[configRUIAN.XMLSUBPATH_KEYNAME] = fieldName
                xmlSubPaths[fieldDef[configRUIAN.XMLSUBPATH_KEYNAME]] = fieldName
            tableDef[configRUIAN.XMLSUBPATH_KEYNAME] = xmlSubPaths
        pass

    def newRecord(self):
        self.recordValues = {}
        self.columnName = ""
        pass

    def importData(self, inputFileName, dbHandler):
        """ Tato procedura importuje data ze souboru ve form�tu v�m�nn�ho souboru
            RUIAN inputFileName a ulo�� jednotliv� z�znamy pomoc� ovlada�e dbHandler.

            @param {String} inputFileName Vstupn� soubor ve form�tu v�m�nn�ho souboru R�IAN.
            @param {String} inputFileName Vstupn� soubor ve form�tu v�m�nn�ho souboru R�IAN.
        """
        self.elemCount = 0
        self.elemPath = []
        self.elemLevel = 0;
        self.elemPathStr = ""
        self.insideImportedTable = False # True, jestli�e pr�v� zpracov�vanou tabulku m�me za�krtnutu importovat
        self.tableName = None
        self.allowedColumns = None
        self.recordTagName = ""
        self.recordValues = {}
        self.columnName = ""
        self.columnLevel = -1
        self.xmlSubPaths = {}
        self.tableRecordCount = 0

        def start_element(name, attrs):
            """ Start element Handler. """
            self.elemCount = self.elemCount + 1
            self.elemLevel = self.elemLevel + 1
            name = name.replace("vf:", "")  # remove the namespace prefix

            # Jestli�e jsme na �rovni datov�ch tabulek, zalo��me ji
            if self.elemPathStr == DATA_XML_PATH:
                self.insideImportedTable = isImportedTable(name) # configRUIAN.tableDef.has_key(name)
                self.tableName = name
                self.insideTable = True
                self.xmlSubPaths = {}
                if self.insideImportedTable:
                    dbHandler.createTable(self.tableName, removeTables)
                    config = configRUIAN.tableDef[name]
                    self.xmlSubPaths = config[configRUIAN.XMLSUBPATH_KEYNAME]
                    self.recordTagName = ""

                    # Najdeme sloupce k importu
                    if config.has_key(configRUIAN.FIELDS_KEY_NAME):
                         fieldDefs = config[configRUIAN.FIELDS_KEY_NAME]
                         self.allowedColumns = fieldDefs.keys()
                    else:
                        self.allowedColumns = None
                    self.tableRecordCount = 0
                    print "            Importuji tabulku ", self.tableName, ":", self.allowedColumns
                else:
                    print name, "properties are not configured."

            elif self.insideImportedTable: # jsme uvnit� tabulky
                if self.recordTagName == "": # new table record
                    self.recordTagName = name
                    self.newRecord()
                elif (self.allowedColumns != None):
                    # Remove namespace prefix, if needed
                    if configRUIAN.SKIPNAMESPACEPREFIX:
                        doubleDotPos = name.find(":")
                        if doubleDotPos >= 0:
                            name = name[doubleDotPos + 1:]

                    columnPath = self.elemPathStr[len(DATA_XML_PATH + XML_PATH_SEPARATOR + self.tableName + XML_PATH_SEPARATOR + self.recordTagName + XML_PATH_SEPARATOR):]
                    if columnPath <> "":
##                        fieldDefs = configRUIAN.tableDef[self.tableName][configRUIAN.FIELDS_KEY_NAME]
##                        fieldName = fieldDefs.keys()[0]
                        columnPath = columnPath + XML_PATH_SEPARATOR + name
                    else:
                        columnPath = name

                    #if name in self.allowedColumns and self.elemLevel == 5: # start of allowed column
                    if columnPath in self.xmlSubPaths:
                        self.columnName = self.xmlSubPaths[columnPath]
                    else:
                        self.columnName = ""
            else:
                # Skipped tags
                pass

            self.elemPath.append(name)
            self.elemPathStr = XML_PATH_SEPARATOR.join(self.elemPath)

        def end_element(name):
            """ End element Handler """
            name = name.replace("vf:", "")          # remove namespace prefix

            # close table
            if self.insideImportedTable and self.tableName == name and self.elemLevel == 3:
                self.insideImportedTable = False
                self.tableName = None
                self.allowedColumns = None
                print "            Na�teno", self.tableRecordCount, "z�znam�."

            # close record
            elif self.recordTagName == name:
                self.recordTagName = ""
                self.tableRecordCount = self.tableRecordCount + 1
                if 1000*math.floor(self.tableRecordCount/1000) == self.tableRecordCount:
                    print self.tableRecordCount, " records"
                self.tableRecordCount
                if self.insideImportedTable:
                    if self.tableName == 'Parcely' and self.recordValues['Id'] == '141':
                        pass    # ********************* poriznuta, blbe parsovana hodnota  ***********************
                    dbHandler.writeRowToTable(self.tableName, self.recordValues)
                    self.recordValues = {}

            self.elemPath.remove(self.elemPath[len(self.elemPath) - 1])
            self.elemPathStr = XML_PATH_SEPARATOR.join(self.elemPath)
            self.elemLevel = self.elemLevel - 1
            pass

        def char_data(data):
            if self.columnName <> "":
                if self.recordValues.has_key(self.columnName):
                    self.recordValues[self.columnName] = self.recordValues[self.columnName] + data
                else:
                    self.recordValues[self.columnName] = data

        p = xml.parsers.expat.ParserCreate()

        # Assign event handlers to expat parser
        p.StartElementHandler = start_element
        p.EndElementHandler = end_element
        p.CharacterDataHandler = char_data

        # Open and process XML file
        suffix = inputFileName.split('.')[-1]
        if suffix == 'xml':
            f = open(inputFileName, "rt")
        elif suffix == 'gz':
            f = gzip.open(inputFileName, "rb")
        else:
            print "Unexpected file format."

        p.ParseFile(f)
        f.close()

        print self.elemCount, "xml elements read"
        pass

import unittest

class TestRUIANParser(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testimportData(self):
        vfDataPath = "..\\01_Data\\"
        vfFileName = vfDataPath + "20130331_OB_539228_UKSH.xml"
        #vfFileName = vfDataPath + "20130331_OB_554782_UKSH.xml"
        #vfFileName = vfDataPath + "20130331_OB_554782_UZSZ.xml"

        #vfDataPath = "..\\source\\"
        #vfFileName = vfDataPath + "20130331_OB_539228_UKSH.xml"
        #vfFileName = vfDataPath + "20130515_ST_ZZSZ.xml.gz"
        ##vfFileName = vfDataPath + "test_parcely.xml"

        parser = RUIANParser()
        ##db=postGIS_DBHandler.Handler("dbname=euradin host=localhost port=5432 user=postgres password=postgres","public")
        ##parser.importData(vfFileName, db)
        parser.importData(vfFileName, textFile_DBHandler.Handler(vfDataPath, ","))
        pass

class TestGlobalFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testgetTabs(self):
        pass

    def testremoveFileExt(self):
        pass

if __name__ == '__main__':
    unittest.main()

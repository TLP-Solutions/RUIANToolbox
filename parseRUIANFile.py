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
import os, xml.parsers.expat
import configRUIAN, DBHandlers, textFile_DBHandler

# @TODO Do�e�it duplicitn� vno�en� n�zvy coi:Kod vs obi:Kod
# @TODO Jak vy�e�it UTF-8

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

class RUIANParser:
    """ T��da implementuj�c� konverzi z exportn�ho form�tu R�IAN. """
    def __init__(self):
        ''' Nastavuje prom�nnou databasePath a inicializuje seznam otev�en�ch
        soubor�'''
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

        def start_element(name, attrs):
            """ Start element Handler. """
            self.elemCount = self.elemCount + 1
            self.elemLevel = self.elemLevel + 1
            name = name.replace("vf:", "")  # remove the namespace prefix

            # Jestli�e jsme na �rovni datov�ch tabulek, zalo��me ji
            if self.elemPathStr == "VymennyFormat\\Data":
                self.insideImportedTable = configRUIAN.tableDef.has_key(name)
                self.tableName = name
                self.insideTable = True
                if self.insideImportedTable:
                    dbHandler.createTable(self.tableName, True)
                    config = configRUIAN.tableDef[name]
                    self.recordTagName = ""

                    # Najdeme sloupce k importu
                    if config.has_key(configRUIAN.FIELDS_KEY_NAME):
                         fieldDefs = config[configRUIAN.FIELDS_KEY_NAME]
                         self.allowedColumns = fieldDefs.keys()
                    else:
                        self.allowedColumns = None
                    print self.tableName, ":", self.allowedColumns
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

                    if name in self.allowedColumns: # start of allowed column
                        self.columnName = name
                    else:
                        self.columnName = ""
            else:
                # Skipped tags
                pass

            self.elemPath.append(name)
            self.elemPathStr = "\\".join(self.elemPath)

        def end_element(name):
            """ End element Handler """
            name = name.replace("vf:", "")          # remove namespace prefix

            # close table
            if self.insideImportedTable and self.tableName == name and self.elemLevel == 3:
                self.insideImportedTable = False
                self.tableName = None
                self.allowedColumns = None

            # close record
            elif self.recordTagName == name:
                self.recordTagName = ""
                if self.insideImportedTable:
                    dbHandler.writeRowToTable(self.tableName, self.recordValues)
                    self.recordValues = {}

            self.elemPath.remove(self.elemPath[len(self.elemPath) - 1])
            self.elemPathStr = "\\".join(self.elemPath)
            self.elemLevel = self.elemLevel - 1
            pass

        def char_data(data):
            if self.columnName <> "" and not self.recordValues.has_key(self.columnName):
                #value = repr(data)
                #if isinstance(value, unicode):
                #    value = value.encode('ascii','ignore')

                self.recordValues[self.columnName] = data

        p = xml.parsers.expat.ParserCreate()

        # Assign event handlers to expat parser
        p.StartElementHandler = start_element
        p.EndElementHandler = end_element
        p.CharacterDataHandler = char_data

        # Open and process XML file
        f = open(inputFileName, "rt")
        p.ParseFile(f)
        f.close()

        print (self.elemCount, "xml elements read")
        pass


vfDataPath = "I:\\02_OpenIssues\\07_Euradin\\01_Data\\"
vfFileName = vfDataPath + "20130331_OB_539228_UKSH.xml"
vfFileName = vfDataPath + "20130331_OB_554782_UKSH.xml"
#vfFileName = vfDataPath + "20130331_OB_554782_UZSZ.xml"

parser = RUIANParser()
parser.importData(vfFileName, textFile_DBHandler.Handler(vfDataPath))

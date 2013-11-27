# -*- coding: cp1250 -*-
#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      raugustyn
#
# Created:     10/11/2013
# Copyright:   (c) raugustyn 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os, xml.parsers.expat, math
import MatchTools

XML_PATH_SEPARATOR = "/"

class AddressFileParser:
    """ T��da implementuj�c� konverzi z exportn�ho form�tu R�IAN. """
    def __init__(self):
        ''' Nastavuje prom�nnou databasePath a inicializuje seznam otev�en�ch
        soubor�'''
        pass

    def logInfo(self):
        doPrint = 50000*math.floor(self.elemCount/50000) == self.elemCount

        count = len(MatchTools.searchDatabase.townNames)
        doPrint = doPrint or 1000*math.floor(count/1000) == count

        count = len(MatchTools.searchDatabase.streetNames)
        doPrint = doPrint or 50000*math.floor(count/50000) == count


        if doPrint:
            print self.elemCount, u"tag�", \
                    len(MatchTools.searchDatabase.townNames), u"obc�", \
                    len(MatchTools.searchDatabase.streetNames), u"ulic"

    def importData(self, inputFileName):
        """ Tato procedura importuje data ze souboru ve form�tu v�m�nn�ho souboru
            RUIAN inputFileName a ulo�� jednotliv� z�znamy pomoc� ovlada�e dbHandler.

            @param {String} inputFileName Vstupn� soubor ve form�tu v�m�nn�ho souboru R�IAN.
            @param {String} inputFileName Vstupn� soubor ve form�tu v�m�nn�ho souboru R�IAN.
        """
        self.elemCount = 0
        self.elemPath = []
        self.elemLevel = 0;
        self.elemPathStr = ""
        self.recordTagName = ""
        self.recordValues = {}
        self.xmlSubPaths = {}
        self.subXML = []

        def addNameToList(list, name):
            if not name in list:
                list.append(name)
            pass

        def start_element(name, attrs):
            """ Start element Handler. """
            self.elemCount = self.elemCount + 1
            self.elemLevel = self.elemLevel + 1
            self.logInfo()


            self.elemPath.append(name)
            self.elemPathStr = XML_PATH_SEPARATOR.join(self.elemPath)

            if name == "obec":
                MatchTools.searchDatabase.townNames.append(attrs["nazev"])
                addNameToList(MatchTools.searchDatabase.ZIPCodes, attrs["nazev"])
                self.logInfo()

            if name == "ulice":
                MatchTools.searchDatabase.streetNames.append(attrs["nazev"])
                self.logInfo()

        def end_element(name):
            """ End element Handler """
                # jsme uvnit� importovan� tabulky

            self.elemPath.remove(self.elemPath[len(self.elemPath) - 1])
            self.elemPathStr = XML_PATH_SEPARATOR.join(self.elemPath)
            self.elemLevel = self.elemLevel - 1
            pass

        def char_data(data):
            pass

        p = xml.parsers.expat.ParserCreate()

        # Assign event handlers to expat parser
        p.StartElementHandler  = start_element
        p.EndElementHandler    = end_element
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

        print u"P�e�teno", self.elemCount, u"xml element�"
        pass

parser = AddressFileParser()
parser.importData('..\\..\\01_SampleData\\adresy.xml')
MatchTools.searchDatabase.saveToFiles('..\\..\\01_SampleData\\')

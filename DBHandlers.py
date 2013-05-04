# -*- coding: cp1250 -*-
#-------------------------------------------------------------------------------
# Name:        DBTools
# Purpose:     Definuje abstraktn� t��du pro ovl�d�n� datab�ze
#              a testovac� bal��ek k n�
#
# Author:      Augustyn
#
# Created:     03.05.2013
# Copyright:   (c) Augustyn 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
class DatabaseHandler:
    """ Abstraktn� definice datab�ze.
    """

    def deleteTable(self, tableName):
        ''' Uvol�uje tabulku tableName, vrac� True pokud se poda�ilo  '''
        return False

    def tableExists(self, tableName):
        ''' Vrac� True, jestli�e tabulka tableName v datab�zi existuje. '''
        return False

    def createTable(self, tableName, overwriteIfExists = False):
        ''' Vytvo�� tabulku tableName, pokud je�t� neexistuje, se sloupci podle definice v
        configRUIAN.tableDef.'''
        return False

    def writeRowToTable(self, tableName, columnValues):
        ''' Zap�e nov� ��dek do datab�ze s hodnotami ulo�en�mi v dictionary columnValues '''
        return False

    def closeTable(self, tableName):
        ''' Uzav�r� tabulku tableName '''
        return False


import unittest
import configRUIAN

class TestHandler(unittest.TestCase):
    """ Abstraktn� definice testov�n� datab�ze.
    """
    testTableName = "testTable"

    def setUp(self):
        self.h = None
        configRUIAN.tableDef[TestHandler.testTableName] = {
            "skipNamespacePrefix" : "true", # remove namespace prefix obi, oki etc
            "field":{
                "Kod":                   {"type":"Integer", "notNull" : "yes", "pkey" : "yes"},
                "Nazev":                 {"type":"String"},
                "StatusKod":             {"type":"Integer"},
                "PlatiOd":               {"type":"DateTime"},
                "PlatiDo":               {"type":"DateTime"},
                "IdTransakce":           {"type":"Long"},
                "GlobalniIdNavrhuZmeny": {"type":"Long"},
                "VlajkaText":            {"type":"String"},
                "ZnakText":              {"type":"String"},
                "DefinicniBod":          {"type":"MultiPointPropertyType",   "xmlSubPath" : "Geometrie/DefinicniBod"},
                "OriginalniHranice":     {"type":"MultiSurfacePropertyType", "xmlSubPath" : "Geometrie/OriginalniHranice"}
            }
        }

        pass

    def tearDown(self):
        self.h = None
        pass

    def testHandlerAssigned(self):
        self.assertIsNotNone(self.h, "Database handler not assigned")

    def testcreateTable(self):
        self.assertEqual(self.h.createTable(TestHandler.testTableName, True), True, "Vytvo�en� testovac� tabulky")
        self.assertEqual(self.h.tableExists(TestHandler.testTableName), True, "Ov��en� jestli vytvo�en� tabulka existuje")
        pass

    def testdeleteTable(self):
        self.h.createTable(TestHandler.testTableName)
        self.assertEqual(self.h.deleteTable(TestHandler.testTableName), True, "Vytvo��me tabulku a n�sledn� ji sma�eme")

        self.assertEqual(self.h.deleteTable("NonExistingTable"), False, "Snaha o smaz�n� neexistuj�c� tabulky -> vrac� False")
        pass

    def testtableNameToFileName(self):
        pass

    def testtableExists(self):
        if self.h.createTable(TestHandler.testTableName, True):
            self.assertEqual(self.h.tableExists(TestHandler.testTableName), True, "Ov��en� jestli vytvo�en� tabulka existuje")
            self.h.deleteTable(TestHandler.testTableName)
            self.assertEqual(self.h.tableExists(TestHandler.testTableName), False, "Tabulku jsme pr�v� vymazali, tak�e neexistuje")
        pass

    def testwriteRowToTable(self):
        pass
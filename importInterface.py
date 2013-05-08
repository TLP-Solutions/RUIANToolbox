# -*- coding: cp1250 -*-
#-------------------------------------------------------------------------------
# Name:        importInterface
# Purpose:
#
# Author:      Radecek
#
# Created:     06/05/2013
# Copyright:   (c) Radecek 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import configRUIAN, configReader

def dummyMessageProc(message, tabLevel = 0):
    tabStr = ""
    for i in range(0, tabLevel):
        tabStr = tabStr + "    "
    print tabStr + message
    pass

def dummyCreateDatabaseProc():
    displayMessage("Creating database")
    for tableName in configRUIAN.tableDef:
        displayMessage("Creating table " + tableName, 1)
        fields = configReader.getTableFields(tableName)
        displayMessage("fields:" + str(fields), 2)
    displayMessage("Done")
    pass

def onImportDatabaseProc():
    displayMessage("Importing database")
    displayMessage("Importing file file1.xml", 1)
    displayMessage("Importing file file2.xml", 1)
    displayMessage("Done")
    pass

def onDatabaseExistsProc():
    return False

"""
Tato procedura by m�la vypisovat do konzole obsah parametru message. Vzhledem k
tomu, �e jste p�esm�roval standardn� v�stup do textov�ho pole, teda aspo� mysl�m,
tak by nem�lo b�t pot�eba na to sahat.

        # create connections
        XStream.stdout().messageWritten.connect( self._console.insertPlainText )
        XStream.stderr().messageWritten.connect( self._console.insertPlainText )

"""
displayMessage = dummyMessageProc

""" Procedura, kterou vyu�ijeme pro testov�n�, jestli ze str�nky vypln�n�
parametr� datab�ze p�ej�t na vytv��en� datab�ze nebo p��mo na import.
"""
databaseExists = onDatabaseExistsProc

"""
Tuto proceduru spust�me, kdy� p�ejdeme na str�nku vytv��en� datab�ze (databaseExists = false)
"""
createDatabase = dummyCreateDatabaseProc

"""
Tuto proceduru spust�me, kdy� p�ejdeme na str�nku import
"""
importDatabase = onImportDatabaseProc

def main():
    createDatabase()
    importDatabase()
    pass

if __name__ == '__main__':
    main()

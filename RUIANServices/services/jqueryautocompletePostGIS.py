# -*- coding: utf-8 -*-
__author__ = 'Augustyn'

#from log import logger

import psycopg2
#from log import logger
import compileaddress
import HTTPShared
from config import config

class PostGISDatabase():
    DATABASE_HOST = config.databaseHost
    PORT          = config.databasePort
    DATABASE_NAME = config.databaseName
    USER_NAME     = config.databaseUserName
    PASSWORD      = config.databasePassword


    def __init__(self):
        self.conection = psycopg2.connect(host = self.DATABASE_HOST, database = self.DATABASE_NAME, port = self.PORT, user = self.USER_NAME, password = self.PASSWORD)

    def getQueryResult(self, query):
        cursor = self.conection.cursor()
        cursor.execute(query)

        rows = []
        row_count = 0
        for row in cursor:
            row_count += 1
            rows.append(row)
        return rows

    def getObecByName(self, name):
        cursor = self.conection.cursor()
        cursor.execute("SELECT obce FROM obce WHERE nazev_obce like '%" + name + "%'")

        rows = []
        row_count = 0
        for row in cursor:
              row_count += 1
              data = row[0]
              data = data[1:len(data) - 1]
              rows.append(data)
        return rows

    def getZIPByStreetAndTown(self, streetName, townName):
        cursor = self.conection.cursor()
        cursor.execute("SELECT psc FROM addresspoints WHERE nazev_obce = '" + townName + "' and nazev_ulice = '" + streetName + "'")

        rows = []
        row_count = 0
        for row in cursor:
              row_count += 1
              data = row[0]
              data = data[1:len(data) - 1]
              rows.append(data)
        return rows

def numberToString(number):
    if number is None:
        return ""
    else:
        return str(number)

def extractDictrictNumber(nazev_mop):
    # Praha 10 -> 10
    if nazev_mop != "":
        return nazev_mop.split(" ")[1]
    else:
        return ""

def analyseRow(typ_so, cislo_domovni):
    if typ_so[-3:] == ".p.":
        houseNumber = numberToString(cislo_domovni)
        recordNumber = ""
    elif typ_so[-3:] == "ev.":
        houseNumber = ""
        recordNumber = numberToString(cislo_domovni)
    else:
        pass

    return houseNumber, recordNumber


builder = HTTPShared.MimeBuilder("texttoonerow")

ID_VALUE = 'id'

def getAutocompleteOneItemResults(ruianType, nameToken, maxCount = 10):
    #logger.info("getCitiesList")
    if nameToken == "" or nameToken == None:
        return []

    if ruianType == "":
        ruianType == ID_VALUE

    nameToken = nameToken.lower()

    joinSeparator = ", "
    if ruianType == ID_VALUE:
        searchSQL = "select gid from gids where cast(gid as text) ilike '" + nameToken + "%'"

    searchSQL += " limit " + str(maxCount)

    try:
        db = PostGISDatabase()
        cursor = db.conection.cursor()
        #logger.debug("Database encoding:" , db.conection.encoding)
        cursor.execute(searchSQL)
    except:
        import sys
        return[sys.exc_info()[0]]

    rows = []
    rowCount = 0
    for row in cursor:
        rowCount += 1
        v = str(row[0])
        value = '{"id":"' + v + '","label":"' + v + '","value":"' + v + '"}'
        rows.append(value)
        if rowCount >= maxCount:  break

    return rows

def getAutocompleteResults(ruianType, nameToken, maxCount = 10):
    #logger.info("getCitiesList")
    if nameToken == "" or nameToken == None:
        return []

    if ruianType == "":
        ruianType == "town"

    nameToken = nameToken.lower()

    joinSeparator = ", "
    hasNumber = False
    if ruianType == "town":
        searchSQL = "select nazev_obce, psc from obce where nazev_obce ilike '%" + nameToken + "%'"
        isStreet = False
    elif ruianType == ID_VALUE:
        return getAutocompleteOneItemResults(ruianType, nameToken, maxCount)

    elif ruianType == "zip":
        searchSQL = "select psc, nazev_obce from psc where psc like '" + nameToken + "%'"
        joinSeparator = " "
        isStreet = False
    else:
        # street
        isStreet = True
        delPos = nameToken.rfind(" ")
        hasNumber = False
        if delPos >= 0:
            # je tam cislo?
            name = nameToken[:delPos]
            cislo = nameToken[delPos + 1:]
            if cislo.isdigit():
                hasNumber = True
        if hasNumber:
            searchSQL = 'select nazev_ulice, cast(cislo_domovni as text), nazev_obce, cast(psc as text), cast(cislo_orientacni as text), znak_cisla_orientacniho, nazev_casti_obce, typ_so, nazev_mop from address_points ' + \
                        "where nazev_ulice ilike '%" + name + "%' and (cast(cislo_domovni as text) ilike '" + cislo + "%'" + \
                        "or cast(cislo_orientacni as text) ilike '" + cislo + "%')"
        else:
            searchSQL = "select nazev_ulice, nazev_obce, psc from ulice where nazev_ulice ilike '%" + nameToken + "%'"

    searchSQL += " limit " + str(maxCount)

    try:
        db = PostGISDatabase()
        cursor = db.conection.cursor()
        #logger.debug("Database encoding:" , db.conection.encoding)
        cursor.execute(searchSQL)
    except:
        import sys
        return[sys.exc_info()[0]]

    rows = []
    rowCount = 0
    for row in cursor:
        rowCount += 1

        htmlItems = []
        for i in range(len(row)):
            if True:
                htmlItems.append(row[i])
            else:
                item = row[i]
                htmlItems.append(item)

        rowLabel = None
        if ruianType == "street":
            if hasNumber:
                idValue = row[2] + "," + row[3]

                street, houseNumber, locality, zipCode, orientationNumber, orientationNumberCharacter, localityPart, typ_so, nazev_mop = row

                houseNumber, recordNumber = analyseRow(typ_so, houseNumber)
                districtNumber = extractDictrictNumber(nazev_mop)

                rowLabel = compileaddress.compileAddress(builder, street, houseNumber, recordNumber, orientationNumber, orientationNumberCharacter, zipCode, locality, localityPart, districtNumber)
            else:
                idValue = row[1] + "," + row[2]
        else:
            idValue = row[1]

        if rowLabel == None:
            rowLabel = joinSeparator.join(htmlItems)

        if hasNumber:
            rowValue = rowLabel[:rowLabel.find(",")]
        else:
            rowValue = row[0]

        value = '{"id":"' + idValue + '","label":"' + rowLabel + '","value":"' + rowValue + '"}'

        rows.append(value)

        if rowCount >= maxCount:
            break

    return rows

def main():
    #print getAutocompleteResults("zip", "16")
    #print getAutocompleteResults("street", "Mrkvičkova 13")
    print getAutocompleteResults("id", "73")

if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    main()


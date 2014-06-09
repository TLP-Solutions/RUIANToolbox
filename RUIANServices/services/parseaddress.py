# -*- coding: utf-8 -*-
__author__ = 'raugustyn'


import psycopg2
import codecs

DATABASE_HOST = "192.168.1.93"
PORT          = "5432"
DATABASE_NAME = "euradin"
USER_NAME     = "postgres"
PASSWORD      = "postgres"

ADDRESSPOINTS_TABLENAME = "address_points"
FULLTEXT_TABLENAME = "fulltext"

TOWNNAME_FIELDNAME   = "nazev_obce"
STREETNAME_FIELDNAME = "nazev_ulice"
TOWNPART_FIELDNAME   = "nazev_casti_obce"
GID_FIELDNAME        = "gid"
TYP_SO_FIELDNAME     = "typ_so"
CISLO_DOMOVNI_FIELDNAME = "cislo_domovni"
CISLO_ORIENTACNI_FIELDNAME = "cislo_orientacni"
ZNAK_CISLA_ORIENTACNIHO_FIELDNAME = "znak_cisla_orientacniho"
ZIP_CODE_FIELDNAME = "psc"

# Konstanty pro logickou strukturu databáze
MAX_TEXT_COUNT = 3 # maximální počet textových položek v adrese ulice, obec, část obce = 3
ORIENTATION_NUMBER_ID = "/"
RECORD_NUMBER_ID = "č.ev."
DESCRIPTION_NUMBER_ID = "č.p."
RECORD_NUMBER_MAX_LEN = 4
ORIENTATION_NUMBER_MAX_LEN = 3
DESCRIPTION_NUMBER_MAX_LEN = 3
HOUSE_NUMBER_MAX_LEN = 4
ZIPCODE_LEN = 5

class RUIANDatabase():
    def __init__(self):
        self.conection = psycopg2.connect(host = DATABASE_HOST, database = DATABASE_NAME, port = PORT, user = USER_NAME, password = PASSWORD)

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
        cursor.execute("SELECT {0} FROM {1} WHERE {0} ilike '%{2}%' group by {0} limit 25".format(TOWNNAME_FIELDNAME, "obce", name))

        rows = []
        row_count = 0
        for row in cursor:
              row_count += 1
              rows.append(row[0])
        return rows

    def getUliceByName(self, name):
        cursor = self.conection.cursor()
        cursor.execute("SELECT {0} FROM {1} WHERE {0} ilike '%{2}%' group by {0} limit 25".format(STREETNAME_FIELDNAME, "ulice", "name"))

        rows = []
        row_count = 0
        for row in cursor:
              row_count += 1
              rows.append(row[0])
        return rows

    def getCastObceByName(self, name):
        cursor = self.conection.cursor()
        cursor.execute("SELECT nazev_casti_obce FROM casti_obce WHERE nazev_casti_obce ilike '%" + name + "%' group by nazev_casti_obce limit 25")

        rows = []
        row_count = 0
        for row in cursor:
              row_count += 1
              rows.append(row[0])
        return rows

    def getSelectResults(self, sqlSelectClause):
        cursor = self.conection.cursor()
        cursor.execute(sqlSelectClause)

        rows = []
        row_count = 0
        for row in cursor:
              row_count += 1
              rows.append(row)
        return rows

ruianDatabase = None

def isInt(value):
    if value == "" or value == None:
        return False
    else:
        for i in range(len(value)):
            if "0123456789".find(value[i:i + 1]) < 0:
                return False
        return True
    #try:
    #    v = int(value)
    #    return True
    #except ValueError:
    #    return False


class AddressItem:
    def __init__(self, value, searchDB = True):
        self.value = value
        self.towns = []
        self.townParts = []
        self.streets = []
        self.isRecordNumber = False
        self.isOrientationNumber = False
        self.isDescriptionNumber = False
        self.isZIP = False
        self.isHouseNumber = False
        self.number = None
        self.maxNumberLen = 0
        self.isNumberID = False
        self.isTextField = False
        self.analyseValue(searchDB)

    def __repr__(self):
        result = ""
        if self.isZIP: result += "PSČ "

        if self.isOrientationNumber: result += "č.or. "

        if self.isRecordNumber: result += RECORD_NUMBER_ID + " "

        if self.isDescriptionNumber: result += DESCRIPTION_NUMBER_ID + " "

        if self.number == None:
            result += '"' + self.value + '"'
        else:
            result += self.number

        return result

    def __str__(self):
        result = ""
        if self.isZIP: result += "PSČ "

        if self.isOrientationNumber: result += "č.or. "

        if self.isRecordNumber: result += RECORD_NUMBER_ID + " "

        if self.isDescriptionNumber: result += DESCRIPTION_NUMBER_ID + " "

        if self.number == None:
            result += '"' + self.value + '" ' + str(len(self.streets)) + "," + str(len(self.towns)) + \
                      "," + str(len(self.townParts))
        else:
            result += self.number

        return result

    def analyseValue(self, searchDB = True):
        if isInt(self.value):
            self.number = self.value
            pass
        elif self.value == ORIENTATION_NUMBER_ID:
            self.isOrientationNumber = True
            self.isNumberID = True
            self.maxNumberLen = ORIENTATION_NUMBER_MAX_LEN
        elif self.value == RECORD_NUMBER_ID:
            self.isRecordNumber = True
            self.isNumberID = True
            self.maxNumberLen = RECORD_NUMBER_MAX_LEN
        elif self.value == DESCRIPTION_NUMBER_ID:
            self.isDescriptionNumber = True
            self.isNumberID = True
            self.maxNumberLen = DESCRIPTION_NUMBER_MAX_LEN
        else:
            self.isTextField = True
            if searchDB:
                self.towns     = ruianDatabase.getObecByName(self.value)
                self.streets   = ruianDatabase.getUliceByName(self.value)
                self.townParts = ruianDatabase.getCastObceByName(self.value)


class _SearchItem:
    def __init__(self, item, text, fieldName):
        self.item = item
        self.text = text
        self.fieldName = fieldName

    def __repr__(self):
        return self.text + " (" + self.item.value + ")"

    def getWhereItem(self):
        if self.item == None:
            return ""
        else:
            return self.fieldName + "= '" + self.text + "'"
    def getID(self):
        return self.fieldName + ':' + self.text

class AddressParser:
    def normaliseSeparators(self, address):
        address = address.replace(ORIENTATION_NUMBER_ID, " " + ORIENTATION_NUMBER_ID)
        address = address.replace("  ", " ")

        address = address.replace(",,", ",")
        address = address.replace(" ,", ",")
        address = address.replace(", ", ",")

        address = address.replace("\r\r", "\r")
        address = address.replace("\r", ",")

        address = address.replace("\n\n", ",")
        address = address.replace("\n", ",")

        return address

    def normaliseDescriptionNumberID(self, address):
        address = address.replace("čp ", DESCRIPTION_NUMBER_ID + " ")
        address = address.replace("č. p.", DESCRIPTION_NUMBER_ID)
        address = address.replace("čp.", DESCRIPTION_NUMBER_ID)
        return address

    def expandNadPod(self, address):
        address = address.replace(" n ", " nad ")
        address = address.replace(" n.", " nad ")
        address = address.replace(" p ", " pod ")
        address = address.replace(" p.", " pod ")
        return address

    def normaliseRecordNumberID(self, address):
        address = address.replace("ev.č.",  RECORD_NUMBER_ID)
        address = address.replace("ev č.",  RECORD_NUMBER_ID)
        address = address.replace("evč.",   RECORD_NUMBER_ID)
        address = address.replace("eč.",    RECORD_NUMBER_ID)
        address = address.replace("ev. č.", RECORD_NUMBER_ID)
        address = address.replace("č. ev.", RECORD_NUMBER_ID)
        address = address.replace("čev.",   RECORD_NUMBER_ID)
        if address.find("č.ev") >= 0 and address.find("č.ev") != address.find(RECORD_NUMBER_ID):
            address = address.replace("č.ev",   RECORD_NUMBER_ID, 1)
        return address

    def separateNumbers(self, address):
        newAddress = ""
        wasNumber = False
        for i in range(len(address)):
            actChar = address[i:i+1]
            if "0123456789".find(actChar) >= 0:
                if i > 0 and not wasNumber:
                     newAddress += ","
                wasNumber = True
                newAddress += actChar
            elif wasNumber:
                newAddress += actChar + ","
                wasNumber = False
            else:
                newAddress += actChar

        return self.normaliseSeparators(newAddress)

    def normalize(self, address):
        address = self.normaliseSeparators(address)
        address = self.normaliseDescriptionNumberID(address)
        address = self.normaliseRecordNumberID(address)
        address = self.expandNadPod(address)
        address = self.separateNumbers(address)

        return address

    def parse(self, address, searchDB = True):
        address = self.normalize(address)
        stringItems = address.split(",")
        items = []
        for value in stringItems:
            item = AddressItem(value, searchDB)
            items.append(item)
        return items

    def analyseItems(self, items):
        newItems = []
        index = 0
        nextItemToBeSkipped = False
        for item in items:
            if nextItemToBeSkipped:
                nextItemToBeSkipped = False
                continue

            if index == len(items) - 1:
                nextItem = None
            else:
                nextItem = items[index + 1]

            toBeSkipped = False
            if item.isNumberID:
                if nextItem == None or nextItem.number == None or len(nextItem.number) > item.maxNumberLen:
                    toBeSkipped = True
                    # Error, za indikátorem č.ev.,č.or.,/ nenásleduje číslice nebo je příliš dlouhá
                else:
                    item.number = nextItem.number
                    nextItemToBeSkipped = True

            elif item.number != None:
                if nextItem != None and nextItem.number != None and len(item.number) + len(nextItem.number) == ZIPCODE_LEN:
                    item.number += nextItem.number
                    nextItemToBeSkipped = True

                if len(item.number) == ZIPCODE_LEN:
                    item.isZIP = True
                elif len(item.number) <= HOUSE_NUMBER_MAX_LEN:
                    item.isHouseNumber = True
                else:
                    # Error, příliš dlouhé číslo domovní nebo evidenční
                    pass
            else:
                #else textový řetezec
                # @TODO Udelat
                #if item.streets == [] and item.streets == [] and item.streets == []:
                #    toBeSkipped = True
                pass

            if not toBeSkipped:
                newItems.append(item)

            index = index + 1

        return newItems


    def analyse(self, address, searchDB = True):
        items = self.parse(address, searchDB)
        return self.analyseItems(items)

    def old_getCombinedTextSearches(self, items):
        sqlList = []
        sqlSubList = []

        def addCombination(sqlCondition):
            #global sqlSubList
            if sqlSubList == []:
                sqlSubList.append(sqlCondition)
            else:
                for i in range(len(sqlSubList)):
                    sqlSubList[i] += " and " + sqlCondition

        def addCandidates(fieldName, list):
            if list != None and list != []:
                for item in list:
                    addCombination(fieldName + " = '" + item + "'")

        for item in items:
            if item.isTextField():
                sqlSubList = []
                addCandidates(TOWNNAME_FIELDNAME,   item.towns)
                addCandidates(TOWNPART_FIELDNAME,   item.townParts)
                addCandidates(STREETNAME_FIELDNAME, item.streets)

                if sqlList == []:
                    sqlList.extend(sqlSubList)
                else:
                    newList = []
                    for oldItem in sqlList:
                        for newItem in sqlSubList:
                            newList.append(oldItem + " and " + newItem)
                    sqlList = []
                    sqlList.extend(newList)
        return sqlList

    def getTextItems(self, items):
        result = []
        for item in items:
            if item.isTextField():
                result.append(item)
            if len(result) == MAX_TEXT_COUNT:
                break
        return result


    def getTextVariants(self, textItems):
        streets = []
        towns = []
        townParts = []

        for item in textItems:
            for street in item.streets:
                streets.append(_SearchItem(item, street, STREETNAME_FIELDNAME))
            for town in item.towns:
                towns.append(_SearchItem(item, town, TOWNNAME_FIELDNAME))
            for townPart in item.townParts:
                townParts.append(_SearchItem(item, townPart, TOWNPART_FIELDNAME))

        if streets == []:
            streets = [_SearchItem(None, None, None)]

        if towns == []:
            towns = [_SearchItem(None, None, None)]

        if townParts == []:
            townParts = [_SearchItem(None, None, None)]


        return (streets, towns, townParts)


    def expandedTextItems(self, searchItems):
        result = []
        for item in searchItems:
            for street in item.streets:
                result.append(_SearchItem(item, street, STREETNAME_FIELDNAME))

            for town in item.towns:
                result.append(_SearchItem(item, town, TOWNNAME_FIELDNAME))

            for townPart in item.townParts:
                result.append(_SearchItem(item, townPart, TOWNPART_FIELDNAME))

        return result

    def getCombinedTextSearches(self, items):
        textItems = self.getTextItems(items)
        sqlItems = []
        for item in textItems:
            sqlItems.append()

        return []

    def getCandidateValues(self, analysedItems):
        sqlItems = []
        for item in analysedItems:
            if item.isTextField:
                sqlItems.append("searchstr ilike '%" + item.value + "%'")
        innerSql = "select {0} from {1} where {2} limit 30".format(GID_FIELDNAME, FULLTEXT_TABLENAME, " and ".join(sqlItems))
        sql = "select {0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8} from {9} where gid IN ({10})".format(
                GID_FIELDNAME, TOWNNAME_FIELDNAME, TOWNPART_FIELDNAME, STREETNAME_FIELDNAME, TYP_SO_FIELDNAME, \
                CISLO_DOMOVNI_FIELDNAME, CISLO_ORIENTACNI_FIELDNAME, ZNAK_CISLA_ORIENTACNIHO_FIELDNAME, ZIP_CODE_FIELDNAME, ADDRESSPOINTS_TABLENAME, str(innerSql))
        #sql = "SELECT {0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8} from {9} where gid IN ({10})".format(
        #        "gid", "nazev_obce", "nazev_casti_obce", "nazev_ulice", "typ_so", \
        #        "cislo_domovni", "cislo_orientacni", "znak_cisla_orientacniho", "psc"\
        #        "addresspoints", str(innerSql))

        #print sql
        candidates = ruianDatabase.getQueryResult(sql)
        return candidates


    def compare(self, items, candidateValues):
        for item in items:
            found = False
            for candidate in candidateValues:
                if str(candidate).find(item.value) == 0:
                    found = True
            if not found:
                return False

        return True


    def fullTextSearchAddress(self, address):
        items = self.analyse(address, False)
        candidatesIDS = self.getCandidateValues(items)
        results = []
        for candidate in candidatesIDS:
            if self.compare(items, candidate):
                results.append(candidate)

        #for result in results:print result
        return results

def initModule():
    global ruianDatabase
    ruianDatabase = RUIANDatabase()

class FormalTester:
    def __init__(self, caption, desc, compilingPerson, tester):
        self.numTests = 0
        self.caption = caption
        self.desc = desc
        self.compilingPerson = compilingPerson
        self.tester = tester
        self.testsHTML = """
<table>
    <tr>
            <th>#</th><th></th><th>Vstup</th><th>Výsledek</th><th>Pozn</th>
    </tr>
"""

    def addTest(self, inputs, result, expectedResult, errorMessage = ""):
        self.numTests = self.numTests + 1

        if str(result) == expectedResult:
            status = "checked"
            print "   ok :", inputs, "-->", result
            expectedResultMessage = ""
        else:
            status = ""
            expectedResultMessage = " &lt; &gt; " + expectedResult
            print "chyba :", inputs, "-->", result, "<>", expectedResult, errorMessage
        self.testsHTML += "<tr>\n"
        self.testsHTML += "    <td>" + str(self.numTests) + "</td>"
        self.testsHTML += "    <td>" + '<input type="checkbox" value=""' + status + ' \>' + "</td>"

        self.testsHTML += "    <td>" + inputs + "</td>"
        self.testsHTML += "    <td>--> " + str(result) + expectedResultMessage + "</td>"
        self.testsHTML += "    <td>" + errorMessage + "</td>"
        self.testsHTML += "</tr>\n"

    def getHTML(self):
        result = """
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
	</head>
	<body>"""
        if self.caption != "": result += "<h1>" + self.caption + "</h1>\n"
        if self.desc != "": result += "<p>" + self.desc + "</p>\n"
        result += self.testsHTML + "</table>"
        result += """
    </body>
</html>"""

        return result

def testAnalyse():
    parser = AddressParser()
    tester = FormalTester("Rozpoznávání typů adresních položek",
"""Skupina testů zajišťujících rozpoznání jednotlivých typů adresních položek v adresním řetězci.
Jednotlivé testy spadají do kategorie tzv. "unit testů", tj. hodnoty a kombinace nemusí být zcela reálné, cílem je
úplná sada eliminující možné chyby.
V této skupině testů je také testováno párování identifikátorů jednotlivých položek se svými hodnotami.
""", "Ing. Tomáš Vacek", "Ing. Radek Makovec")

    def doTest(value, expectedValue, ErrorMessage = ""):
        tester.addTest(value, parser.analyse(value), expectedValue, ErrorMessage)

    doTest("Pod lesem 1370 č. ev. 1530 Lipník n ", '["Pod lesem", 1370, č.ev. 1530, "Lipník nad "]')

    doTest("3/13", "[3, č.or. 13]", "Rozpoznání čísla orientačního")
    doTest("3/ 13", "[3, č.or. 13]", "Rozpoznání čísla orientačního")
    doTest("3 / 13", "[3, č.or. 13]", "Rozpoznání čísla orientačního")

    doTest("č. p. 113 Bělá", '[č.p. 113, "Bělá"]', 'Rozpoznání čísla popisného')
    doTest("čp. 113 Bělá", '[č.p. 113, "Bělá"]', 'Rozpoznání čísla popisného')
    doTest("č.p. 113 Bělá", '[č.p. 113, "Bělá"]', 'Rozpoznání čísla popisného')
    doTest("č.p.113 Bělá", '[č.p. 113, "Bělá"]', 'Rozpoznání čísla popisného')
    doTest("čp 113 Bělá", '[č.p. 113, "Bělá"]', 'Rozpoznání čísla popisného')
    doTest("čp113 Bělá", '[č.p. 113, "Bělá"]', 'Rozpoznání čísla popisného')

    doTest("16300",  "[PSČ 16300]", 'Rozpoznání PSČ')
    doTest("1 6300", "[PSČ 16300]", 'Rozpoznání PSČ')
    doTest("16 300", "[PSČ 16300]", 'Rozpoznání PSČ')
    doTest("163 00", "[PSČ 16300]", 'Rozpoznání PSČ')
    doTest("1630 0", "[PSČ 16300]", 'Rozpoznání PSČ')

    doTest("Pod lesem 1370 č. ev. 1530, Březová", '["Pod lesem", 1370, č.ev. 1530, "Březová"]', 'Rozpoznání čísla evidenčního')
    doTest("Pod lesem 1370 č.ev. 1530, Březová", '["Pod lesem", 1370, č.ev. 1530, "Březová"]', 'Rozpoznání čísla evidenčního')
    doTest("Pod lesem 1370 č. ev.1530, Březová", '["Pod lesem", 1370, č.ev. 1530, "Březová"]', 'Rozpoznání čísla evidenčního')
    doTest("Pod lesem 1370 č.ev 1530, Březová", '["Pod lesem", 1370, č.ev. 1530, "Březová"]', 'Rozpoznání čísla evidenčního')
    doTest("Pod lesem 1370 č.ev1530, Březová", '["Pod lesem", 1370, č.ev. 1530, "Březová"]', 'Rozpoznání čísla evidenčního')
    doTest("Pod lesem 1370 čev.1530, Březová", '["Pod lesem", 1370, č.ev. 1530, "Březová"]', 'Rozpoznání čísla evidenčního')

    doTest("Roudnice n Labem", '["Roudnice nad Labem"]', "Chybný zápis nad")
    doTest("Roudnice n. Labem", '["Roudnice nad Labem"]', "Chybný zápis nad")

    doTest("Brněnská 1370 č. p. 113, Březová", '["Brněnská", 1370, č.p. 113, "Březová"]')

    doTest("Pod lesem 1370 č. ev. 1530 Svatý Jan p skalo", '["Pod lesem", 1370, č.ev. 1530, "Svatý Jan pod skalo"]')
    doTest("Pod lesem 1370 č. ev. 1530 Lipník n ", '["Pod lesem", 1370, č.ev. 1530, "Lipník nad "]')

    with codecs.open("parseaddress_tests.html", "w", "utf-8") as outFile:
        htmlContent = tester.getHTML()
        outFile.write(htmlContent.decode("utf-8"))
        outFile.close()

def testFullTextSearchAddress():
    parser = AddressParser()
    tester = FormalTester("Rozpoznávání typů adresních položek",
"""Skupina testů zajišťujících rozpoznání jednotlivých typů adresních položek v adresním řetězci.
Jednotlivé testy spadají do kategorie tzv. "unit testů", tj. hodnoty a kombinace nemusí být zcela reálné, cílem je
úplná sada eliminující možné chyby.
V této skupině testů je také testováno párování identifikátorů jednotlivých položek se svými hodnotami.
""", "Ing. Tomáš Vacek", "Ing. Radek Makovec")

    def doTest(value, expectedValue, ErrorMessage = ""):
        tester.addTest(value, parser.analyse(value), expectedValue, ErrorMessage)

    #parser.fullTextSearchAddress("Klostermannova 586, Hořovice, 26801")
    #parser.fullTextSearchAddress("Hořo, Klostermann 586, 26801")
    parser.fullTextSearchAddress("Hořo, Klostermann 7, 26801")

    with codecs.open("parseaddress.html", "w", "utf-8") as outFile:
        htmlContent = tester.getHTML()
        outFile.write(htmlContent.decode("utf-8"))
        outFile.close()

initModule()

def main():
    #testAnalyse()
    testFullTextSearchAddress()

if __name__ == '__main__':
    main()

#create table
#fulltext
#as
#select gid, concat(nazev_obce, ',', nazev_ulice, ',', nazev_casti_obce) searchstr from addresspoints
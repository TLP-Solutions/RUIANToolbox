# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        validateaddressid
# Purpose:
#
# Author:      Radek Augustýn
#
# Created:     13/11/2013
# Copyright:   (c) Radek Augustýn 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
__author__ = 'Radek Augustýn'

from HTTPShared import *
import RUIANConnection

def validateAddressId(resultFormat, addressPlaceId):
    return ""

def validateAddressIdServiceHandler(queryParams, response):
    builder = MimeBuilder(queryParams["Format"])
    response.mimeFormat = builder.getMimeFormat()
    if queryParams["AddressPlaceId"].isdigit():
        address = RUIANConnection.findAddress(queryParams["AddressPlaceId"])
        if address:
            response.htmlData = builder.listToResponseText(["True"])
        else:
            response.htmlData = builder.listToResponseText(["False"])
    else:
        response.htmlData = builder.listToResponseText(["False"])
    response.handled = True
    return response

def createServiceHandlers():
    services.append(
        WebService("/ValidateAddressId", u"Ověření identifikátoru adresy", u"Ověřuje existenci daného identifikátoru adresy",
                   u"""Umožňuje ověřit existenci zadaného identifikátoru adresy RÚIAN v databázi.""",
            [
                getResultFormatParam()
            ],
            [
                getAddressPlaceIdParamURL_IdNotDisabled()
            ],
            validateAddressIdServiceHandler,
            sendButtonCaption = u"Ověř identifikátor adresy",
            htmlInputTemplate = '''<select>
                                        <option value="text">text</option>
                                        <option value="xml">xml</option>
                                        <option value="html">html</option>
                                        <option value="json">json</option>
                                    </select>'''
        )
    )
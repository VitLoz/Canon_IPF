# -*- coding: utf-8 -*-
import urllib.request
import re
import configparser
from tkinter import *
import base64
import time

class ColorImages(object):
    def __init__(self, plotterPageURL):
        self.plotterPageURL = plotterPageURL
        self.regexpr =""r'[<>="]+'"" # r'[<>="]+

        
        with urllib.request.urlopen(self.plotterPageURL) as url:
            htmlText = url.read()
        htmlText = htmlText.decode("utf-8")
        htmlList = htmlText.split("\n")
        
        self.htmlList = htmlList

    def getImageURL(self, htmlLineIndex, splittedItem):
        imageURL = re.split(self.regexpr, self.htmlList[htmlLineIndex])[splittedItem]
        imageURL = self.plotterPageURL + imageURL
        return imageURL

    def getCyanImage(self):
        return self.getImageURL(318, 5)

    def getMagentaImage(self):
        return self.getImageURL(319, 5)

    def getYellowImage(self):
        return self.getImageURL(320, 5)

    def getMbk1Image(self):
        return self.getImageURL(353, 5)

    def getMbk2Image(self):
        return self.getImageURL(354, 5)

    def getBlackImage(self):
        return self.getImageURL(355, 5)

    def getMcImage(self):
        return self.getImageURL(388, 7)

class ColorValues(object):
    def __init__(self, plotterPageURL):
        self.plotterPageURL = plotterPageURL
        self.regexpr =""r'[<>]+'"" 

        
        with urllib.request.urlopen(self.plotterPageURL) as url:
            htmlText = url.read()
        htmlText = htmlText.decode("utf-8")
        htmlList = htmlText.split("\n")
        
        self.htmlList = htmlList


    def getValue(self, htmlLineIndex, splittedItem):
        colorValue = re.split(self.regexpr, self.htmlList[htmlLineIndex])[splittedItem]
        return colorValue

    def getCyanValue(self):
        return self.getValue(329, 2)

    def getMagentaValue(self):
        return self.getValue(330, 2)

    def getYellowValue(self):
        return self.getValue(331, 2)

    def getMbk1Value(self):
        return self.getValue(364, 2)

    def getMbk2Value(self):
        return self.getValue(365, 2)

    def getBlackValue(self):
        return self.getValue(366, 2)

    def getMcValue(self):
        return self.getValue(387, 2)

class PaperTypes(object):
    def __init__(self, plotterPageURL):
        self.plotterPageURL = plotterPageURL
        self.regexpr =""r'[<>]+'""
        
        with urllib.request.urlopen(self.plotterPageURL) as url:
            htmlText = url.read()
        htmlText = htmlText.decode("utf-8")
        htmlList = htmlText.split("\n")
        
        self.htmlList = htmlList

    def getPaper(self, htmlLineIndex, lstPositions):
        paperType = re.split(self.regexpr, self.htmlList[htmlLineIndex])
        returnPaper = ""
        for pos in lstPositions:
            returnPaper += paperType[pos]
            returnPaper+= " "
        return returnPaper

    def getRollPaper(self):
        result = self.getPaper(264, [2, 5])
        if "Unknown" in result:
            return "Неизвестно"
        else:
            return result

    def getCassetePaper(self):
        result = self.getPaper(272, [2, 5])
        if "Unknown" in result:
            return "Неизвестно"
        else:
            return result

class Configuration(object):
    def __init__(self, configPath):
        self.configPath = configPath
        self.Config = configparser.ConfigParser()
        self.Config.read(self.configPath)

    def getConfigValue(self, section):
        dictOptions = {}
        options = self.Config.options(section)
        for option in options:
                dictOptions[option] = self.Config.get(section, option)
        return dictOptions

    def getConfigPlotterIP(self):
        return self.getConfigValue("Network")['plotterip']

    def getConfigRefreshInterval(self):
        return self.getConfigValue("Duration")['refreshrate']

class MainWindow(object):
    def __init__(self):
        self.initMainWindow()

        self.placeCyan()
        self.placeMagenta()
        self.placeYellow()
        self.placeMbk1()
        self.placeMbk2()
        self.placeBlack()
        self.placeMc()
        self.placeRoll()
        self.placeCass()

        self.showWindow()

    def initMainWindow(self):
        self.mainWindow = Tk()
        self.mainWindow.title("iPF610 v. 1.0")
        self.mainWindow.resizable(0,0)

    def createImage(self, imageURL):
        with urllib.request.urlopen(imageURL) as URL:
            raw_data = URL.read()
        return base64.encodestring(raw_data)

    def placeCyan(self):
        self.cyanImageLabel= Label(self.mainWindow)
        self.cyanImageLabel.grid(row = 0, column = 0, sticky = W + E)
        self.cyanValue = StringVar()
        self.cyanValueLabel = Label(textvariable = self.cyanValue).grid(row = 1, column = 0, sticky = W + E)

    def refreshCyan(self):
        self.cyanImage = PhotoImage(data = self.createImage(self.colorImagesLinks.getCyanImage()))
        self.cyanImageLabel.config(image = self.cyanImage)
        self.cyanValue.set(self.colorValues.getCyanValue())

    def placeMagenta(self):
        self.magentaImageLabel= Label(self.mainWindow)
        self.magentaImageLabel.grid(row = 0, column = 1, sticky = W + E)
        self.magentaValue = StringVar()
        self.magentaValueLabel = Label(textvariable = self.magentaValue).grid(row = 1, column = 1, sticky = W + E)

    def refreshMagenta(self):
        self.magentaImage = PhotoImage(data = self.createImage(self.colorImagesLinks.getMagentaImage()))
        self.magentaImageLabel.config(image = self.magentaImage)
        self.magentaValue.set(self.colorValues.getMagentaValue())

    def placeYellow(self):
        self.yellowImageLabel= Label(self.mainWindow)
        self.yellowImageLabel.grid(row = 0, column = 2, sticky = W + E)
        self.yellowValue = StringVar()
        self.yellowValueLabel = Label(textvariable = self.yellowValue).grid(row = 1, column = 2, sticky = W + E)

    def refreshYellow(self):
        self.yellowImage = PhotoImage(data = self.createImage(self.colorImagesLinks.getYellowImage()))
        self.yellowImageLabel.config(image = self.yellowImage)
        self.yellowValue.set(self.colorValues.getYellowValue())

    def placeMbk1(self):
        self.mbk1ImageLabel= Label(self.mainWindow, bg="#8b8989")
        self.mbk1ImageLabel.grid(row = 2, column = 0, sticky = W + E)
        self.mbk1Value = StringVar()
        self.mbk1ValueLabel = Label(textvariable = self.mbk1Value, bg="#8b8989").grid(row = 3, column = 0, sticky = W + E)

    def refreshMbk1(self):
        self.mbk1Image = PhotoImage(data = self.createImage(self.colorImagesLinks.getMbk1Image()))
        self.mbk1ImageLabel.config(image = self.mbk1Image)
        self.mbk1Value.set(self.colorValues.getMbk1Value())

    def placeMbk2(self):
        self.mbk2ImageLabel= Label(self.mainWindow, bg="#8b8989")
        self.mbk2ImageLabel.grid(row = 2, column = 1, sticky = W + E)
        self.mbk2Value = StringVar()
        self.mbk2ValueLabel = Label(textvariable = self.mbk2Value, bg="#8b8989").grid(row = 3, column = 1, sticky = W + E)

    def refreshMbk2(self):
        self.mbk2Image = PhotoImage(data = self.createImage(self.colorImagesLinks.getMbk2Image()))
        self.mbk2ImageLabel.config(image = self.mbk2Image)
        self.mbk2Value.set(self.colorValues.getMbk2Value())

    def placeBlack(self):
        self.blackImageLabel= Label(self.mainWindow)
        self.blackImageLabel.grid(row = 2, column = 2, sticky = W + E)
        self.blackValue = StringVar()
        self.blackValueLabel = Label(textvariable = self.blackValue).grid(row = 3, column = 2, sticky = W + E)

    def refreshBlack(self):
        self.blackImage = PhotoImage(data = self.createImage(self.colorImagesLinks.getBlackImage()))
        self.blackImageLabel.config(image = self.blackImage)
        self.blackValue.set(self.colorValues.getBlackValue())

    def placeMc(self):
        self.mcImageLabel= Label(self.mainWindow)
        self.mcImageLabel.grid(columnspan=3, sticky=W+E)
        self.mcValue = StringVar()
        self.mcValueLabel = Label(textvariable = self.mcValue).grid(columnspan=3, sticky = W + E)

    def refreshMc(self):
        self.mcImage = PhotoImage(data = self.createImage(self.colorImagesLinks.getMcImage()))
        self.mcImageLabel.config(image = self.mcImage)
        self.mcValue.set("Свободно: " + self.colorValues.getMcValue())

    def placeRoll(self):
        self.rollValue = StringVar()
        self.rollValueLabel= Label(textvariable = self.rollValue).grid(columnspan=3, sticky = W)

    def refreshRoll(self):
        self.rollValue.set("Рул: " + self.paperTypes.getRollPaper())

    def placeCass(self):
        self.cassValue = StringVar()
        self.cassValueLabel= Label(textvariable = self.cassValue).grid(columnspan=3, sticky = W)

    def refreshCass(self):
        self.cassValue.set("Касс: " + self.paperTypes.getCassetePaper())

    def getConfig(self):
        self.Config = Configuration("config.ini")
        self.plotterIP = "http://" + self.Config.getConfigPlotterIP()
        self.duration = self.Config.getConfigRefreshInterval()

    def getData(self):
        self.colorImagesLinks = ColorImages(self.plotterIP)
        self.colorValues = ColorValues(self.plotterIP)
        self.paperTypes = PaperTypes(self.plotterIP)
        
    def showWindow(self):
        #Get Config Info for App
        self.getConfig()
        #Get Color Image Links, Papers Types, Colors Values
        self.getData()

        self.refreshCyan()
        self.refreshMagenta()
        self.refreshYellow()
        self.refreshMbk1()
        self.refreshMbk2()
        self.refreshBlack()
        self.refreshMc()
        self.refreshRoll()
        self.refreshCass()
        self.mainWindow.after(self.duration, self.showWindow)
        

mw = MainWindow()
mw.mainWindow.mainloop()

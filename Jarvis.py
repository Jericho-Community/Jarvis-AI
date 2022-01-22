import re as regexModule
import difflib as diffrenceLibModule
import json as JSON
import numpy as number
import scipy as scientificComputing
import statistics
import os


class Jarvis:
    def __init__(self, voiceSettings=None):
        self.voiceSettings = voiceSettings
        with open(os.path.realpath(os.path.join(os.path.dirname(__file__), 'sources', 'resources', 'basic_converse.json')), 'r') as basicConverseJsonFile:
            self.cachedJsonData = {
                "basicConverseJson": JSON.load(basicConverseJsonFile)}

    def start(self):
        self.__programStarted = True
        while self.__programStarted == True:
            userRawinput = (str(input("Wolfy : "))).strip()
            if userRawinput.lower() == 'stop':
                self.__programStarted = None
            else:
                self.__firstParse(userRawinput)

    def __firstParse(self, userRawinput):
        cookedDictionary = {
            "userRawinput": userRawinput,
            "questionsSpotted": self.__regex(userRawinput, 'question'),
            "similarityData": {
                "normalReplies": self.__rawsimilarityStringsfromJson(userRawinput, self.cachedJsonData["basicConverseJson"]["normal_replies"]["rawValue"], self.cachedJsonData["basicConverseJson"]["normal_replies"]["possibleIndex"]),
            },
        }

        print("Jarvis : Similarity Value out of 1.00 ->",cookedDictionary["similarityData"]["normalReplies"]["universalSimilarity"])

    def __rawsimilarityStringsfromJson(self, rawInput, jsonList=[], selectiveIndex=0):
        rawSimilarityDatas = []
        count = 0
        rawInput = rawInput.split(" ") or rawInput
        while count < len(jsonList):
            rawSimilarityData = diffrenceLibModule.SequenceMatcher(
                None, rawInput[selectiveIndex], jsonList[count]).ratio()
            rawSimilarityData = float("{:.3f}".format(
                rawSimilarityData if rawSimilarityData is not None else 0.0))
            rawSimilarityDatas.append(rawSimilarityData)
            count = count + 1

        cookedSimilarityData = {
            "universalSimilarity": bool(max(rawSimilarityDatas) >= 0.75),
            "meanOrAverageData": {
                "rawValue": number.mean(rawSimilarityDatas),
                "arrayValue": jsonList[rawSimilarityDatas.index(min(rawSimilarityDatas, key=(lambda listValue: abs(listValue - number.mean(rawSimilarityDatas)))))]
            },
            "medianOrMiddleData": {
                "rawValue": number.median(rawSimilarityDatas),
                "arrayValue": jsonList[rawSimilarityDatas.index(min(rawSimilarityDatas, key=(lambda listValue: abs(listValue - number.mean(rawSimilarityDatas)))))]
            },
            "modeOrlargestOccurenceData": {
                "rawValue": statistics.mode(rawSimilarityDatas),
                "arrayValue": jsonList[rawSimilarityDatas.index(min(rawSimilarityDatas, key=(lambda listValue: abs(listValue - statistics.mode(rawSimilarityDatas)))))]
            },
            "maxData": {
                "rawValue": max(rawSimilarityDatas),
                "arrayValue": jsonList[rawSimilarityDatas.index(max(rawSimilarityDatas))]
            },
            "minData": {
                "rawValue": min(rawSimilarityDatas),
                "arrayValue": jsonList[rawSimilarityDatas.index(min(rawSimilarityDatas))]
            }
        }

        return cookedSimilarityData

    def __regex(self, value=None, type=None):
        if value == None or not str(value):
            return None
        elif type and type.lower() == 'question' and value.endswith('?'):
            return value
        elif type and type.lower() == 'question' and len(regexModule.compile(r'\s[A-Za-z\s]*\?').findall(value)):
            return regexModule.compile(r'\s[A-Za-z\s]*\?').findall(value)
        else:
            return None


Bot = Jarvis()
Bot.start()

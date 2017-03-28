#!/usr/bin/python
#/****************************************************************************
# AQLogReader
# Copyright (c) 2016, Henrik Egemose Schmidt <hes1990@gmail.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the copyright holder nor the names of its
#      contributors may be used to endorse or promote products derived from
#      this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL HENRIK EGEMOSE SCHMIDT BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#****************************************************************************/
"""
This class is a reader for the AutoQuad log file format.

This implementation is derived from the qgroundcontrol_aq project.
    "https://github.com/AutoQuad/qgroundcontrol_aq"

The Functions in the class do not check for all errors in input.

aqLogReader(logFIleName)
        Initialize the class and load the LOG file.
        If no logfile is given the class is Initialize and the LOG can be
        loaded with the setLogFile function.

setLogFile(logFileName)
        Use to set or change the log file.

printCurrentSettings()
        Use to get a list of the current settings.

printChannelNames()
        Use to get a list of all the available channel names.

setChannels(stringArray)
        Use to select the from which channels to get data.
        stringArray of the type [\"GPS_LAT\",\"GPS_LON\"]

setDataFrameRate(int)
        Use to change the sampling rate given in Hz. Max 200.
        The default FrameRate is 5 Hz.

data = getData()
        Use to get the wanted data from the log
        Return the data in a array of the type:
        [channel1(0),channel2(0), etc.],
        [channel1(1),channel2(1), etc.], etc.

******************************************************************************
Change log:
2016-03-31 Henrik: implementation of an AutoQuad log reader.
"""

from struct import unpack
import time

class aqLogReader():

    #List of all AutoQuad channel names
    allChannelNames = ["LASTUPDATE", "VOLTAGE0", "VOLTAGE1", "VOLTAGE2", "VOLTAGE3", "VOLTAGE4", "VOLTAGE5", "VOLTAGE6", "VOLTAGE7", "VOLTAGE8", "VOLTAGE9", "VOLTAGE10", "VOLTAGE11", "VOLTAGE12", "VOLTAGE13", "VOLTAGE14", "IMU_RATEX", "IMU_RATEY", "IMU_RATEZ", "IMU_ACCX", "IMU_ACCY", "IMU_ACCZ", "IMU_MAGX", "IMU_MAGY", "IMU_MAGZ", "GPS_PDOP", "GPS_HDOP", "GPS_VDOP", "GPS_TDOP", "GPS_NDOP", "GPS_EDOP", "GPS_ITOW", "GPS_POS_UPDATE", "GPS_LAT", "GPS_LON", "GPS_HEIGHT", "GPS_HACC", "GPS_VACC", "GPS_VEL_UPDATE", "GPS_VELN", "GPS_VELE", "GPS_VELD", "GPS_SACC", "ADC_PRESSURE1", "ADC_PRESSURE2", "ADC_TEMP0", "ADC_TEMP1", "ADC_TEMP2", "ADC_VIN", "ADC_MAG_SIGN", "UKF_Q1", "UKF_Q2", "UKF_Q3", "UKF_Q4", "UKF_POSN", "UKF_POSE", "UKF_POSD", "UKF_PRES_ALT", "UKF_ALT", "UKF_VELN", "UKF_VELE", "UKF_VELD", "MOT_MOTOR0", "MOT_MOTOR1", "MOT_MOTOR2", "MOT_MOTOR3", "MOT_MOTOR4", "MOT_MOTOR5", "MOT_MOTOR6", "MOT_MOTOR7", "MOT_MOTOR8", "MOT_MOTOR9", "MOT_MOTOR10", "MOT_MOTOR11", "MOT_MOTOR12", "MOT_MOTOR13", "MOT_THROTTLE", "MOT_PITCH", "MOT_ROLL", "MOT_YAW", "RADIO_QUALITY", "RADIO_CHANNEL0", "RADIO_CHANNEL1", "RADIO_CHANNEL2", "RADIO_CHANNEL3", "RADIO_CHANNEL4", "RADIO_CHANNEL5", "RADIO_CHANNEL6", "RADIO_CHANNEL7", "RADIO_CHANNEL8", "RADIO_CHANNEL9", "RADIO_CHANNEL10", "RADIO_CHANNEL11", "RADIO_CHANNEL12", "RADIO_CHANNEL13", "RADIO_CHANNEL14", "RADIO_CHANNEL15", "RADIO_CHANNEL16", "RADIO_CHANNEL17", "RADIO_ERRORS", "GMBL_TRIGGER", "ACC_BIAS_X", "ACC_BIAS_Y", "ACC_BIAS_Z", "CURRENT_PDB", "CURRENT_EXT", "VIN_PDB", "UKF_ALT_VEL", "NUM_IDS"]

    #list of data formats
    logFieldTypes = ["DOUBLE", "FLOAT", "U32", "S32", "U16", "S16", "U8", "S8"]

    def __init__(self,logFileName = None):
        self.logFileName = logFileName
        self.logFrameRate = 200 #in Hz. The drone logging rate.
        self.dataFrameRate = 5 #in Hz.

        self.channelsToExport = []
        self.logDataSize = 0
        self.channelNames = []

        if self.logFileName != None:
            (self.fieldIdNumber,self.fieldTypeNumber) = self.getHeader()
            if self.fieldIdNumber != -1:
                self.getChannelNames()
                self.setChannels()
                self.getLogDataSize()
            else:
                print "\nLog File has no readable Header!\n"

    def help(self):
        print "\nList of commands:\n"
        print "    setLogFile(logFileName)"
        print "        Use to set or change the log file.\n"
        print "    printCurrentSettings()"
        print "        Use to get a list of the current settings.\n"
        print "    printChannelNames()"
        print "        Use to get a list of all the available channel names.\n"
        print "    setChannels(stringArray)"
        print "        Use to select the from which channels to get data."
        print "        stringArray of the type [\"GPS_LAT\",\"GPS_LON\"]\n"
        print "    setDataFrameRate(int)"
        print "        Use to change the sampling rate given in Hz. Max 200.\n"
        print "    data = getData()"
        print "        Use to get the wanted data from the log"
        print "        Return the data in a array of the type:"
        print "            [channel1(0),channel2(0), etc.],"
        print "            [channel1(1),channel2(1), etc.], etc.\n"

    def printCurrentSettings(self):
        print "\nLog file: %s\n" %self.logFileName
        print "dataFrameRate: %i Hz\n" %self.dataFrameRate
        print "Channels selected: "
        if len(self.channelsToExport) == 0:
            print "    None"
        for idx in range(0,len(self.channelsToExport)):
            print "    ", self.channelNames[self.channelsToExport[idx]]
        print "\n"

    def printChannelNames(self):
        if self.channelNames == []:
            print "\nLog file can not be read!\n"
            return
        print "\nNumber and Channel name: "
        idx = 0
        for string in self.channelNames:
            print str(idx) +":"+ string
            idx += 1

    def setDataFrameRate(self, number):
        self.dataFrameRate = number

    def setLogFile(self,logFileName):
        self.logFileName = logFileName
        (self.fieldIdNumber,self.fieldTypeNumber) = self.getHeader()
        if self.fieldIdNumber != -1:
            self.getChannelNames()
            self.setChannels()
            self.getLogDataSize()
        else:
            print "\nLog File has no readable Header!\n"

    def getChannelNames(self):
        self.channelNames = []
        for i in range(0,len(self.fieldIdNumber)):
            channelNumber = self.fieldIdNumber[i]
            channelName = self.allChannelNames[channelNumber]
            self.channelNames.append(channelName)

    def setChannels(self, channelStringArray = None):
        if channelStringArray == None:
            channelStringArray = ["GPS_LAT", "GPS_LON", "GPS_HEIGHT"]
        self.channelsToExport = []
        for i in range(0,len(channelStringArray)):
            try:
                self.channelsToExport.append(self.channelNames.index( channelStringArray[i]))
            except ValueError:
                print "\n%s are not in the data.\n    Use printChannelNames() to get a list of available channels\n" %channelStringArray[i]

    def findHeaderMarker(self):
        c = self.file.read(1)
        if c == "":
            return c
        if c != "A":
            return -1
        c = self.file.read(1)
        if c == "":
            return c
        if c != "q":
            return -1
        c = self.file.read(1)
        if c == "":
            return c
        if c != "H":
            return -1
        return 1

    def findHeader(self):
        headerFound = 0
        while headerFound != 1:
            headerFound = self.findHeaderMarker()
            if headerFound == "":
                return -1
        return 1

    def readHeader(self):
        fieldId = []
        fieldType = []
        numberOfChannels = ord(self.file.read(1))
        checksumCalcA = numberOfChannels
        checksumCalcB = checksumCalcA
        for i in range(0,numberOfChannels):
            onefieldId = ord(self.file.read(1))
            onefieldType = ord(self.file.read(1))
            fieldId.append(onefieldId)
            fieldType.append(onefieldType)
            checksumCalcA = checksumCalcA + onefieldId
            checksumCalcB = checksumCalcB + checksumCalcA
            checksumCalcA = checksumCalcA + onefieldType
            checksumCalcB = checksumCalcB + checksumCalcA
        checksumA = ord(self.file.read(1))
        checksumB = ord(self.file.read(1))
        while (checksumCalcA > 255):
            checksumCalcA = checksumCalcA - 256
        while (checksumCalcB > 255):
            checksumCalcB = checksumCalcB - 256
        if (checksumA == checksumCalcA and checksumB == checksumCalcB):
            return (fieldId,fieldType)
        else:
            return (-1,-1)

    def getHeader(self):
        self.file = open(self.logFileName, "rb")
        endOfFile = 0
        headerMissing = 1
        headerMissingNumber = 0
        while (endOfFile != -1 and headerMissing == 1):
            endOfFile = self.findHeader()
            if endOfFile == -1:
                self.file.close()
                return (-1,-1)
            (fieldId,fieldType) = self.readHeader()
            if fieldId != -1:
                headerMissing = 0
        self.file.close()
        return (fieldId,fieldType)

    def getLogDataSize(self):
        self.logDataSize = 0
        for idx in range(0,len(self.fieldTypeNumber)):
            fieldType = self.logFieldTypes[self.fieldTypeNumber[idx]]
            if fieldType == "DOUBLE":
                self.logDataSize = self.logDataSize + 8
            elif fieldType == "FLOAT" or fieldType == "U32" or fieldType == "S32":
                self.logDataSize = self.logDataSize + 4
            elif fieldType == "U16" or fieldType == "S16":
                self.logDataSize = self.logDataSize + 2
            elif fieldType == "U8" or fieldType == "S8":
                self.logDataSize = self.logDataSize + 1

    def findDataMarker(self):
        c = self.file.read(1)
        if c == "":
            return c
        if c != "A":
            return -1
        c = self.file.read(1)
        if c == "":
            return c
        if c != "q":
            return -1
        c = self.file.read(1)
        if c == "":
            return c
        if c != "M":
            return -1
        return 1

    def findData(self):
        dataFound = 0
        while dataFound != 1:
            dataFound = self.findDataMarker()
            if dataFound == "":
                return -1
        return 1

    def readData(self):
        rawData = self.file.read(self.logDataSize)
        checksumA = ord(self.file.read(1))
        checksumB = ord(self.file.read(1))
        checksumCalcA = 0
        checksumCalcB = 0
        for i in range(0,self.logDataSize):
            checksumCalcA = checksumCalcA + ord(rawData[i])
            checksumCalcB = checksumCalcB + checksumCalcA
        while (checksumCalcA > 255):
            checksumCalcA = checksumCalcA - 256
        while (checksumCalcB > 255):
            checksumCalcB = checksumCalcB - 256
        if (checksumA == checksumCalcA and checksumB == checksumCalcB):
            return rawData
        else:
            return -1

    def convertData(self,rawData):
        j = 0
        logData = len(self.channelsToExport)*[None]
        for idx in range(0,len(self.fieldTypeNumber)):
            fieldType = self.logFieldTypes[self.fieldTypeNumber[idx]]
            if idx in self.channelsToExport:
                channelNum = self.channelsToExport.index(idx)
                if fieldType == "DOUBLE":
                    logData[channelNum] = unpack("d",rawData[j:j+8])[0]
                    j += 8
                elif fieldType == "FLOAT":
                    logData[channelNum] = unpack("f",rawData[j:j+4])[0]
                    j += 4
                elif fieldType == "U32":
                    logData[channelNum] = unpack("I",rawData[j:j+4])[0]
                    j += 4
                elif fieldType == "S32":
                    logData[channelNum] = unpack("i",rawData[j:j+4])[0]
                    j += 4
                elif fieldType == "U16":
                    logData[channelNum] = unpack("H",rawData[j:j+2])[0]
                    j += 2
                elif fieldType == "S16":
                    logData[channelNum] = unpack("h",rawData[j:j+2])[0]
                    j += 2
                elif fieldType == "U8":
                    logData[channelNum] = unpack("B",rawData[j:j+1])[0]
                    j += 1
                elif fieldType == "S8":
                    logData[channelNum] = unpack("b",rawData[j:j+1])[0]
                    j += 1
            else:
                if fieldType == "DOUBLE":
                    j += 8
                elif fieldType == "FLOAT":
                    j += 4
                elif fieldType == "U32":
                    j += 4
                elif fieldType == "S32":
                    j += 4
                elif fieldType == "U16":
                    j += 2
                elif fieldType == "S16":
                    j += 2
                elif fieldType == "U8":
                    j += 1
                elif fieldType == "S8":
                    j += 1
        return logData

    def getData(self):
        if self.logDataSize == 0:
            print "\nThe Log file can not be read!\n"
            return
        self.file = open(self.logFileName, "rb")
        endOfFile = 0
        allLogData = []
        while endOfFile != -1:
            for i in range(0,int(self.logFrameRate/self.dataFrameRate)):
                endOfFile = self.findData()
            if endOfFile != -1:
                rawData = self.readData()
                if rawData != -1:
                    logData = self.convertData(rawData)
                    allLogData.append(logData)
                else:
                    print "Data point checksum mismatch, data point skipped."
        self.file.close()
        return allLogData

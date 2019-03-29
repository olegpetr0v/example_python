#-*- coding: utf-8 -*-

from sys import platform
import os
import time
from datetime import datetime
import pytz
import calendar

from reprint_local import output

#импорт констант
import const


#функция получения разделителя пути
def getPathSep():
    pathSep = None
    if platform == 'win32':
         pathSep = '\\'
    elif platform =='linux':
         pathSep = '/'
    return pathSep


#функция получения даты отчёты из названия файла
def getDate(filePath):
    fileDate = filePath.split(getPathSep())[-1].split('.')[0].split('_')[-1]
    return fileDate


#функция определения даты предыдущего месяца
def getPrevDate(date):
    year, month = int(date[:4]), int(date[4:])
    prevMonth = (month - 2)%12 + 1
    prevYear = year if prevMonth < month else year - 1
    prevDate = '{}{:02}'.format(prevYear, prevMonth) 
    return prevDate


#функция определения типа отчёта
def getFileType(filePath):
    fileName = filePath.split(getPathSep())[-1].split('.')[0].lower()
    rightFileType = None
    for fileType in const.fileTypes:
        if fileName.find(fileType.lower()) != -1:
            rightFileType = fileType
    return rightFileType


# функция сортировки отчётов
def sortCheckFiles(item):
    if item['fileType'] == const.T_01_LOCATION:       return 1
    if item['fileType'] == const.T_01_CLOCATION:      return 2
    if item['fileType'] == const.T_01_TLOCATION:      return 3
    if item['fileType'] == const.T_01_CLOCATION_T:    return 4
    if item['fileType'] == const.T_02_DENSITY:        return 5
    if item['fileType'] == const.T_02_CDENSITY:       return 6
    if item['fileType'] == const.T_02_TDENSITY:       return 7
    if item['fileType'] == const.T_02_CDENSITY_T:     return 8
    if item['fileType'] == const.T_03_MATRIX:         return 9
    if item['fileType'] == const.T_03_CMATRIX:        return 10
    if item['fileType'] == const.T_03_TMATRIX:        return 11
    if item['fileType'] == const.T_04_MATRIX_HMWK:    return 12
    if item['fileType'] == const.T_04_CMATRIX_HMWK:   return 13
    if item['fileType'] == const.T_04_TMATRIX_HMWK:   return 14
    if item['fileType'] == const.T_05_CORR_MET:       return 15
    if item['fileType'] == const.T_09_TIMES:          return 16
    if item['fileType'] == const.T_09_TIMES_H:        return 17
    if item['fileType'] == const.T_09_CTIMES:         return 18
    if item['fileType'] == const.T_09_CTIMES_H:       return 19
    if item['fileType'] == const.T_11_CMAT_METRO:     return 20
    if item['fileType'] == const.T_11_CMAT_METRO_H:   return 21


def sortExtraFiles(item):
    return int(item['fileDate'] + str('%2s' % sortCheckFiles(item)).replace(' ', '0'))


#получение размера файла
def getFileSize(filePath):
    return os.path.getsize(filePath)


# progressbar
def getBar(barName, maxVal):
    if maxVal is None:
        bar = progressbar.ProgressBar(maxval=progressbar.UnknownLength, widgets = [barName, progressbar.SimpleProgress()]).start()        
    else:
        bar = progressbar.ProgressBar(maxval = maxVal, widgets = [barName,
                                                                  progressbar.ReverseBar(left='[', marker='=', right=']'),
                                                                  progressbar.SimpleProgress()
                                                                 ]).start()
    return bar


#получение имени файла из пути
def getFileName(filePath):
    pathSep = getPathSep()
    fileName = filePath.split(pathSep)[-1]
    return fileName


# получение дат рабочих дней в месяце
def getMonthWorkDates(fileDate):
    monthWorkDates = []
    year = int(fileDate[:4])
    month = int(fileDate[4:])
    daysInMonth = calendar.monthrange(year, month)[1]
    for day in range(1, daysInMonth+1):
        if len(str(day)) == 1:
            day = '0' + str(day)
        dayDate = '%s.%s.%s' % (fileDate[:4],fileDate[4:],str(day))
        if datetime.weekday(datetime.strptime(dayDate, '%Y.%m.%d')) in range(5):
            monthWorkDates.append(dayDate)
    for date in monthWorkDates:
        if date in const.HOLIDAY_DATES:
            monthWorkDates.remove(date)
    return monthWorkDates


# получение дат выходных и праздничных дней в месяце
def getMonthHolidayDates(fileDate):
    monthHolidayDates = []
    year = int(fileDate[:4])
    month = int(fileDate[4:])
    daysInMonth = calendar.monthrange(year, month)[1]
    for day in range(1, daysInMonth+1):
        if len(str(day)) == 1:
            day = '0' + str(day)
        dayDate = '%s.%s.%s' % (fileDate[:4],fileDate[4:],str(day))
        if datetime.weekday(datetime.strptime(dayDate, '%Y.%m.%d')) in range(5,7,1):
            monthHolidayDates.append(dayDate)
    monthHolidayDates = monthHolidayDates + const.HOLIDAY_DATES
    return monthHolidayDates
        

#формирование словаря для счётчика
def getCounterDict(checkFiles):
    counterDict = {'flag': True}
    for fileType in checkFiles.keys():
        if fileType in const.fileTypes:
            counterDict[fileType + '_md5Counter'] = None
            counterDict[fileType + '_strCounter'] = None
    return counterDict


def progressViewer(counter):
    print('Проверка..')
    startTime = datetime.now()
    with output(initial_len=int(((len(counter)-1)/2)+1), interval=0) as outputlines:
        while counter['flag'] is True:
            currentTime = datetime.now()
            outputlines[0] = 'Время выполнения: %s' % str(currentTime - startTime)
            i = iter(range(1,int(((len(counter)-1)/2)+1), 1))
            for fileType in const.fileTypes:
                if fileType+'_md5Counter' in counter.keys():
                    if counter[fileType+'_md5Counter'] is None:
                        s2 = counter[fileType+'_md5Counter']
                    elif counter[fileType+'_md5Counter'] >= 0:
                        s2 = counter[fileType+'_md5Counter']
                    else:
                        s2 = str(abs(counter[fileType+'_md5Counter'])) + ' END'
                    if counter[fileType+'_strCounter'] is None:
                        s3 = counter[fileType+'_strCounter']
                    elif counter[fileType+'_strCounter'] >= 0:
                        s3 = counter[fileType+'_strCounter']
                    else:
                        s3 = str(abs(counter[fileType+'_strCounter'])) + ' END'
                    outputlines[next(i)] = '%22s:  Вычисление MD5 - %9s,   Проверено строк - %s' % (fileType, s2, s3)
            time.sleep(0.2)

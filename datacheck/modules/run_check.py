#-*- coding: utf-8 -*-

import time
import os
import sys
from multiprocessing import Process, Pool, Value, Manager, Lock

#импорт вспомогательных функций
from supfuncs import getPathSep, getDate, getPrevDate, getFileType, sortCheckFiles, sortExtraFiles, getCounterDict, progressViewer

import check_01_Location, check_01_CLocation, check_01_TLocation, check_01_CLocation_types
#import check_02_Density, check_02_CDensity, check_02_TDensity, check_02_CDensity_types
#import check_03_Matrix, check_03_CMatrix, check_03_TMatrix
#import check_04_Matrix_HMWK, check_04_CMatrix_HMWK, check_04_TMatrix_HMWK
#import check_05_Corr_Metro
#import check_09_Times, check_09_Times_Holiday, check_09_CTimes, check_09_CTimes_Holiday
#import check_11_CMat_Metro, check_11_CMat_Metro_Holiday

#импорт констант
import const
  
inputPath = '..%s201802' % getPathSep() #'../'
outputPath = '..%s201802.txt' % getPathSep() #'../Результат.txt'
        

def runCheckProcess(fileType, item, checkFiles, extraFiles, counter, lock):
    if fileType == const.T_01_LOCATION:
        ans = check_01_Location.runCheck(item['filePath'], item['fileDate'], checkFiles, extraFiles, counter, lock)
    if fileType == const.T_01_CLOCATION:
        ans = check_01_CLocation.runCheck(item['filePath'], item['fileDate'], checkFiles, extraFiles, counter, lock)
    if fileType == const.T_01_TLOCATION:
        ans = check_01_TLocation.runCheck(item['filePath'], item['fileDate'], checkFiles, extraFiles, counter, lock)
    if fileType == const.T_01_CLOCATION_T:
        ans = check_01_CLocation_types.runCheck(item['filePath'], item['fileDate'], checkFiles, extraFiles, counter, lock)

    
if __name__ == '__main__':
    #получение списка файлов для проверки
    filesInRootPath = []
    if len(sys.argv) > 1:
        #поиск и фильтрация файлов в переданных аргументах
        for file in sys.argv[1:]:
            if os.path.splitext(file)[1] in const.fileFormats:
                filesInRootPath.append(file)
    else:
        #поиск и фильтрация в заданном корневом каталоге всех файлов
        for rootDir, dirs, files in os.walk(inputPath):
            for file in files:
                if os.path.splitext(file)[1] in const.fileFormats:
                    filesInRootPath.append(os.path.join(rootDir, file))
    filesInRootPath.sort()

    #удаление файлов с неопрелеляемой датой из списка файлов
    for filePath in filesInRootPath:
        expectFileDate = filePath.split(getPathSep())[-1].split('.')[0].split('_')[-1]
        if not (len(expectFileDate) == 6 and expectFileDate.isdigit()) is True:
            filesInRootPath.remove(filePath)
        else:
            expectYear, expectMonth = expectFileDate[0:4], expectFileDate[4:6]
            if (int(expectMonth) > 12 and int(expectYear) not in range(2014,2020)):
                filesInRootPath.remove(filePath)
    
    #удаление файлов с неопределяемым типом из списка файлов
    for filePath in filesInRootPath:
        fileName = filePath.split(getPathSep())[-1].split('.')[0]
        findFlag = False
        for fileType in const.fileTypes:
            if fileName.lower().find(fileType.lower()) != -1:
                findFlag = True
        if findFlag == False:
            filesInRootPath.remove(filePath)
    
    #определение списка дат отчётов
    dateSet = set()
    for filePath in filesInRootPath:
        dateSet.add(getDate(filePath))
    dateList = list(dateSet)
    dateList.sort()
    checkDate = dateList[0]
    prevCheckDate = getPrevDate(checkDate)
    
    #структурирование метаданных найденных файлов
    checkFiles = {}
    extraFiles = {}
    for filePath in filesInRootPath:
        if getDate(filePath) == checkDate:
            checkFiles[getFileType(filePath)] = {'filePath':filePath, 'fileType':getFileType(filePath), 'fileDate':getDate(filePath)}
        else:
            if getDate(filePath) not in extraFiles.keys():
                extraFiles[getDate(filePath)] = {}
                extraFiles[getDate(filePath)][getFileType(filePath)] = {'filePath':filePath, 'fileType':getFileType(filePath), 'fileDate':getDate(filePath)}
            else:
                extraFiles[getDate(filePath)][getFileType(filePath)] = {'filePath':filePath, 'fileType':getFileType(filePath), 'fileDate':getDate(filePath)}
    #checkFiles.sort(key=sortCheckFiles)
    #extraFiles.sort(key=sortExtraFiles)

    report = 'Дата проверяемых файлов -- %s.\r\n\r\n' % checkDate
    report += 'Будут проверены файлы:\r\n'
    for item in checkFiles.items():
        report += '%24s : %s\r\n' % (item[1]['fileType'], item[1]['filePath'])
    report += '\r\n'
    if len(extraFiles) > 0:
        report += 'Найдены вспомогательные файлы:\r\n'
    for item1 in extraFiles.items():
        for item2 in item1[1].items():
            report += '%24s : %s\r\n' % (item2[1]['fileType'], item2[1]['filePath'])
    report += '\r\n'
    print(report)
    
    counterDict = getCounterDict(checkFiles)
    m = Manager()
    lock = m.Lock()
    counter = m.dict()
    counter.update(counterDict)
    progressViewer = Process(target=progressViewer, args=(counter,))
    progressViewer.start()
    pool = Pool(4)
    pool.starmap(runCheckProcess, [(item[0], item[1], checkFiles, extraFiles, counter, lock,) for item in list(checkFiles.items())])
    time.sleep(1)
    counter['flag'] = False
    pool.close()
    pool.join()
    progressViewer.join()
    


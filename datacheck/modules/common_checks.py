#-*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import hashlib
from itertools import product
from datetime import datetime
import re
import const
from sys import platform
import os

#импорт вспомогательных функций
from supfuncs import getPathSep, getBar, getFileSize


def checkName(filePath, fileType):
    pathSep = getPathSep()
    try:
        fileName = filePath.split(pathSep)[-1]
        partList = fileName.split('.')[0].split('_')
        if not (len(partList[0]) == 2
                and partList[0][0] in ['0', '1']
                and int(partList[0]) in range(1, 12)
                and int(partList[-2]) in range(1, 20)
                and "_".join(partList[1:-2]) == fileType
                and int(partList[-1][:4]) in range(2014, 2020)
                and int(partList[-1][4:]) in range(1, 13)):
            raise Exception()
    except:
        result = 'Проверка имени файла с набором данных - отклонено.'
        return result
    else:
        result = 'Проверка имени файла с набором данных - принято.'
        return result


def md5Sum(filePath, fileType, counter, lock, blockSize=65536):
    fHash = hashlib.md5()
    counter[fileType + '_md5Counter'] = 0
    calcSize = 0
    fileSize = getFileSize(filePath)
    with open(filePath, 'rb') as f:
        for block in iter(lambda: f.read(blockSize), b""):
            fHash.update(block)
            calcSize += len(block)
            counter[fileType + '_md5Counter'] = round((calcSize/fileSize)*100, 2)
    counter[fileType + '_md5Counter'] = - counter[fileType + '_md5Counter']
    return fHash.hexdigest()


def checkMD5(filePath, fileType, counter, lock):
    sumGiven = md5Sum(filePath, fileType, counter, lock).upper()
    try:
        md5FilePath = filePath + '.md5'
        with open(md5FilePath) as f:
            sumTrue = f.read().strip().split(' ')[0].upper()
    except:
        result = 'Проверка контрольной суммы - отклонено (отсутствует файл %s).' % md5FilePath
    else:
        if sumTrue != sumGiven:
            result = 'Проверка контрольной суммы - отклонено (неверная хэш сумма: должна быть "%s", но дана %s").' % (sumTrue, sumGiven)
        else:
            result = 'Проверка контрольной суммы - принято.'
    return result
                
                
def checkColumns(filePath, columnsTrue):
    try:
        df = pd.read_csv(filePath, header=0, sep=';', nrows=1)
        columnsGiven = list(df.columns)
    except:
        return 'Проверка названий полей в файле с набором данных - отклонено (ошибка при открытии таблицы).'
    else:
        if columnsGiven != columnsTrue:
            result = 'Проверка названий полей в файле с набором данных - отклонено (неверные имена колонок : должны быть %s вместо %s).' % (columnsTrue, columnsGiven)
            return result
        else:
            result = 'Проверка названий полей в файле с набором данных - принято.'
            return result
        
    
class checkTypes():
    def __init__(self, columns, colTypes):
        self.columnNames = columns
        self.columnTypes = colTypes
        self.error = None
        self.result = None
    
    def update(self, chunk):
        if self.error is None:
            for col in self.columnNames:
                colType = self.columnTypes[col]
                if colType == const.TYPE_INT_NOT_NEG:
                    if (chunk[col] < 0).any():
                        self.result = 'некорректное значение в колонке "%s"' % col
                        self.error = True
                elif colType == const.TYPE_DT:
                    pattern = re.compile('\d\d\d\d.\d\d.\d\d')
                    for value in chunk[col]:
                        found = pattern.match(value)
                        if found is None or found.group() != value:
                            self.result = 'некорректное значение в колонке "%s"' % col
                            self.error = True
                            break
                elif colType == const.TYPE_TS_HM:
                    pattern = re.compile('\d\d\d\d.\d\d.\d\d \d\d:\d\d')
                    for value in chunk[col]:
                        found = pattern.match(value)
                        if found is None or found.group() != value: 
                            self.result = 'некорректное значение в колонке "%s"' % col
                            self.error = True
                            break
                elif colType  == const.TYPE_TS_H:
                    pattern = re.compile('\d\d\d\d.\d\d.\d\d \d\d')
                    for value in chunk[col]:
                        found = pattern.match(value)
                        if found is None or found.group() != value:
                            self.result = 'некорректное значение в колонке "%s"' % col
                            self.error = True
                            break

    def commit(self):
        if self.error is not None:
            self.result = 'Проверка форматов значений - отклонено (%s).' % self.result
        else:
            self.result = 'Проверка форматов значений - принято.'
   
    def getResult(self):
        return self.result
        
        
class checkOrder():
    def __init__(self, sortedColumns):
        self.sortedColumns = sortedColumns
        self.error = None
        self.result = None
        
    def update(self, chunk):
        if self.error is None:
            if not all(chunk.sort_values(by=self.sortedColumns).index == chunk.index):
                self.error = None
    
    def commit(self):
        if self.error is not None:
            self.result = 'Проверка выполнения сортировки записей - отклонено.'
        else:
            self.result = 'Проверка выполнения сортировки записей - принято.'
   
    def getResult(self):
        return self.result
        
    
class checkEntirity():
    def __init__(self, checks, dateFormat, year, month):
        #self.result1 = 'Проверка наличия данных за все временные периоды и по всем зонам разбиения - отклонено.'
        self.result1 = None
        #self.result2 = 'Проверка отсутствия данных за некорректные временные периоды или по несуществующим зонам разбиения - отклонено.'
        self.result2 = None
        self.colsToCheck = list(checks.keys())
        days = 29 if ((not year%4 and year%100) or (not year%400)) and (month == 2) else const.daysInMonth[month]
        #days = const.daysInMonth[month]
        self.colTrueSet1 = {}
        self.colTrueSet2 = {}
        self.colGivenSet = {}
        for col, checkType in checks.items():
            # this column is zid/station/cell
            if checkType == const.ALL_ZIDS:
                trueSet1 = set(pd.read_csv(const.ADM_IDS_FILE, sep=';', encoding="utf-8").zone_id)
                trueSet2 = trueSet1.union(list(np.arange(200101, 200108))+[-1, 0])
            elif checkType == const.ALL_CELLS:
                trueSet1 = set(pd.read_csv(const.CELL_IDS_FILE, sep=';', encoding="utf-8").cell_id)
                trueSet2 = trueSet1.union([-1, 0])
            elif checkType == const.ALL_TRZONES:
                trueSet1 = set(pd.read_csv(const.TRZ_IDS_FILE, sep=';', encoding="utf-8").trz_id)
                trueSet2 = trueSet1.union([-1, 0])
            elif checkType == const.ALL_CAT:
                trueSet1 = set(pd.read_csv(const.CAT_IDS_FILE, sep=';', encoding="utf-8").cat_id)
                trueSet2 = trueSet1.union([-1, 0])
            elif checkType == const.ALL_STATIONS:
                #trueSet1 = set(range(1, 196)) if year <= 2015 else set(range(1, 199))
                #trueSet2 = set(range(1, 198)) if year <= 2015 else set(range(1, 200))
                #trueSet1 = set(range(1, 196) if year <= 2015 else set(range(1, 199)) if month < 4 else set(range(1, 200))
                #trueSet2 = set(range(1, 198)) if year <= 2015 else set(range(1, 200)) if month < 4 else set(range(1, 201))
                #trueSet1 = set(range(1, 215)) if year <= 2015 else set(range(1, 200)) if month < 4 else set(range(1, 201)) if month < 10 else set(range(1, 204))
                #trueSet2 = set(range(1, 215)) if year <= 2015 else set(range(1, 200)) if month < 4 else set(range(1, 201)) if month < 10 else set(range(1, 204))
                trueSet1 = set(range(1,215))
                trueSet2 = set(range(1,215))
            # this column is datetime
            elif checkType == const.ALL_MONTHS:
                trueSet1 = set([datetime(year, month, days).__format__(dateFormat)])
                trueSet2 = trueSet1
            elif checkType == const.ALL_DAYS:
                trueSet1 = set([datetime(year, month, d).__format__(dateFormat) for d in range(1, days + 1)])
                trueSet2 = trueSet1
            elif checkType == const.ALL_HOURS:
                trueSet1 = set([datetime(year, month, d, h).__format__(dateFormat) \
                               for (d, h) in product(range(1, days + 1), range(0, 24))])
                trueSet2 = trueSet1
            elif checkType == const.ALL_HALFS_OF_HOUR:
                trueSet1 = set([datetime(year, month, d, h, m).__format__(dateFormat) \
                               for (d, h, m) in product(range(1, days + 1), range(0, 24), np.arange(2)*30)])
                trueSet2 = trueSet1
            elif checkType == const.ALL_MONTH_HOURS:
                trueSet1 = set([datetime(year, month, days, h).__format__(dateFormat) for h in range(0, 24)])
                trueSet2 = trueSet1
            self.colTrueSet1[col] = trueSet1
            self.colTrueSet2[col] = trueSet2
            self.colGivenSet[col] = set()
    
    def update(self, chunk):
        for col in self.colsToCheck:
            self.colGivenSet[col].update(chunk[col])
            
    def commit(self):
        error1 = None
        error2 = None
        for col in self.colsToCheck:
            if not self.colTrueSet1[col].issubset(self.colGivenSet[col]):
                error1 = 'в колонке "%s" не присутствуют значения %s'%(col,\
                                                                       self.colTrueSet1[col].difference(self.colGivenSet[col]))
            if not self.colGivenSet[col].issubset(self.colTrueSet2[col]):
                error2 = 'в колонке "%s" недопустимое значение %s'%(col,\
                                                                    self.colGivenSet[col].difference(self.colTrueSet2[col]))
        if error1 is not None:
            self.result1 = 'Проверка наличия данных за все временные периоды и по всем зонам разбиения - отклонено (%s).' % error1
        else:
            self.result1 = 'Проверка наличия данных за все временные периоды и по всем зонам разбиения - принято.'
        if error2 is not None:
            self.result2 = 'Проверка отсутствия данных за некорректные временные периоды или по несуществующим зонам разбиения - отклонено (%s).' % error2
        else:
            self.result2 = 'Проверка отсутствия данных за некорректные временные периоды или по несуществующим зонам разбиения - принято.'
   
    def getColGivenSet(self):
        return self.colGivenSet
    
    def getResult(self):
        return self.result1, self.result2

#-*- coding: utf-8 -*-

import pandas as pd

#импорт общих проверок
from common_checks import checkName, checkMD5, checkColumns, checkTypes, checkOrder, checkEntirity

#импорт вспомогательных функций
from supfuncs import getFileName

#импорт констант
import const

        
COLUMNS           = ['dt', 'zid', 'customers_cnt_home', 'customers_cnt_job', 'customers_cnt_day', 'customers_cnt_move']
COLUMN_TYPES      = {'dt'                 : const.TYPE_DT, 
                     'zid'                : const.TYPE_INT,
                     'customers_cnt_home' : const.TYPE_INT_NOT_NEG,
                     'customers_cnt_job'  : const.TYPE_INT_NOT_NEG,
                     'customers_cnt_day'  : const.TYPE_INT_NOT_NEG,
                     'customers_cnt_move' : const.TYPE_INT_NOT_NEG }
COLUMN_PAND_TYPES = {'dt'                 : str,
                     'zid'                : int,
                     'customers_cnt_home' : int,
                     'customers_cnt_job'  : int,
                     'customers_cnt_day'  : int,
                     'customers_cnt_move' : int }
SORTED_COLUMNS    = ['dt', 'zid']
CHECK_COLUMNS     = {'dt'  : const.ALL_MONTHS,
                     'zid' : const.ALL_ZIDS }
DATEFORMAT        = '%Y.%m.%d'

LOCATION_COLUMN_PAND_TYPES = {'dt'                 : str,
                              'zid'                : int,
                              'customers_cnt_home' : int,
                              'customers_cnt_job'  : int,
                              'customers_cnt_day'  : int,
                              'customers_cnt_move' : int }


# Проверка №1
class test8():
    def __init__(self):
        self.error = None
        self.result = None
        
    def update(self, chunk):
        if self.error is None:
            if not all(chunk.customers_cnt_move <= chunk.customers_cnt_home) is True: self.error = True
            if not all(chunk.customers_cnt_job <= chunk.customers_cnt_day) is True: self.error = True
            if not all(chunk.customers_cnt_day <= (chunk.customers_cnt_home + chunk.customers_cnt_job)) is True: self.error = True
        
    def commit(self):
        if self.error is True:
            self.result = 'Проверка №1 - отклонено.'
        elif self.error is None:
            self.result = 'Проверка №1 - принято.'
    
    def getResult(self):
        return self.result


# Проверка №2
class test9():
    def __init__(self):
        self.result = None
        self.comPop = 0 # общая численность населения в проверяемом отчёте
    
    def update(self, chunk):
        self.comPop += chunk.customers_cnt_home.sum()
            
    def commit(self):
        statComPop = 20009853
        if (self.comPop < 0.15*statComPop) or (self.comPop > 0.5*statComPop):
            self.result = 'Проверка №2 - отклонено.'
        else:
            self.result = 'Проверка №2 - принято.'
    
    def getResult(self):
        return self.result
    
    
# Перекрёстные проверки
class test10_11():
    def __init__(self, checkFiles):
        self.cLocationExist = None
        self.tLocationExist = None
        self.result10 = None
        self.result11 = None
        self.locationSumHome = 0
        self.cLocationSumHome = 0
        self.tLocationSumHome = 0
        #
        if const.T_01_CLOCATION in checkFiles.keys(): self.cLocationExist = True
        if const.T_01_TLOCATION in checkFiles.keys(): self.tLocationExist = True
                
    def update(self, chunk, checkFiles):
        if self.cLocationExist is True or self.tLocationExist is True: self.locationSumHome += chunk.customers_cnt_home.sum()   
        #
        if self.cLocationExist is True and self.cLocationSumHome is None:
            self.cLocationSumHome = pd.read_csv(checkFiles[const.T_01_CLOCATION]['filePath'], header=0, sep=';', dtype=COLUMN_PAND_TYPES, index_col=False).customers_cnt_home.sum()
        #
        if self.tLocationExist is True and self.tLocationSumHome is None:
            self.tLocationSumHome = pd.read_csv(checkFiles[const.T_01_TLOCATION]['filePath'], header=0, sep=';', dtype=COLUMN_PAND_TYPES, index_col=False).customers_cnt_home.sum()
            
    def commit(self):
        if self.cLocationExist is not True:
            self.result10 = 'Проверка №2 - не проводилось. (Отсутствует отчёт типа CLocation)'
        else:
            if self.locationSumHome == self.cLocationSumHome:
                self.result10 = 'Проверка №2 - принято.'
            else:
                self.result10 = 'Проверка №2 - отклонено.'
        #        
        if self.tLocationExist is False:
            self.result11 = 'Проверка №2 - не проводилось. (Отсутствует отчёт типа TLocation)'
        else:
            if self.locationSumHome == self.tLocationSumHome:
                self.result11 = 'Проверка №2 - принято.'
            else:
                self.result11 = 'Проверка №2 - отклонено.'
    
    def getResult10(self):
        return self.result10
    
    def getResult11(self):
        return self.result11

    
def runCheck(filePath, fileDate, checkFiles, extraFiles, counter, lock, fileType=const.T_01_LOCATION):
    ans =  'Проверка файла %s:' % getFileName(filePath)
    ans += '\r\n'
    ans += '1.1.1  ' + checkName(filePath, fileType)               + '\r\n'
    ans += '1.1.2  ' + checkMD5(filePath, fileType, counter, lock) + '\r\n'
    ans += '1.1.3  ' + checkColumns(filePath, COLUMNS)             + '\r\n'
    
    c4 = checkTypes(COLUMNS, COLUMN_TYPES)
    c5 = checkOrder(SORTED_COLUMNS)
    c6_7 = checkEntirity(CHECK_COLUMNS, DATEFORMAT, int(fileDate[:4]), int(fileDate[4:]))
    c8 = test8()
    c9 = test9()
    c10_11 = test10_11(checkFiles)
    
    counter[fileType + '_strCounter'] = 0
    for chunk in pd.read_csv(filePath, header=0, sep=';', dtype=COLUMN_PAND_TYPES, chunksize=const.CHUNKSIZE, index_col=False):
        c4.update(chunk)
        c5.update(chunk)
        c6_7.update(chunk)
        c8.update(chunk)
        c9.update(chunk)
        c10_11.update(chunk, checkFiles)
        counter[fileType + '_strCounter'] += len(chunk.index)
    
    c4.commit()
    c5.commit()
    c6_7.commit()
    c8.commit()
    c9.commit()
    c10_11.commit()
    
    counter[fileType + '_strCounter'] = - counter[fileType + '_strCounter']
         
    ans += '1.1.4  ' + c4.getResult()           + '\r\n'
    ans += '1.1.5  ' + c5.getResult()           + '\r\n'
    ans += '1.1.6  ' + c6_7.getResult()[0]      + '\r\n'
    ans += '1.1.7  ' + c6_7.getResult()[1]      + '\r\n'
    ans += '1.1.8  ' + c8.getResult()           + '\r\n'
    ans += '1.1.9  ' + c9.getResult()           + '\r\n'
    ans += '1.1.10 ' + c10_11.getResult10()     + '\r\n'
    ans += '1.1.11 ' + c10_11.getResult11()     + '\r\n'
    
    ans += '\r\n'
    return ans

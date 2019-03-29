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
                     'zid' : const.ALL_TRZONES }
DATEFORMAT        = '%Y.%m.%d'


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
class test10_13():
    def __init__(self, checkFiles):
        self.locationExist = None
        self.result10 = None
        self.result11 = None
        self.result12 = None
        self.result13 = None
        self.locationSumHome = None
        self.locationSumJob= None
        self.locationSumDay = None
        self.locationSumMove = None
        self.tLocationSumHome = 0
        self.tLocationSumJob = 0
        self.tLocationSumDay = 0
        self.tLocationSumMove = 0
        #
        if const.T_01_LOCATION in checkFiles.keys(): self.locationExist = True
                
    def update(self, chunk, checkFiles):
        if self.locationExist is True:
            self.tLocationSumHome += chunk.customers_cnt_home.sum()
            self.tLocationSumJob += chunk.customers_cnt_job.sum()
            self.tLocationSumDay += chunk.customers_cnt_day.sum()
            self.tLocationSumMove += chunk.customers_cnt_move.sum()
        #
        if self.locationExist is True and self.locationSumHome is None:
            df = pd.read_csv(checkFiles[const.T_01_LOCATION]['filePath'], header=0, sep=';', dtype=COLUMN_PAND_TYPES, index_col=False)
            self.locationSumHome = df.customers_cnt_home.sum()
            self.locationSumJob = df.customers_cnt_job.sum()
            self.locationSumDay = df.customers_cnt_day.sum()
            self.locationSumMove = df.customers_cnt_move.sum()
        
    def commit(self):
        if self.locationExist is not True:
            self.result10 = 'Перекрёстные проверки - не проводилось. (Отсутствует отчёт типа Location)'
            self.result11 = 'Перекрёстные проверки - не проводилось. (Отсутствует отчёт типа Location)'
            self.result12 = 'Перекрёстные проверки - не проводилось. (Отсутствует отчёт типа Location)'
            self.result13 = 'Перекрёстные проверки - не проводилось. (Отсутствует отчёт типа Location)'
        else:
            if self.tLocationSumHome == self.locationSumHome:
                self.result10 = 'Перекрёстные проверки - принято.'
            else:
                self.result10 = 'Перекрёстные проверки - отклонено.'
            #
            if self.tLocationSumJob == self.locationSumJob:
                self.result11 = 'Перекрёстные проверки - принято.'
            else:
                self.result11 = 'Перекрёстные проверки - отклонено.'
            #
            if self.tLocationSumDay == self.locationSumDay:
                self.result12 = 'Перекрёстные проверки - принято.'
            else:
                self.result12 = 'Перекрёстные проверки - отклонено.'
            #
            if self.tLocationSumMove == self.locationSumMove:
                self.result13 = 'Перекрёстные проверки - принято.'
            else:
                self.result13 = 'Перекрёстные проверки - отклонено.'
    
    def getResult10(self):
        return self.result10
    
    def getResult11(self):
        return self.result11
    
    def getResult12(self):
        return self.result12
    
    def getResult13(self):
        return self.result13

    
def runCheck(filePath, fileDate, checkFiles, extraFiles, counter, lock, fileType=const.T_01_TLOCATION):
    ans =  'Проверка файла %s:' % getFileName(filePath)
    ans += '\r\n'
    ans += '1.3.1  ' + checkName(filePath, fileType)               + '\r\n'
    ans += '1.3.2  ' + checkMD5(filePath, fileType, counter, lock) + '\r\n'
    ans += '1.3.3  ' + checkColumns(filePath, COLUMNS)             + '\r\n'
    
    c4 = checkTypes(COLUMNS, COLUMN_TYPES)
    c5 = checkOrder(SORTED_COLUMNS)
    c6_7 = checkEntirity(CHECK_COLUMNS, DATEFORMAT, int(fileDate[:4]), int(fileDate[4:]))
    c8 = test8()
    c9 = test9()
    c10_13 = test10_13(checkFiles)
    
    counter[fileType + '_strCounter'] = 0
    for chunk in pd.read_csv(filePath, header=0, sep=';', dtype=COLUMN_PAND_TYPES, chunksize=const.CHUNKSIZE, index_col=False):
        c4.update(chunk)
        c5.update(chunk)
        c6_7.update(chunk)
        c8.update(chunk)
        c9.update(chunk)
        c10_13.update(chunk, checkFiles)
        counter[fileType + '_strCounter'] += len(chunk.index)
    
    c4.commit()
    c5.commit()
    c6_7.commit()
    c8.commit()
    c9.commit()
    c10_13.commit()
    
    counter[fileType + '_strCounter'] = - counter[fileType + '_strCounter']
     
    ans += '1.3.4  ' + c4.getResult()           + '\r\n'
    ans += '1.3.5  ' + c5.getResult()           + '\r\n'
    ans += '1.3.6  ' + c6_7.getResult()[0]      + '\r\n'
    ans += '1.3.7  ' + c6_7.getResult()[1]      + '\r\n'
    ans += '1.3.8  ' + c8.getResult()           + '\r\n'
    ans += '1.3.9  ' + c9.getResult()           + '\r\n'
    ans += '1.3.10 ' + c10_13.getResult10()     + '\r\n'
    ans += '1.3.11 ' + c10_13.getResult11()     + '\r\n'
    ans += '1.3.12 ' + c10_13.getResult12()     + '\r\n'
    ans += '1.3.13 ' + c10_13.getResult13()     + '\r\n'
    
    ans += '\r\n'
    return ans

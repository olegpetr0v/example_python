#-*- coding: utf-8 -*-

import pandas as pd

#импорт общих проверок
from common_checks import checkName, checkMD5, checkColumns, checkTypes, checkOrder, checkEntirity

#импорт вспомогательных функций
from supfuncs import getFileName

#импорт констант
import const

        
COLUMNS           = ['customers_type', 'dt', 'zid', 'customers_cnt_home', 'customers_cnt_job', 'customers_cnt_day', 'customers_cnt_move']
COLUMN_TYPES      = {'customers_type'     : const.TYPE_INT,
                     'dt'                 : const.TYPE_DT, 
                     'zid'                : const.TYPE_INT,
                     'customers_cnt_home' : const.TYPE_INT_NOT_NEG,
                     'customers_cnt_job'  : const.TYPE_INT_NOT_NEG,
                     'customers_cnt_day'  : const.TYPE_INT_NOT_NEG,
                     'customers_cnt_move' : const.TYPE_INT_NOT_NEG }
COLUMN_PAND_TYPES = {'customers_type'     : int,
                     'dt'                 : str,
                     'zid'                : int,
                     'customers_cnt_home' : int,
                     'customers_cnt_job'  : int,
                     'customers_cnt_day'  : int,
                     'customers_cnt_move' : int }
SORTED_COLUMNS    = ['customers_type', 'dt', 'zid']
CHECK_COLUMNS     = {'customers_type' : const.ALL_CAT,
                     'dt'             : const.ALL_MONTHS}
DATEFORMAT        = '%Y.%m.%d'

CLOCATION_COLUMN_PAND_TYPES = {'dt'                 : str,
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


# Перекрёстные проверки
class test9_10():
    def __init__(self, checkFiles):
        self.cLocationExist = None
        self.errorCons = None
        self.errorHome = None
        self.errorJob = None
        self.errorInfo = None
        self.result9 = None
        self.result10 = None
        self.aggCLocationTypes = None
        self.aggCLocation = None
        #
        if const.T_01_CLOCATION in checkFiles.keys(): self.cLocationExist = True
    
    def update(self, chunk, checkFiles):
        df = chunk.groupby(['customers_type','zid'], as_index=False).sum()
        if self.aggCLocationTypes is None:
            self.aggCLocationTypes = df
        else:
            df = pd.concat([df, self.aggCLocationTypes], ignore_index=True)
            self.aggCLocationTypes = df.groupby(['customers_type','zid'], as_index=False).sum()
        #
        if self.cLocationExist is True:
            self.aggCLocation = pd.read_csv(checkFiles[const.T_01_CLOCATION]['filePath'], header=0, sep=';', dtype=COLUMN_PAND_TYPES, index_col=False)                      
    
    def commit(self):
        if self.cLocationExist is True:
            df = pd.merge(self.aggCLocationTypes, self.aggCLocation, how='left', left_on=['zid'], right_on=['zid'], suffixes=[':l',':r'])
            if df.isnull().any().any() is True: self.errorCons = True
            if not all (df['customers_cnt_home:l'] <= df['customers_cnt_home:r']) is True: self.errorHome = True
            if not all (df['customers_cnt_job:l'] <= df['customers_cnt_job:r']) is True: self.errorJob = True
        #        
        if self.cLocationExist is not True:
            self.result9 = 'Проверка №1 - не проводилось. (Отсутствует отчёт типа CLocation)'
            self.result10 = 'Проверка №1 - не проводилось. (Отсутствует отчёт типа CLocation)'
        elif self.errorCons is True:
            self.result9 = 'Проверка №1 - отклонено. (В отчёте CLocation отсутствуют требуемые записи)' 
            self.result10 = 'Проверка №1 - отклонено. (В отчёте CLocation отсутствуют требуемые записи)'
        else:
            if self.errorHome is True:
                self.result9 = 'Проверка №1 - отклонено.'
            else:
                self.result9 = 'Проверка №1 - принято.'
            if self.errorJob is True:
                self.result10 = 'Проверка №1 - отклонено.'
            else:
                self.result10 = 'Проверка №1 - принято.'
    
    def getResult9(self):
        return self.result9
    
    def getResult10(self):
        return self.result10      


def runCheck(filePath, fileDate, checkFiles, extraFiles, counter, lock, fileType=const.T_01_CLOCATION_T):
    ans =  'Проверка файла %s:' % getFileName(filePath)
    ans += '\r\n'
    ans += '1.4.1  ' + checkName(filePath, fileType)               + '\r\n'
    ans += '1.4.2  ' + checkMD5(filePath, fileType, counter, lock) + '\r\n'
    ans += '1.4.3  ' + checkColumns(filePath, COLUMNS)             + '\r\n'
    
    c4 = checkTypes(COLUMNS, COLUMN_TYPES)
    c5 = checkOrder(SORTED_COLUMNS)
    c6_7 = checkEntirity(CHECK_COLUMNS, DATEFORMAT, int(fileDate[:4]), int(fileDate[4:]))
    c8 = test8()
    c9_10 = test9_10(checkFiles)
   
    counter[fileType + '_strCounter'] = 0
    for chunk in pd.read_csv(filePath, header=0, sep=';', dtype=COLUMN_PAND_TYPES, chunksize=const.CHUNKSIZE, index_col=False):
        c4.update(chunk)
        c5.update(chunk)
        c6_7.update(chunk)
        c8.update(chunk)
        c9_10.update(chunk, checkFiles)
        counter[fileType + '_strCounter'] += len(chunk.index)
        
    c4.commit()
    c5.commit()
    c6_7.commit()
    c8.commit()
    c9_10.commit()
    
    counter[fileType + '_strCounter'] = - counter[fileType + '_strCounter']
     
    ans += '1.4.4  ' + c4.getResult()          + '\r\n'
    ans += '1.4.5  ' + c5.getResult()          + '\r\n'
    ans += '1.4.6  ' + c6_7.getResult()[0]     + '\r\n'
    ans += '1.4.7  ' + c6_7.getResult()[1]     + '\r\n'
    ans += '1.4.8  ' + c8.getResult()          + '\r\n'
    ans += '1.4.9  ' + c9_10.getResult9()      + '\r\n'
    ans += '1.4.10 ' + c9_10.getResult10()     + '\r\n'
    
    ans += '\r\n'
    return ans

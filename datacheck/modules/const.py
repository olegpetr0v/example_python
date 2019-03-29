#-*- coding: utf-8 -*-

fileFormats = ['.csv', '.gz', '.rar', '.zip']    

T_01_LOCATION     = 'Location'
T_01_CLOCATION    = 'CLocation'
T_01_TLOCATION    = 'TLocation'
T_01_CLOCATION_T  = 'CLocation_types'
T_02_DENSITY      = 'Density'
T_02_CDENSITY     = 'CDensity'
T_02_TDENSITY     = 'TDensity'
T_02_CDENSITY_T   = 'CDensity_types'
T_03_MATRIX       = 'Matrix'
T_03_CMATRIX      = 'CMatrix'
T_03_TMATRIX      = 'TMatrix'
T_04_MATRIX_HMWK  = 'Matrix_Home_Work'
T_04_CMATRIX_HMWK = 'CMatrix_Home_Work'
T_04_TMATRIX_HMWK = 'TMatrix_Home_Work'
T_05_CORR_METRO   = 'Corr_Metro'
T_09_TIMES        = 'Times'
T_09_TIMES_H      = 'Times_Holiday'
T_09_CTIMES       = 'CTimes'
T_09_CTIMES_H     = 'CTimes_Holiday'
T_11_CMAT_METRO   = 'CMatrix_Metro'
T_11_CMAT_METRO_H = 'CMatrix_Metro_holiday'

fileTypes = ( T_01_LOCATION, T_01_CLOCATION, T_01_TLOCATION, T_01_CLOCATION_T,
              T_02_DENSITY, T_02_CDENSITY, T_02_TDENSITY, T_02_CDENSITY_T,
              T_03_MATRIX, T_03_CMATRIX, T_03_TMATRIX,
              T_04_MATRIX_HMWK, T_04_CMATRIX_HMWK, T_04_TMATRIX_HMWK,
              T_05_CORR_METRO,
              T_09_TIMES, T_09_TIMES_H, T_09_CTIMES, T_09_CTIMES_H,
              T_11_CMAT_METRO, T_11_CMAT_METRO_H
            )

daysInMonth = { 1 : 31, 2 : 28, 3 : 31,  4 : 30,  5 : 31,  6 : 30,
                7 : 31, 8 : 31, 9 : 30, 10 : 31, 11 : 30, 12 : 31 }

# имена месяцев в Именительном падеже
monthNames0 = { 1 : 'январь', 2 : 'февраль', 3 : 'март',      4 : 'апрель',   5 : 'май',     6 : 'июнь', 
                7 : 'июль',   8 : 'август',  9 : 'сентябрь', 10 : 'октябрь', 11 : 'ноябрь', 12 : 'декабрь' }
# имена месяцев в Предложном падеже
monthNames1 = { 1 : 'январе', 2 : 'феврале',   3 : 'марте',      4 : 'апреле',    5 : 'мае',      6 : 'июне', 
                7 : 'июле',   8 : 'августе',   9 : 'сентябре',  10 : 'октябре',  11 : 'ноябре',  12 : 'декабре' }
# имена месяцев в Творительном падеже
monthNames2 = { 1 : 'январем', 2 : 'февралем', 3 : 'мартом',     4 : 'апрелем',   5 : 'маем',     6 : 'июнем', 
                7 : 'июлем',   8 : 'августом', 9 : 'сентябрем', 10 : 'октябрем', 11 : 'ноябрем', 12 : 'декабрем' }

HOLIDAY_DATES = ['2018.01.01','2018.01.02','2018.01.03','2018.01.04','2018.01.05','2018.01.08','2018.02.23',
                 '2018.03.08','2018.03.09','2018.04.30','2018.05.01','2018.05.02','2018.05.09','2018.06.11',
                 '2018.06.12','2018.11.05','2018.12.31']

ADM_IDS_FILE  = 'admzone.csv'
CELL_IDS_FILE = 'fishnet.csv'
CELL2ADM_FILE = 'fishnet2adm.csv'
ADM_MKAD_FILE = 'admMKAD.csv'
TRZ_IDS_FILE  = 'trzone.csv'
CAT_IDS_FILE  = 'categories.csv'
           
chunksize = 2 * 10 ** 6
CHUNKSIZE = 1000000

TYPE_INT = 0
TYPE_INT_NOT_NEG = 1
TYPE_DT = 2
TYPE_TS_HM = 3
TYPE_TS_H = 4

# types of check
ALL_MONTHS = 0
ALL_DAYS = 1
ALL_HOURS = 2
ALL_HALFS_OF_HOUR = 3
ALL_MONTH_HOURS = 4

ALL_ZIDS = 5
ALL_CELLS = 6
ALL_STATIONS = 7
ALL_TRZONES = 8
ALL_CAT = 9

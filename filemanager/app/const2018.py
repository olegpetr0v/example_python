#-*- coding: utf-8 -*-

#список всех имен файлов отчётов
REPORTS_FILENAMES = [
     '01_Location',
     '01_CLocation',
     '01_CLocation_types',
     '01_TLocation',
     '02_Density',
     '02_CDensity',
     '02_CDensity_types',
     '02_TDensity',
     '03_Matrix',
     '03_CMatrix',
     '03_TMatrix',
     '04_Matrix_Home_Work',
     '04_CMatrix_Home_Work',
     '04_TMatrix_Home_Work',
     '05_Corr_Metro',
     '09_Times',
     '09_Times_Holiday',
     '09_CTimes',
     '09_CTimes_Holiday',
     '11_CMatrix_Metro',
     '11_CMatrix_Metro_Holiday'
]

#HEADER = ' ' + '_' * 16 + '|'

LINES = {
     '01_Location'              : '|%16s|' % '01_Location',
     '01_CLocation'             : '|%16s|' % '01_CLocation',
     '01_TLocation'             : '|%16s|' % '01_TLocation',
     '01_CLocation_types'       : '|%16s|' % '01_CLocation_t',
     '02_Density'               : '|%16s|' % '02_Density',
     '02_CDensity'              : '|%16s|' % '02_CDensity',
     '02_CDensity_types'        : '|%16s|' % '02_TDensity',
     '02_TDensity'              : '|%16s|' % '02_CDensity_t',
     '03_Matrix'                : '|%16s|' % '03_Matrix',
     '03_CMatrix'               : '|%16s|' % '03_CMatrix',
     '03_TMatrix'               : '|%16s|' % '03_TMatrix',
     '04_Matrix_Home_Work'      : '|%16s|' % '04_Matrix_HMWK',
     '04_CMatrix_Home_Work'     : '|%16s|' % '04_CMatrix_HMWK',
     '04_TMatrix_Home_Work'     : '|%16s|' % '04_TMatrix_HMWK',
     '05_Corr_Metro'            : '|%16s|' % '05_Corr_Metro',
     '09_Times'                 : '|%16s|' % '09_Times',
     '09_Times_Holiday'         : '|%16s|' % '09_Times_H',
     '09_CTimes'                : '|%16s|' % '09_CTimes',
     '09_CTimes_Holiday'        : '|%16s|' % '09_CTimes_H',
     '11_CMatrix_Metro'         : '|%16s|' % '11_CMatrix_M',
     '11_CMatrix_Metro_Holiday' : '|%16s|' % '11_CMatrix_M_H',
}

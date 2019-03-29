#-*- coding: utf-8 -*-

#список всех имен файлов отчётов
REPORTS_FILENAMES = [
     '01_Location',
     '01_CLocation',
     '01_fCLocation',
     '02_Density',
     '02_CDensity',
     '02_fCDensity',
     '03_Matrix',
     '04_Matrix_Home_Work',
     '05_Corr_Metro',
     '06_Matrix_Dom',
     '07_Dachnik',
     '08_ExternalWorkers',
     '09_Times',
     '10_Transit',
     '11_CMatrix_Metro'
]

#HEADER = ' ' + '_' * 16 + '|'

LINES = {
     '01_Location'         : '|%16s|' % '01_Location',
     '01_CLocation'        : '|%16s|' % '01_CLocation',
     '01_fCLocation'       : '|%16s|' % '01_fCLocation',
     '02_Density'          : '|%16s|' % '02_Density',
     '02_CDensity'         : '|%16s|' % '02_CDensity',
     '02_fCDensity'        : '|%16s|' % '02_fCDensity',
     '03_Matrix'           : '|%16s|' % '03_Matrix',
     '04_Matrix_Home_Work' : '|%16s|' % '04_Matrix_HMWK',
     '05_Corr_Metro'       : '|%16s|' % '05_Corr_Metro',
     '06_Matrix_Dom'       : '|%16s|' % '06_Matrix_Dom',
     '07_Dachnik'          : '|%16s|' % '07_Dachnik',
     '08_ExternalWorkers'  : '|%16s|' % '08_ExternalW',
     '09_Times'            : '|%16s|' % '09_Times',
     '10_Transit'          : '|%16s|' % '10_Transit',
     '11_CMatrix_Metro'    : '|%16s|' % '11_CMatrixM'
}

SKIPZIDS = ['150', '152', '241', '252', '261', '263', '266', '335', '368', '460', '475', '263', '1069']

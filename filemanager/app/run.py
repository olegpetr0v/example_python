PROCESSES = 2 #количество параллельных процессов
PATH = 'D:\\allreports' # путь к корневой директории с исходными отчётами
OUTPATH = 'D:\\out' # путь к корневой директории с итоговыми отчётами
TEMPDIRPATH = 'D:\\tmp' # путь к temp директории
RM = '2018' # версия менеджера: 2015 или 2018
COPY = True # включение опции копирования и нормализции имён отчётов в новую директорию,  базовая опция
REPACK = False # включение опции упаковки и нормализации отчётов при копировании, работает только при COPY == True
RECODE = False # включение опции перекодирования отчётов при копировании, работает только при REPACK == True
MONTHLIST2015 = [ # перечень этапов(месяцев) для обработки
    #201507,
    #201508,
    #201509,
    #201510,
    #201511,
    #201512,
    #201601,
    #201602,
    #201603,
    #201604,
    #201605,
    #201606,
    #201607,
    #201608,
    #201609,
    201610,
    #201611,
    #201612,
    #201701,
    #201702,
    #201703,
    #201704,
    #201705,
    #201706    
]
REPORTS2015 = [ # перечень отчётов для обработки, расскоментировать нужные отчёты
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
EXTDICT2015 = { # выбор расширения итогового отчёта: 'csv' или 'gz'
     '01_Location'         :'gz',
     '01_CLocation'        :'gz',
     '01_fCLocation'       :'gz',
     '02_Density'          :'gz',
     '02_CDensity'         :'gz',
     '02_fCDensity'        :'gz',
     '03_Matrix'           :'gz',
     '04_Matrix_Home_Work' :'gz',
     '05_Corr_Metro'       :'gz',
     '06_Matrix_Dom'       :'gz',
     '07_Dachnik'          :'gz',
     '08_ExternalWorkers'  :'gz',
     '09_Times'            :'gz',
     '10_Transit'          :'gz',
     '11_CMatrix_Metro'    :'gz'
}
REPLACEDICTPATH2015 = {
    'azones':'.\\azones.csv', # путь к словарю перекодировки административных районов
    'czones':'.\\czones.csv', # путь к словарю перекодировки ячеек 500х500 районов
}
MONTHLIST2018 = [ # перечень этапов(месяцев) для обработки
    201802,
    201803,
    #201804
]
REPORTS2018 = [ # перечень отчётов для обработки, расскоментировать нужные отчёты
     '01_Location',
     '01_CLocation',
     '01_CLocation_types',
     '01_TLocation',
     '02_Density',
     '02_CDensity',
     #'02_CDensity_types',
     #'02_TDensity',
     #'03_Matrix',
     #'03_CMatrix',
     #'03_TMatrix',
     #'04_Matrix_Home_Work',
     #'04_CMatrix_Home_Work',
     #'04_TMatrix_Home_Work',
     #'05_Corr_Metro',
     #'09_Times',
     #'09_Times_Holiday',
     #'09_CTimes',
     #'09_CTimes_Holiday',
     #'11_CMatrix_Metro',
     #'11_CMatrix_Metro_Holiday'
]
EXTDICT2018 = { # выбор расширения итогового отчёта: 'csv' или 'gz'
     '01_Location'              :'gz',
     '01_CLocation'             :'gz',
     '01_CLocation_types'       :'gz',
     '01_TLocation'             :'gz',
     '02_Density'               :'gz',
     '02_CDensity'              :'gz',
     '02_CDensity_types'        :'gz',
     '02_TDensity'              :'gz',
     '03_Matrix'                :'gz',
     '03_CMatrix'               :'gz',
     '03_TMatrix'               :'gz',
     '04_Matrix_Home_Work'      :'gz',
     '04_CMatrix_Home_Work'     :'gz',
     '04_TMatrix_Home_Work'     :'gz',
     '05_Corr_Metro'            :'gz',
     '09_Times'                 :'gz',
     '09_Times_Holiday'         :'gz',
     '09_CTimes'                :'gz',
     '09_CTimes_Holiday'        :'gz',
     '11_CMatrix_Metro'         :'gz',
     '11_CMatrix_Metro_Holiday' :'gz'
}
REPLACEDICTPATH2018 = {
    'azones':'.\\azones.csv', # путь к словарю перекодировки административных районов
    'czones':'.\\czones.csv', # путь к словарю перекодировки ячеек 500х500 районов
    'tzones':'.\\tzones.csv', # путь к словарю перекодировки транспортных районов
}


from copy_reports import *
from repack_reports import *
from recode_reports import *


if __name__ == '__main__':
    if RM == '2015':
        if COPY == True and REPACK == True and RECODE == True:
            recodeReports(RM, PROCESSES, PATH, OUTPATH, TEMPDIRPATH, MONTHLIST2015, REPORTS2015, EXTDICT2015, REPLACEDICTPATH2015)
        elif COPY == True and REPACK == True and RECODE == False:
            repackReports(RM, PROCESSES, PATH, OUTPATH, TEMPDIRPATH, MONTHLIST2015, REPORTS2015, EXTDICT2015)
        elif COPY == True and REPACK == False and RECODE == False:
            copyReports(RM, PROCESSES, PATH, OUTPATH, TEMPDIRPATH, MONTHLIST2015, REPORTS2015, EXTDICT2015)
        else:
            print('Неправильно заданы параметры!')
    elif RM == '2018':
        if COPY == True and REPACK == True and RECODE == True:
            recodeReports(RM, PROCESSES, PATH, OUTPATH, TEMPDIRPATH, MONTHLIST2018, REPORTS2018, EXTDICT2018, REPLACEDICTPATH2018)
        elif COPY == True and REPACK == True and RECODE == False:
            repackReports(RM, PROCESSES, PATH, OUTPATH, TEMPDIRPATH, MONTHLIST2018, REPORTS2018, EXTDICT2018)
        elif COPY == True and REPACK == False and RECODE == False:
            copyReports(RM, PROCESSES, PATH, OUTPATH, TEMPDIRPATH, MONTHLIST2018, REPORTS2018, EXTDICT2018)
        else:
            print('Неправильно заданы параметры!')

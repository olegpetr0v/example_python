#-*- coding: utf-8 -*

import platform
import os
import shutil
import hashlib
import gzip
from datetime import datetime
from reprint_local import output
import time

#импорт констант
import const2015
import const2018


#функция очистки директории
def cleandir(dirpath):
    sep = getPathSep()
    filelistgen = os.walk(dirpath)
    filelist = []
    dirlist = []
    for i in filelistgen:
        for j in i[1]:
            dirlist.append(i[0] + sep + j)
        for j in i[2]:
            filelist.append(i[0] + sep + j)
    for i in filelist:
        os.remove(i)
    for i in reversed(dirlist):
        os.rmdir(i)


#функция получения разделителя пути
def getPathSep():
    pathSep = None
    p = platform.architecture()
    o = p[1].lower()
    if o.find('windows') != -1:
         pathSep = '\\'
    elif o.find('linux') != -1:
         pathSep = '/'
    return pathSep


#функция проверки файла MD5
def isMD5File(fileName):
    if fileName.lower().find('md5') != -1:
        return True
    else:
        return False


#функция определния типа файла
def getFileType(rm, fileName):
    fileType = ''
    fileName = fileName.lower()
    if rm == '2015':
        for name in const2015.REPORTS_FILENAMES:
            if fileName.find(name.lower()) != -1:
                fileType = name
    elif rm == '2018':
        for name in const2018.REPORTS_FILENAMES:
            if fileName.find(name.lower()) != -1:
                fileType = name
    return fileType


#функция опреления номера итерации
def getFileIter(fileName):
    fileName = fileName.lower()
    fileIter = fileName.split('.')[0].split('_')[-2]
    return fileIter


#функция определения расширения файла csv|gz
def getFileExt(fileName):
    fileExt = ''
    fileName = fileName.lower()
    if fileName.split('.')[-1] == 'csv':
        fileExt = 'csv'
    elif fileName.split('.')[-1] == 'gz':
        fileExt = 'gz'
    return fileExt


#функция сортировки списка файлов
def sortListDir2018(item):
    index = None
    if item.lower().find('01_location')              != -1: index = 1
    if item.lower().find('01_clocation')             != -1: index = 2
    if item.lower().find('01_clocation_types')       != -1: index = 3
    if item.lower().find('01_tlocation')             != -1: index = 4
    if item.lower().find('02_density')               != -1: index = 5
    if item.lower().find('02_cdensity')              != -1: index = 6
    if item.lower().find('02_cdensity_types')        != -1: index = 7
    if item.lower().find('02_tdensity')              != -1: index = 8
    if item.lower().find('03_matrix')                != -1: index = 9
    if item.lower().find('03_cmatrix')               != -1: index = 10
    if item.lower().find('03_tmatrix')               != -1: index = 11
    if item.lower().find('04_matrix_home_work')      != -1: index = 12
    if item.lower().find('04_cmatrix_home_work')     != -1: index = 13
    if item.lower().find('04_tmatrix_home_work')     != -1: index = 14
    if item.lower().find('05_corr_metro')            != -1: index = 15
    if item.lower().find('09_times')                 != -1: index = 16
    if item.lower().find('09_times_holiday')         != -1: index = 17
    if item.lower().find('09_ctimes')                != -1: index = 18
    if item.lower().find('09_ctimes_holiday')        != -1: index = 19
    if item.lower().find('11_cmatrix_metro')         != -1: index = 20
    if item.lower().find('11_cmatrix_metro_holiday') != -1: index = 21
    return index


def sortListDir2015(item):
    index = None
    if item.lower().find('01_location')              != -1: index = 1
    if item.lower().find('01_clocation')             != -1: index = 2
    if item.lower().find('01_fclocation')            != -1: index = 3
    if item.lower().find('02_density')               != -1: index = 4
    if item.lower().find('02_cdensity')              != -1: index = 5
    if item.lower().find('02_fcdensity')             != -1: index = 6
    if item.lower().find('03_matrix')                != -1: index = 7
    if item.lower().find('04_matrix_home_work')      != -1: index = 8
    if item.lower().find('05_corr_metro')            != -1: index = 9
    if item.lower().find('06_matrix_dom')            != -1: index = 10
    if item.lower().find('07_dachnik')               != -1: index = 11
    if item.lower().find('08_externalworkers')       != -1: index = 12
    if item.lower().find('09_times')                 != -1: index = 13
    if item.lower().find('10_transit')               != -1: index = 14
    if item.lower().find('11_cmatrix_metro')         != -1: index = 15
    return index
    

#функция получения списка файлов
def getFileList(rm, path, monthList, reports):
    sep = getPathSep()
    fileList = []
    for month in monthList:
        month = str(month)
        listdir = os.listdir(path + sep + month)
        if rm == '2015':
            listdir.sort(key=sortListDir2015)
        elif rm == '2018':
            listdir.sort(key=sortListDir2018)
        for fileName in listdir:
            if os.path.isfile(path + sep + month + sep + fileName) is True:
                if isMD5File(fileName) is not True:
                    originFilePath = path + sep + month + sep + fileName
                    originFileExt = getFileExt(fileName)
                    fileType = getFileType(rm, fileName)
                    fileIter = getFileIter(fileName)
                    fileMonth = month
                    if fileType in reports:
                        fileList.append((originFilePath, originFileExt, fileType, fileIter, fileMonth))
    return fileList 
                

#функция бинарного копирования
def copy(originFilePath, outFilePath):
    f_in = open(originFilePath, 'rb')
    f_out = open(outFilePath, 'wb')
    shutil.copyfileobj(f_in, f_out)
    f_in.close()
    f_out.close()
    

def copy_gz_to_csv(originFilePath, outFilePath):
    f_in = gzip.open(originFilePath, 'rb')
    f_out = open(outFilePath, 'wb')
    shutil.copyfileobj(f_in, f_out)
    f_in.close()
    f_out.close()    


def copy_csv_to_gz(originFilePath, outFilePath):
    p = platform.architecture()
    o = p[1].lower()
    b = p[0].lower()
    if o.find('windows') != -1:
        if b == '32bit':
            os.system(os.getcwd() + '\\7z\\7za.exe a -tgzip -ssw -mx5 ' + outFilePath + ' ' + originFilePath + ' > nul')
        elif b == '64bit':
            os.system(os.getcwd() + '\\7z\\x64\\7za.exe a -tgzip -ssw -mx4 ' + outFilePath + ' ' + originFilePath + ' > nul')
        
    
def repack(attr, d, lock):
    if attr['fileExt'] == 'csv' and attr['outFileExt'] == 'csv':
        copy(attr['originFilePath'], attr['outFilePath'])
    elif attr['fileExt'] == 'gz' and attr['outFileExt'] == 'csv.gz':
        copy(attr['originFilePath'], attr['outFilePath'])
    elif attr['fileExt'] == 'gz' and attr['outFileExt'] == 'csv':
        copy_gz_to_csv(attr['originFilePath'], attr['outFilePath'])
    elif attr['fileExt'] == 'csv' and attr['outFileExt'] == 'csv.gz':
        copy_csv_to_gz(attr['originFilePath'], attr['outFilePath'])
    

def recode(attr, ad, cd, td, d, lock):
    if attr['rm'] == '2015':
        if attr['fileType'] == '01_Location'         : transformLine, rd = transformLocation2015Line, ad
        if attr['fileType'] == '01_CLocation'        : transformLine, rd = transformCLocation2015Line, cd
        if attr['fileType'] == '01_fCLocation'       : transformLine, rd = transformfCLocation2015Line, cd
        if attr['fileType'] == '02_Density'          : transformLine, rd = transformDensity2015Line, ad
        if attr['fileType'] == '02_CDensity'         : transformLine, rd = transformCDensity2015Line, cd
        if attr['fileType'] == '02_fCDensity'        : transformLine, rd = transformfCDensity2015Line, cd
        if attr['fileType'] == '03_Matrix'           : transformLine, rd = transformMatrix2015Line, ad
        if attr['fileType'] == '04_Matrix_Home_Work' : transformLine, rd = transformMatrixHMWK2015Line, ad
        if attr['fileType'] == '05_Corr_Metro'       : transformLine, rd = transformCorrMetro2015Line, None
        if attr['fileType'] == '06_Matrix_Dom'       : transformLine, rd = transformMatrixDom2015Line, ad
        if attr['fileType'] == '07_Dachnik'          : transformLine, rd = transformDachnik2015Line, ad
        if attr['fileType'] == '08_ExternalWorkers'  : transformLine, rd = transformExternalWorkers2015Line, ad
        if attr['fileType'] == '09_Times'            : transformLine, rd = transformTimes2015Line, ad
        if attr['fileType'] == '10_Transit'          : transformLine, rd = transformTransit2015Line, ad
        if attr['fileType'] == '11_CMatrix_Metro'    : transformLine, rd = transformCMatrixMetro2015Line, cd
            
            
    elif attr['rm'] == '2018':
        if attr['fileType'] == '01_Location'             : transformLine, rd = transformLocation2018Line, ad
        if attr['fileType'] == '01_CLocation'            : transformLine, rd = transformLocation2018Line, cd
        if attr['fileType'] == '01_TLocation'            : transformLine, rd = transformLocation2018Line, td
        if attr['fileType'] == '01_CLocation_types'      : transformLine, rd = transformCLocation_types2018Line, cd
        if attr['fileType'] == '02_Density'              : transformLine, rd = transformDensity2018Line, ad
        if attr['fileType'] == '02_CDensity'             : transformLine, rd = transformDensity2018Line, cd
        if attr['fileType'] == '02_TDensity'             : transformLine, rd = transformDensity2018Line, td
        if attr['fileType'] == '02_CDensity_types'       : transformLine, rd = transformCDensity_types2018Line, cd
        if attr['fileType'] == '03_Matrix'               : transformLine, rd = transformMatrix2018Line, ad
        if attr['fileType'] == '03_CMatrix'              : transformLine, rd = transformMatrix2018Line, cd
        if attr['fileType'] == '03_TMatrix'              : transformLine, rd = transformMatrix2018Line, td
        if attr['fileType'] == '04_Matrix_Home_Work'     : transformLine, rd = transformMatrixHomeWork2018Line, ad
        if attr['fileType'] == '04_CMatrix_Home_Work'    : transformLine, rd = transformMatrixHomeWork2018Line, cd
        if attr['fileType'] == '04_TMatrix_Home_Work'    : transformLine, rd = transformMatrixHomeWork2018Line, td
        if attr['fileType'] == '05_Corr_Metro'           : transformLine, rd = transformCorrMetro2018Line, None
        if attr['fileType'] == '09_Times'                : transformLine, rd = transformTimes2018Line, ad
        if attr['fileType'] == '09_Times_Holiday'        : transformLine, rd = transformTimes2018Line, ad
        if attr['fileType'] == '09_CTimes'               : transformLine, rd = transformTimes2018Line, cd
        if attr['fileType'] == '09_CTimes_Holiday'       : transformLine, rd = transformTimes2018Line, cd
        if attr['fileType'] == '11_CMatrix_Metro'        : transformLine, rd = transformCMatrixMetro2018Line, cd
        if attr['fileType'] == '11_CMatrix_Metro_Holiday': transformLine, rd = transformCMatrixMetro2018Line, cd
    #
    if attr['fileExt'] == 'csv':
        f_in = open(attr['originFilePath'], 'rt')
    elif attr['fileExt'] == 'gz':
        f_in = gzip.open(attr['originFilePath'], 'rt')
    f_out = open(attr['tempFilePath'], 'wt')
    header = f_in.readline()
    f_out.write(header)
    for line in f_in:
        if line != '':
            line = transformLine(line, rd)
        f_out.write(line)
    f_in.close()
    f_out.close()
    #
    if attr['outFileExt'] == 'csv':
        copy(attr['tempFilePath'], attr['outFilePath'])
    elif attr['outFileExt'] == 'csv.gz':
        copy_csv_to_gz(attr['tempFilePath'], attr['outFilePath'])
    #
    os.remove(attr['tempFilePath'])
    
    
#функция рассчёта MD5 хеша файла
def getMD5Hash(filePath):
    f = open(filePath, 'rb')
    md5sum = hashlib.md5()
    while True:
        chunk = f.read(8192)
        if not chunk:
            break
        md5sum.update(chunk)
    f.close()
    return md5sum.hexdigest()    
    
    
# функция рассчёта и создания файла с md5 хешем
def createMD5File(filePath):
    sep = getPathSep()
    fileName = filePath.split(sep)[-1]
    MD5Hash = getMD5Hash(filePath)
    MD5FilePath = filePath + '.md5'
    digest = MD5Hash + ' *' +  fileName + '\r\n'
    f = open(MD5FilePath, 'wt')
    f.write(digest)
    f.close()
    

def getCounterDict(REPORTS, MONTHLIST):
    d = {}
    for report in REPORTS:
        for month in MONTHLIST:
            d[report+str(month)] = False
    return d


def getOutputTemplate(RM, REPORTS, MONTHLIST, t):
    outputTemplate = []
    timerStr = '%s'%t + ': %s'
    outputTemplate.append(timerStr)
    headerStr = ' ' + '_' * 16 + '|'
    for month in MONTHLIST:
        headerStr += str(month) + '|'
    outputTemplate.append(headerStr)
    for report in REPORTS:
        if RM == '2015':
            line = const2015.LINES[report]
        elif RM == '2018':
            line = const2018.LINES[report]
        for month in MONTHLIST:
            line += '  %2s  |'
        outputTemplate.append(line)
    return outputTemplate
    

def progressViewer(mode, timer, state, RM, REPORTS, MONTHLIST, d, t):
    outputTemplate = getOutputTemplate(RM, REPORTS, MONTHLIST, t)
    startTime = datetime.now()
    flag = True
    with output(initial_len=len(REPORTS)+2, interval=0) as outputlines:
        while flag is True:
            currentTime = datetime.now()
            outputlines[0] = outputTemplate[0] % str(currentTime - startTime)
            outputlines[1] = outputTemplate[1]
            i = 2
            for report in REPORTS:
                values = []
                for month in MONTHLIST:
                    if d[report+str(month)] == False:
                        value = '  '
                    else:
                        value = '++'
                    values.append(value)
                outputlines[i] = outputTemplate[i] % tuple(values)
                i += 1
            #
            if mode == 'window':
                t = currentTime - startTime
                s = outputlines[1:]
                s = '\n'.join(s)
                print(t)
                print(s)
                timer.emit(str(t))
                state.emit(s)
            if all(d.values()) is True: flag = False
            time.sleep(0.3)


def getNewAzid2015(zid, rd):
    if zid == '-1' or int(zid) > 200000:
        pass
    elif zid in const2015.SKIPZIDS:
        zid = None
    else:
        zid = rd[zid]
    return zid

            
def transformLocation2015Line(line, rd):
    tokens = line.split(';')
    tokens[1] = getNewAzid2015(tokens[1], rd)
    if None in tokens:
        line = ''
    else:
        line = ';'.join(tokens)
    return line


def transformCLocation2015Line(line, rd):
    tokens = line.split(';')
    tokens[1] = rd[tokens[1]]
    line = ';'.join(tokens)
    return line


def transformfCLocation2015Line(line, rd):
    tokens = line.split(';')
    tokens[2] = rd[tokens[2]]
    line = ';'.join(tokens)
    return line


def transformDensity2015Line(line, rd):
    tokens = line.split(';')
    tokens[1] = getNewAzid2015(tokens[1], rd)
    if None in tokens:
        line = ''
    else:
        line = ';'.join(tokens)
    return line
    
    
def transformCDensity2015Line(line, rd):
    tokens = line.split(';')
    tokens[1] = rd[tokens[1]]
    line = ';'.join(tokens)
    return line


def transformfCDensity2015Line(line, rd):
    tokens = line.split(';')
    tokens[2] = rd[tokens[2]]
    line = ';'.join(tokens)
    return line
    

def transformMatrix2015Line(line, rd):
    tokens = line.split(';')
    tokens[1] = getNewAzid2015(tokens[1], rd)
    tokens[2] = getNewAzid2015(tokens[2], rd)
    if None in tokens:
        line = ''
    else:
        line = ';'.join(tokens)
    return line
    

def transformMatrixHMWK2015Line(line, rd):
    tokens = line.split(';')
    tokens[1] = getNewAzid2015(tokens[1], rd)
    tokens[2] = getNewAzid2015(tokens[2], rd)
    if None in tokens:
        line = ''
    else:
        line = ';'.join(tokens)
    return line
    
    
def transformCorrMetro2015Line(line, rd):
    return line
    
        
def transformMatrixDom2015Line(line, rd):
    tokens = line.split(';')
    tokens[2] = getNewAzid2015(tokens[2], rd)
    tokens[3] = getNewAzid2015(tokens[3], rd)
    if None in tokens:
        line = ''
    else:
        line = ';'.join(tokens)
    return line


def transformDachnik2015Line(line, rd):
    tokens = line.split(';')
    tokens[1] = getNewAzid2015(tokens[1], rd)
    if None in tokens:
        line = ''
    else:
        line = ';'.join(tokens)
    return line


def transformExternalWorkers2015Line(line, rd):
    tokens = line.split(';')
    tokens[1] = getNewAzid2015(tokens[1], rd)
    if None in tokens:
        line = ''
    else:
        line = ';'.join(tokens)
    return line


def transformTimes2015Line(line, rd):
    tokens = line.split(';')
    tokens[1] = getNewAzid2015(tokens[1], rd)
    tokens[2] = getNewAzid2015(tokens[2], rd)
    if None in tokens:
        line = ''
    else:
        line = ';'.join(tokens)
    return line


def transformTransit2015Line(line, rd):
    tokens = line.split(';')
    tokens[1] = getNewAzid2015(tokens[1], rd)
    tokens[2] = getNewAzid2015(tokens[2], rd)
    if None in tokens:
        line = ''
    else:
        line = ';'.join(tokens)
    return line


def transformCMatrixMetro2015Line(line, rd):
    tokens = line.split(';')
    tokens[2] = rd[tokens[2]]
    line = ';'.join(tokens)
    return line

####

def transformLocation2018Line(line, rd):
    tokens = line.split(';')
    tokens[1] = rd[tokens[1]]
    line = ';'.join(tokens)
    return line


def transformCLocation_types2018Line(line, rd):
    tokens = line.split(';')
    tokens[2] = rd[tokens[2]]
    line = ';'.join(tokens)
    return line
    

def transformDensity2018Line(line, rd):
    tokens = line.split(';')
    tokens[1] = rd[tokens[1]]
    tokens[2] = rd[tokens[2]]
    line = ';'.join(tokens)
    return line

def transformCDensity_types2018Line(line, rd):
    tokens = line.split(';')
    tokens[2] = rd[tokens[2]]
    tokens[3] = rd[tokens[3]]
    line = ';'.join(tokens)
    return line


def transformMatrix2018Line(line, rd):
    tokens = line.split(';')
    tokens[1] = rd[tokens[1]]
    tokens[2] = rd[tokens[2]]
    tokens[3] = rd[tokens[3]]
    line = ';'.join(tokens)
    return line


def transformMatrixHomeWork2018Line(line, rd):
    tokens = line.split(';')
    tokens[1] = rd[tokens[1]]
    tokens[2] = rd[tokens[2]]
    line = ';'.join(tokens)
    return line


def transformCorrMetro2018Line(line, rd):
    return line


def transformTimes2018Line(line, rd):
    tokens = line.split(';')
    tokens[1] = rd[tokens[1]]
    tokens[2] = rd[tokens[2]]
    line = ';'.join(tokens)
    return line


def transformCMatrixMetro2018Line(line, rd):
    tokens = line.split(';')
    tokens[2] = rd[tokens[2]]
    line = ';'.join(tokens)
    return line

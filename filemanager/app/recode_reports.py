#-*- coding: utf-8 -*-

from supfuncs import getFileList, getPathSep, cleandir, recode, createMD5File, progressViewer, getCounterDict
from multiprocessing import Process, Pool, Manager, Lock
import os
import time


def getOutParams(RM, fileList, OUTPATH, TEMPDIRPATH, EXTDICT):
    newFileList = []
    sep = getPathSep()
    for file in fileList:
        a = {}
        a['rm'] = RM
        a['originFilePath'] = file[0]
        a['fileExt'] = file[1]
        a['fileType'] = file[2]
        a['fileIter'] = file[3]
        a['fileMonth'] = file[4]
        if EXTDICT[a['fileType']] == 'gz':
            a['outFileExt'] = 'csv.gz'
        elif EXTDICT[a['fileType']] == 'csv':
            a['outFileExt'] = 'csv'
        a['outDirPath'] = OUTPATH + sep + a['fileMonth']
        a['tempDirPath'] = TEMPDIRPATH
        a['outFilePath'] = a['outDirPath'] + sep + a['fileType'] + '_' + a['fileIter'] + '_' + a['fileMonth'] + '.' + a['outFileExt']
        a['tempFilePath'] = a['tempDirPath'] + sep + a['fileType'] + '_' + a['fileIter'] + '_' + a['fileMonth'] + '.' + 'csv'
        newFileList.append(a)
    return newFileList


def recodeOneReport(attr, ad, cd, td, d, lock):
    os.makedirs(attr['outDirPath'], exist_ok=True)
    recode(attr, ad, cd, td, d, lock)
    createMD5File(attr['outFilePath'])
    #
    with lock: d[attr['fileType']+attr['fileMonth']] = True
    time.sleep(1)
    
def readReplaceDict(RM, REPALCEDICTPATH):
    with open(REPALCEDICTPATH['azones'], 'rt') as f:
        ad = {}
        for line in f.readlines():
            line = line.replace('\r','').replace('\n','')
            if line != '':
                key, value = line.split(';')
                ad[key] = value
        f.close()
    with open(REPALCEDICTPATH['czones'], 'rt') as f:
        cd = {}
        for line in f.readlines():
            line = line.replace('\r','').replace('\n','')
            if line != '':
                key, value = line.split(';')
                cd[key] = value
        f.close()
    if RM == '2015':
        td = None
    if RM == '2018':
        with open(REPALCEDICTPATH['tzones'], 'rt') as f:
            td = {}
            for line in f.readlines():
                line = line.replace('\r','').replace('\n','')
                if line != '':
                    key, value = line.split(';')
                    td[key] = value
            f.close()
    return ad, cd, td
    
    
def recodeReports(RM, PROCESSES, PATH, OUTPATH, TEMPDIRPATH, MONTHLIST, REPORTS, EXTDICT, REPLACEDICTPATH, mode='console', timer=None, state=None):
    os.system('cls')
    cleandir(TEMPDIRPATH)
    fileList = getFileList(RM, PATH, MONTHLIST, REPORTS)
    fileList = getOutParams(RM, fileList, OUTPATH, TEMPDIRPATH, EXTDICT)
    #
    ad, cd, td = readReplaceDict(RM, REPLACEDICTPATH)
    #
    m = Manager()
    lock = m.Lock()
    d = m.dict()
    d.update(getCounterDict(REPORTS, MONTHLIST))
    process = Process(target=progressViewer, args=(mode, timer, state, RM, REPORTS, MONTHLIST, d, 'Кодирование отчётов'))
    pool = Pool(PROCESSES)
    #
    process.start()
    pool.starmap(recodeOneReport, [(attr, ad, cd, td, d, lock) for attr in fileList])
    pool.close()
    pool.join()
    process.join()
    #
    cleandir(TEMPDIRPATH)
    
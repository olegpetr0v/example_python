#-*- coding: utf-8 -*-

from supfuncs import getFileList, getPathSep, repack, cleandir, createMD5File
from supfuncs import getCounterDict, progressViewer
from multiprocessing import Process, Pool, Manager, Lock
import os
import time


def getOutParams(RM, fileList, OUTPATH, EXTDICT):
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
        a['outFilePath'] = a['outDirPath'] + sep + a['fileType'] + '_' + a['fileIter'] + '_' + a['fileMonth'] + '.' + a['outFileExt']
        newFileList.append(a)
    return newFileList


def repackOneReport(attr, d, lock):
    os.makedirs(attr['outDirPath'], exist_ok=True)
    repack(attr, d, lock)
    createMD5File(attr['outFilePath'])
    #
    with lock: d[attr['fileType']+attr['fileMonth']] = True
    time.sleep(1)


def repackReports(RM, PROCESSES, PATH, OUTPATH, TEMPDIRPATH, MONTHLIST, REPORTS, EXTDICT, mode='console', timer=None, state=None):
    os.system('cls')
    cleandir(TEMPDIRPATH)
    fileList = getFileList(RM, PATH, MONTHLIST, REPORTS)
    fileList = getOutParams(RM, fileList, OUTPATH, EXTDICT)
    #
    m = Manager()
    lock = m.Lock()
    d = m.dict()
    d.update(getCounterDict(REPORTS, MONTHLIST))
    process = Process(target=progressViewer, args=(mode, timer, state, RM, REPORTS, MONTHLIST, d, 'Переупаковка отчётов'))
    pool = Pool(PROCESSES)
    #
    process.start()
    pool.starmap(repackOneReport, [(attr, d, lock) for attr in fileList])
    pool.close()
    pool.join()
    process.join()   
    #
    cleandir(TEMPDIRPATH)
    
#-*- coding: utf-8 -*-

from supfuncs import getFileList, getPathSep, copy, createMD5File, getCounterDict, progressViewer
from multiprocessing import Process, Pool, Manager, Lock
import os
import time


def getOutParams(RM, fileList, OUTPATH):
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
        if a['fileExt'] == 'gz':
            a['outFileExt'] = 'csv.gz'
        else:
            a['outFileExt'] = 'csv'
        a['outDirPath'] = OUTPATH + sep + a['fileMonth']
        a['outFilePath'] = a['outDirPath'] + sep + a['fileType'] + '_' + a['fileIter'] + '_' + a['fileMonth'] + '.' + a['outFileExt']
        newFileList.append(a)
    return newFileList


def copyOneReport(attr, d, lock):
    os.makedirs(attr['outDirPath'], exist_ok=True)
    copy(attr['originFilePath'], attr['outFilePath'])
    createMD5File(attr['outFilePath'])
    #
    with lock: d[attr['fileType']+attr['fileMonth']] = True
    time.sleep(1)
    
    
def copyReports(RM, PROCESSES, PATH, OUTPATH, TEMPDIRPATH, MONTHLIST, REPORTS, EXTDICT, mode='console', timer=None, state=None):
    #os.system('cls')
    fileList = getFileList(RM, PATH, MONTHLIST, REPORTS)
    fileList = getOutParams(RM, fileList, OUTPATH)
    #
    m = Manager()
    lock = m.Lock()
    d = m.dict()
    d.update(getCounterDict(REPORTS, MONTHLIST))
    #process = Process(target=progressViewer, args=(mode, timer, state, RM, REPORTS, MONTHLIST, d, 'Копирование отчётов'))
    pool = Pool(PROCESSES)
    #
    #process.start()
    pool.starmap(copyOneReport, [(attr, d, lock) for attr in fileList])
    progressViewer(mode, timer, state, RM, REPORTS, MONTHLIST, d, 'Копирование отчётов')
    pool.close()
    pool.join()
    #process.join()
    
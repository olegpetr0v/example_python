# -*- coding: utf-8 -*-

import sys
import os
import time
from PyQt5 import QtCore, QtWidgets

import configUI

from copy_reports import *
from repack_reports import *
from recode_reports import *


class processThread(QtCore.QThread):
    timer = QtCore.pyqtSignal(str)
    state = QtCore.pyqtSignal(str)
    params = {}
    
    def run(self):
        p = self.params
        if p['RM'] == '2015':
            if p['COPY'] == True and p['REPACK'] == True and p['RECODE'] == True:
                recodeReports(p['RM'], p['PROCESSES'], p['PATH'], p['OUTPATH'], p['TEMPDIRPATH'], p['MONTHLIST2015'], p['REPORTS2015'], p['EXTDICT'], p['REPLACEDICTPATH2015'], mode='window', timer=self.timer, state=self.state)
            elif p['COPY'] == True and p['REPACK'] == True and p['RECODE'] == False:
                repackReports(p['RM'], p['PROCESSES'], p['PATH'], p['OUTPATH'], p['TEMPDIRPATH'], p['MONTHLIST2015'], p['REPORTS2015'], p['EXTDICT2015'], mode='window', timer=self.timer, state=self.state)
            elif p['COPY'] == True and p['REPACK'] == False and p['RECODE'] == False:
                copyReports(p['RM'], p['PROCESSES'], p['PATH'], p['OUTPATH'], p['TEMPDIRPATH'], p['MONTHLIST2015'], p['REPORTS2015'], p['EXTDICT2015'], mode='window', timer=self.timer, state=self.state)
        elif p['RM'] == '2018':
            if p['COPY'] == True and p['REPACK'] == True and p['RECODE'] == True:
                recodeReports(p['RM'], p['PROCESSES'], p['PATH'], p['OUTPATH'], p['TEMPDIRPATH'], p['MONTHLIST2018'], p['REPORTS2018'], p['EXTDICT2018'], p['REPLACEDICTPATH2018'], mode='window', timer=self.timer, state=self.state)
            elif p['COPY'] == True and p['REPACK'] == True and p['RECODE'] == False:
                repackReports(p['RM'], p['PROCESSES'], p['PATH'], p['OUTPATH'], p['TEMPDIRPATH'], p['MONTHLIST2018'], p['REPORTS2018'], p['EXTDICT2018'], mode='window', timer=self.timer, state=self.state)
            elif p['COPY'] == True and p['REPACK'] == False and p['RECODE'] == False:
                copyReports(p['RM'], p['PROCESSES'], p['PATH'], p['OUTPATH'], p['TEMPDIRPATH'], p['MONTHLIST2018'], p['REPORTS2018'], p['EXTDICT2018'], mode='window', timer=self.timer, state=self.state)
        

class configWindow(QtWidgets.QMainWindow, configUI.Ui_MainWindow):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        #
        self.labelWorkRegime.setEnabled(False)
        self.labelTimer.setEnabled(False)
        self.labelState.setEnabled(False)
        self.pushButtonStop.setEnabled(False)
        self.tabWidgetState.setCurrentIndex(0)
        #
        self.radioButtonCopy.toggled.connect(lambda:self.groupBoxRegimeState(self.radioButtonCopy, self.radioButtonRepack, self.radioButtonRecode))
        self.radioButtonRepack.toggled.connect(lambda:self.groupBoxRegimeState(self.radioButtonCopy, self.radioButtonRepack, self.radioButtonRecode))
        self.radioButtonRecode.toggled.connect(lambda:self.groupBoxRegimeState(self.radioButtonCopy, self.radioButtonRepack, self.radioButtonRecode))
        self.radioButtonCopy.setChecked(True)
        #
        self.pushButtonInDir.clicked.connect(self.browseInputFolder)
        self.pushButtonTempDir.clicked.connect(self.browseTempFolder)
        self.pushButtonOutDir.clicked.connect(self.browseOutFolder)
        #
        self.pushButtonAdmDict2015.clicked.connect(self.browseAdmDict2015)
        self.pushButtonCellsDict2015.clicked.connect(self.browseCellsDict2015)
        self.pushButtonAdmDict2018.clicked.connect(self.browseAdmDict2018)
        self.pushButtonCellsDict2018.clicked.connect(self.browseCellsDict2018)
        self.pushButtonTrDict2018.clicked.connect(self.browseTrDict2018)
        #
        self.pushButtonCheckAllDates2015.clicked.connect(self.selectAllDates2015)
        self.pushButtonUncheckAllDates2015.clicked.connect(self.unselectAllDates2015)
        #
        self.pushButtonCheckAllDates2018.clicked.connect(self.selectAllDates2018)
        self.pushButtonUncheckAllDates2018.clicked.connect(self.unselectAllDates2018)
        #
        self.pushButtonCheckAllReports2015.clicked.connect(self.selectAllReports2015)
        self.pushButtonUncheckAllReports2015.clicked.connect(self.unselectAllReports2015)
        self.pushButtonCheckAllReports2018.clicked.connect(self.selectAllReports2018)
        self.pushButtonUncheckAllReports2018.clicked.connect(self.unselectAllReports2018)
        #
        self.pushButtonSetGZ2015.clicked.connect(self.setAllGZ2015)
        self.pushButtonSetCSV2015.clicked.connect(self.setAllCSV2015)
        self.pushButtonSetGZ2018.clicked.connect(self.setAllGZ2018)
        self.pushButtonSetCSV2018.clicked.connect(self.setAllCSV2018)
        #
        self.pushButtonStart.clicked.connect(self.start)
        #self.pushButtonStop.clicked.connect(self.refresh)
       
    def start(self):
        check, info, params = self.checkConfig()
        if check == False:
            QtWidgets.QMessageBox().warning(self, 'Неправильная кофигурация', info, QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
        else:
            self.activateStateTab()
            self.thread = processThread()
            self.thread.params = params
            self.thread.timer.connect(self.updateTimer)
            self.thread.state.connect(self.updateState)
            self.thread.finished.connect(self.deactivateStateTab)
            self.thread.start()
            
    def updateTimer(self, value):
        self.labelTimer.setText(value)
    
    def updateState(self, value):
        self.labelState.setText(value)        
    
    def deactivateStateTab(self):
        self.groupBoxRegime.setEnabled(False)
        self.groupBoxDir.setEnabled(False)
        self.groupBoxProcess.setEnabled(False)
        self.tabWidgetVersion.setEnabled(False)
        self.pushButtonStart.setEnabled(False)
        self.pushButtonStop.setEnabled(True)
        self.labelWorkRegime.setEnabled(False)
        self.labelWorkRegime.setEnabled(False)
        self.labelTimer.setEnabled(False)
        self.labelState.setEnabled(False)
        
    def activateStateTab(self):
        self.groupBoxRegime.setEnabled(False)
        self.groupBoxDir.setEnabled(False)
        self.groupBoxProcess.setEnabled(False)
        self.tabWidgetVersion.setEnabled(False)
        self.pushButtonStart.setEnabled(False)
        self.pushButtonStop.setEnabled(True)
        if self.radioButtonCopy.isChecked() == True:
            self.labelWorkRegime.setText('Копирование')
        if self.radioButtonRepack.isChecked() == True:
            self.labelWorkRegime.setText('Упаковка')
        if self.radioButtonRecode.isChecked() == True:
            self.labelWorkRegime.setText('Кодирование')
        self.labelWorkRegime.setEnabled(True)
        self.labelTimer.setEnabled(True)
        self.labelState.setEnabled(True)
        self.tabWidgetState.setCurrentIndex(1)
    
    def checkInputDir(self):
        path = self.labInputDir.text()
        return os.path.isdir(path)
    
    def checkTempDir(self):
        path = self.labTempDir.text()
        return os.path.isdir(path)
    
    def checkOutDir(self):
        path = self.labOutDir.text()
        return os.path.isdir(path)
    
    def checkNumberProcess(self):
        number = self.lineEditNimberProcess.text()
        return number.isdigit()
    
    def checkAdmDict2015(self):
        path = self.labAdmDict2015.text()
        return os.path.isfile(path)
    
    def checkCellsDict2015(self):
        path = self.labCellsDict2015.text()
        return os.path.isfile(path)
   
    def checkAdmDict2018(self):
        path = self.labAdmDict2018.text()
        return os.path.isfile(path)
    
    def checkCellsDict2018(self):
        path = self.labCellsDict2018.text()
        return os.path.isfile(path)
    
    def checkTrDict2018(self):
        path = self.labTrDict2018.text()
        return os.path.isfile(path)
        
    def checkConfigCopy(self):
        info = ''
        if self.checkInputDir() == False:
            info += 'Не задана директория исходных отчётов.\n'
        if self.checkOutDir() == False:
            info += 'Не задана директория выходных отчётов.\n'
        if self.checkNumberProcess() == False:
            info += 'Не задано количество параллельных процессов.\n'
        if self.tabWidgetVersion.currentIndex() == 0:
            if self.checkCheckedReportsAndDates2015() == False:
                info += 'Не выбраны отчёты.\n'
        elif self.tabWidgetVersion.currentIndex() == 1:
            if self.checkCheckedReportsAndDates2018() == False:
                info += 'Не выбраны отчёты.\n'
        if info == '':
            return True, None
        else:
            return False, info  

    def checkConfigRepack(self):
        info = ''
        if self.checkInputDir() == False:
            info += 'Не задана директория исходных отчётов.\n'
        if self.checkTempDir() == False:
            info += 'Не задана директория временных файлов.\n'
        if self.checkOutDir() == False:
            info += 'Не задана директория выходных отчётов.\n'
        if self.checkNumberProcess() == False:
            info += 'Не задано количество параллельных процессов.\n'
        if self.tabWidgetVersion.currentIndex() == 0:
            if self.checkCheckedReportsAndDates2015() == False:
                info += 'Не выбраны отчёты.\n'
        elif self.tabWidgetVersion.currentIndex() == 1:
            if self.checkCheckedReportsAndDates2018() == False:
                info += 'Не выбраны отчёты.\n'
        if info == '':
            return True, None
        else:
            return False, info
        
    def checkConfigRecode(self):
        info = ''
        if self.checkInputDir() == False:
            info += 'Не задана директория исходных отчётов.\n'
        if self.checkTempDir() == False:
            info += 'Не задана директория временных файлов.\n'
        if self.checkOutDir() == False:
            info += 'Не задана директория выходных отчётов.\n'
        if self.checkNumberProcess() == False:
            info += 'Не задано количество параллельных процессов.\n'
        if self.tabWidgetVersion.currentIndex() == 0:
            if self.checkAdmDict2015() == False:
                info += 'Не задан словарь перекодировки административных районов.\n'
            if self.checkCellsDict2015() == False:
                info += 'Не задан словарь перекодировки ячеек 500х500.\n'
            if self.checkCheckedReportsAndDates2015() == False:
                info += 'Не выбраны отчёты.\n'
        elif self.tabWidgetVersion.currentIndex() == 1:
            if self.checkAdmDict2018() == False:
                info += 'Не задан словарь перекодировки административных районов.\n'
            if self.checkCellsDict2018() == False:
                info += 'Не задан словарь перекодировки ячеек 500х500.\n'
            if self.checkTrDict2018() == False:
                info += 'Не задан словарь перекодировки транспортных районов.\n'
            if self.checkCheckedReportsAndDates2018() == False:
                info += 'Не выбраны отчёты.\n'
        if info == '':
            return True, None
        else:
            return False, info
    
    def collectParams(self):
        params = {}
        params['PROCESSES'] = int(self.lineEditNimberProcess.text())
        params['PATH'] = self.labInputDir.text()
        params['TEMPDIRPATH'] = self.labTempDir.text()
        params['OUTPATH'] = self.labOutDir.text()
        if self.tabWidgetVersion.currentIndex() == 0:
            params['RM'] = '2015'
        elif self.tabWidgetVersion.currentIndex() == 1:
            params['RM'] = '2018'
        if self.radioButtonCopy.isChecked() == True:
            params['COPY'], params['REPACK'], params['RECODE'] = True, False, False
        elif self.radioButtonRepack.isChecked() == True:
            params['COPY'], params['REPACK'], params['RECODE'] = True, True, False
        elif self.radioButtonRecode.isChecked() == True:
            params['COPY'], params['REPACK'], params['RECODE'] = True, True, True
        params['MONTHLIST2015'] = self.getMonthList2015()
        params['REPORTS2015'] = self.getReports2015()
        params['EXTDICT2015'] = self.getExtDict2015()
        params['MONTHLIST2018'] = self.getMonthList2018()
        params['REPORTS2018'] = self.getReports2018()
        params['EXTDICT2018'] = self.getExtDict2018()
        params['REPLACEDICTPATH2015'] = self.getReplaceDictPath2015()
        params['REPLACEDICTPATH2018'] = self.getReplaceDictPath2018()
        return params
    
    def getReplaceDictPath2015(self):
        pathes = {}
        pathes['azones'] = self.labAdmDict2015.text()
        pathes['czones'] = self.labCellsDict2015.text()
        return pathes
    
    def getReplaceDictPath2018(self):
        pathes = {}
        pathes['azones'] = self.labAdmDict2018.text()
        pathes['czones'] = self.labCellsDict2018.text()
        pathes['tzones'] = self.labTrDict2018.text()
        return pathes
    
    def checkConfig(self):
        if self.radioButtonCopy.isChecked() == True:
            check, info = self.checkConfigCopy()
        elif self.radioButtonRepack.isChecked() == True:
            check, info = self.checkConfigRepack()
        elif self.radioButtonRecode.isChecked() == True:
            check, info = self.checkConfigRecode()
        if check == True:
            params = self.collectParams()
        else:
            params = None
        return check, info, params
    
    def getReports2015(self):
        reports = []
        if self.checkBox01_Location2015.isChecked(): reports.append('01_Location')
        if self.checkBox01_CLocation2015.isChecked(): reports.append('01_CLocation')
        if self.checkBox01_fCLocation2015.isChecked(): reports.append('01_fCLocation')
        if self.checkBox02_Density2015.isChecked(): reports.append('02_Density')
        if self.checkBox02_CDensity2015.isChecked(): reports.append('02_CDensity')
        if self.checkBox02_fCDensity2015.isChecked(): reports.append('02_fCDensity')
        if self.checkBox03_Matrix2015.isChecked(): reports.append('03_Matrix')
        if self.checkBox04_Matrix_HMWK2015.isChecked(): reports.append('04_Matrix_Home_Work')
        if self.checkBox05_Corr_Metro2015.isChecked(): reports.append('05_Corr_Metro')
        if self.checkBox06_MatrixDom2015.isChecked(): reports.append('06_Matrix_Dom')
        if self.checkBox07_Dachnik2015.isChecked(): reports.append('07_Dachnik')
        if self.checkBox08_ExternalW2015.isChecked(): reports.append('08_ExternalWorkers')
        if self.checkBox09_Times2015.isChecked(): reports.append('09_Times')
        if self.checkBox10_Transit2015.isChecked(): reports.append('10_Transit')
        if self.checkBox11_CMatrixM2015.isChecked(): reports.append('11_CMatrix_Metro')
        return reports
    
    def getReports2018(self):
        reports = []
        if self.checkBox01_Location2018.isChecked(): reports.append('01_Location')
        if self.checkBox01_CLocation2018.isChecked(): reports.append('01_CLocation')
        if self.checkBox01_TLocation2018.isChecked(): reports.append('01_TLocation')
        if self.checkBox01_CLocation_t2018.isChecked(): reports.append('01_CLocation_types')
        if self.checkBox02_Density2018.isChecked(): reports.append('02_Density')
        if self.checkBox02_CDensity2018.isChecked(): reports.append('02_CDensity')
        if self.checkBox02_TDensity2018.isChecked(): reports.append('02_TDensity')
        if self.checkBox02_CDensity_t2018.isChecked(): reports.append('02_CDensity_types')
        if self.checkBox03_Matrix2018.isChecked(): reports.append('03_Matrix')
        if self.checkBox03_CMatrix2018.isChecked(): reports.append('03_CMatrix')
        if self.checkBox03_TMatrix2018.isChecked(): reports.append('03_TMatrix')
        if self.checkBox04_Matrix_HMWK2018.isChecked(): reports.append('04_Matrix_Home_Work')
        if self.checkBox04_CMatrix_HMWK2018.isChecked(): reports.append('04_CMatrix_Home_Work')
        if self.checkBox04_TMatrix_HMWK2018.isChecked(): reports.append('04_TMatrix_Home_Work')
        if self.checkBox05_Corr_Metro2018.isChecked(): reports.append('05_Corr_Metro')
        if self.checkBox09_Times2018.isChecked(): reports.append('09_Times')
        if self.checkBox09_Times_H2018.isChecked(): reports.append('09_Times_Holiday')
        if self.checkBox09_CTimes2018.isChecked(): reports.append('09_CTimes')
        if self.checkBox09_CTimes_H2018.isChecked(): reports.append('09_CTimes_Holiday')
        if self.checkBox11_CMatrixM2018.isChecked(): reports.append('11_CMatrix_Metro')
        if self.checkBox11_CMatrixM_H2018.isChecked(): reports.append('11_CMatrix_Metro_Holiday')
        return reports
    
    def getMonthList2015(self):
        monthList = []
        if self.checkBox201507.isChecked(): monthList.append(201507)
        if self.checkBox201508.isChecked(): monthList.append(201508)
        if self.checkBox201509.isChecked(): monthList.append(201509)
        if self.checkBox201510.isChecked(): monthList.append(201510)
        if self.checkBox201511.isChecked(): monthList.append(201511)
        if self.checkBox201512.isChecked(): monthList.append(201512)
        if self.checkBox201601.isChecked(): monthList.append(201601)
        if self.checkBox201602.isChecked(): monthList.append(201602)
        if self.checkBox201603.isChecked(): monthList.append(201603)
        if self.checkBox201604.isChecked(): monthList.append(201604)
        if self.checkBox201605.isChecked(): monthList.append(201605)
        if self.checkBox201606.isChecked(): monthList.append(201606)
        if self.checkBox201607.isChecked(): monthList.append(201607)
        if self.checkBox201608.isChecked(): monthList.append(201608)
        if self.checkBox201609.isChecked(): monthList.append(201609)
        if self.checkBox201610.isChecked(): monthList.append(201610)
        if self.checkBox201611.isChecked(): monthList.append(201611)
        if self.checkBox201612.isChecked(): monthList.append(201612)
        if self.checkBox201701.isChecked(): monthList.append(201701)
        if self.checkBox201702.isChecked(): monthList.append(201702)
        if self.checkBox201703.isChecked(): monthList.append(201703)
        if self.checkBox201704.isChecked(): monthList.append(201704)
        if self.checkBox201705.isChecked(): monthList.append(201705)
        if self.checkBox201706.isChecked(): monthList.append(201706)
        return monthList
    
    def getMonthList2018(self):
        monthList = []
        if self.checkBox201802.isChecked(): monthList.append(201802)
        if self.checkBox201803.isChecked(): monthList.append(201803)
        if self.checkBox201804.isChecked(): monthList.append(201804)
        return monthList
    
    def getExtDict2015(self):
        ext = {}
        if self.checkBox01_Location2015.isChecked(): ext['01_Location'] = self.comboBox01_Location2015.currentText()
        if self.checkBox01_CLocation2015.isChecked(): ext['01_CLocation'] = self.comboBox01_CLocation2015.currentText()
        if self.checkBox01_fCLocation2015.isChecked(): ext['01_fCLocation'] = self.comboBox01_fCLocation2015.currentText()
        if self.checkBox02_Density2015.isChecked(): ext['02_Density'] = self.comboBox02_Density2015.currentText()
        if self.checkBox02_CDensity2015.isChecked(): ext['02_CDensity'] = self.comboBox02_CDensity2015.currentText()
        if self.checkBox02_fCDensity2015.isChecked(): ext['02_fCDensity'] = self.comboBox02_fCDensity2015.currentText()
        if self.checkBox03_Matrix2015.isChecked(): ext['03_Matrix'] = self.comboBox03_Matrix2015.currentText()
        if self.checkBox04_Matrix_HMWK2015.isChecked(): ext['04_Matrix_Home_Work'] = self.comboBox04_Matrix_HMWK2015.currentText()
        if self.checkBox05_Corr_Metro2015.isChecked(): ext['05_Corr_Metro'] = self.comboBox05_Corr_Metro2015.currentText()
        if self.checkBox06_MatrixDom2015.isChecked(): ext['06_Matrix_Dom'] = self.comboBox06_MatrixDom2015.currentText()
        if self.checkBox07_Dachnik2015.isChecked(): ext['07_Dachnik'] = self.comboBox07_Dachnik2015.currentText()
        if self.checkBox08_ExternalW2015.isChecked(): ext['08_ExternalWorkers'] = self.comboBox08_ExternalW2015.currentText()
        if self.checkBox09_Times2015.isChecked(): ext['09_Times'] = self.comboBox09_Times2015.currentText()
        if self.checkBox10_Transit2015.isChecked(): ext['10_Transit'] = self.comboBox10_Transit2015.currentText()
        if self.checkBox11_CMatrixM2015.isChecked(): ext['11_CMatrix_Metro'] = self.comboBox11_CMatrixM2015.currentText()
        return ext
    
    def getExtDict2018(self):
        ext = {}
        if self.checkBox01_Location2018.isChecked(): ext['01_Location'] = self.comboBox01_Location2018.currentText()
        if self.checkBox01_CLocation2018.isChecked(): ext['01_CLocation'] = self.comboBox01_CLocation2018.currentText()
        if self.checkBox01_TLocation2018.isChecked(): ext['01_TLocation'] = self.comboBox01_TLocation2018.currentText()
        if self.checkBox01_CLocation_t2018.isChecked(): ext['01_CLocation_types'] = self.comboBox01_CLocation_t2018.currentText()
        if self.checkBox02_Density2018.isChecked(): ext['02_Density'] = self.comboBox02_Density2018.currentText()
        if self.checkBox02_CDensity2018.isChecked(): ext['02_CDensity'] = self.comboBox02_CDensity2018.currentText()
        if self.checkBox02_TDensity2018.isChecked(): ext['02_TDensity'] = self.comboBox02_TDensity2018.currentText()
        if self.checkBox02_CDensity_t2018.isChecked(): ext['02_CDensity_types'] = self.comboBox02_CDensity_t2018.currentText()
        if self.checkBox03_Matrix2018.isChecked(): ext['03_Matrix'] = self.comboBox03_Matrix2018.currentText()
        if self.checkBox03_CMatrix2018.isChecked(): ext['03_CMatrix'] = self.comboBox03_TMatrix2018.currentText()
        if self.checkBox03_TMatrix2018.isChecked(): ext['03_TMatrix'] = self.comboBox03_CMatrix2018.currentText()
        if self.checkBox04_Matrix_HMWK2018.isChecked(): ext['04_Matrix_Home_Work'] = self.comboBox04_Matrix_HMWK2018.currentText()
        if self.checkBox04_CMatrix_HMWK2018.isChecked(): ext['04_CMatrix_Home_Work'] = self.comboBox04_CMatrix_HMWK2018.currentText()
        if self.checkBox04_TMatrix_HMWK2018.isChecked(): ext['04_TMatrix_Home_Work'] = self.comboBox04_TMatrix_HMWK2018.currentText()
        if self.checkBox05_Corr_Metro2018.isChecked(): ext['05_Corr_Metro'] = self.comboBox05_Corr_Metro2018.currentText()
        if self.checkBox09_Times2018.isChecked(): ext['09_Times'] = self.comboBox09_Times2018.currentText()
        if self.checkBox09_Times_H2018.isChecked(): ext['09_Times_Holiday'] = self.comboBox09_Times_H2018.currentText()
        if self.checkBox09_CTimes2018.isChecked(): ext['09_CTimes'] = self.comboBox09_CTimes2018.currentText()
        if self.checkBox09_CTimes_H2018.isChecked(): ext['09_CTimes_Holiday'] = self.comboBox09_CTimes_H2018.currentText()
        if self.checkBox11_CMatrixM2018.isChecked(): ext['11_CMatrix_Metro'] = self.comboBox11_CMatrixM2018.currentText()
        if self.checkBox11_CMatrixM_H2018.isChecked(): ext['11_CMatrix_Metro_Holiday'] = self.comboBox11_CMatrixM_H2018.currentText()
        return ext           
    
    def checkCheckedReportsAndDates2018(self):
        checkedBoxesReports =[
            self.checkBox01_Location2018.isChecked(),
            self.checkBox01_CLocation2018.isChecked(),
            self.checkBox01_TLocation2018.isChecked(),
            self.checkBox01_CLocation_t2018.isChecked(),
            self.checkBox02_Density2018.isChecked(),
            self.checkBox02_CDensity2018.isChecked(),
            self.checkBox02_TDensity2018.isChecked(),
            self.checkBox02_CDensity_t2018.isChecked(),
            self.checkBox03_Matrix2018.isChecked(),
            self.checkBox03_Matrix2018.isChecked(),
            self.checkBox03_CMatrix2018.isChecked(),
            self.checkBox03_TMatrix2018.isChecked(),
            self.checkBox04_Matrix_HMWK2018.isChecked(),
            self.checkBox04_CMatrix_HMWK2018.isChecked(),
            self.checkBox04_TMatrix_HMWK2018.isChecked(),
            self.checkBox05_Corr_Metro2018.isChecked(),
            self.checkBox09_Times2018.isChecked(),
            self.checkBox09_Times_H2018.isChecked(),
            self.checkBox09_CTimes2018.isChecked(),
            self.checkBox09_CTimes_H2018.isChecked(),
            self.checkBox11_CMatrixM2018.isChecked(),
            self.checkBox11_CMatrixM_H2018.isChecked()
            ]
        checkedBoxesDates =[
            self.checkBox201802.isChecked(),
            self.checkBox201803.isChecked(),
            self.checkBox201804.isChecked()
            ]
        if any(checkedBoxesReports) is True and any(checkedBoxesDates) is True:
            return True
        else:
            return False
    
    def checkCheckedReportsAndDates2015(self):
        checkedBoxesReports =[
            self.checkBox01_Location2015.isChecked(),
            self.checkBox01_CLocation2015.isChecked(),
            self.checkBox01_fCLocation2015.isChecked(),
            self.checkBox02_Density2015.isChecked(),
            self.checkBox02_CDensity2015.isChecked(),
            self.checkBox02_fCDensity2015.isChecked(),
            self.checkBox03_Matrix2015.isChecked(),
            self.checkBox04_Matrix_HMWK2015.isChecked(),
            self.checkBox05_Corr_Metro2015.isChecked(),
            self.checkBox06_MatrixDom2015.isChecked(),
            self.checkBox07_Dachnik2015.isChecked(),
            self.checkBox08_ExternalW2015.isChecked(),
            self.checkBox09_Times2015.isChecked(),
            self.checkBox10_Transit2015.isChecked(),
            self.checkBox11_CMatrixM2015.isChecked()
            ]
        checkedBoxesDates =[
            self.checkBox201507.isChecked(),
            self.checkBox201508.isChecked(),
            self.checkBox201509.isChecked(),
            self.checkBox201510.isChecked(),
            self.checkBox201511.isChecked(),
            self.checkBox201512.isChecked(),
            self.checkBox201601.isChecked(),
            self.checkBox201602.isChecked(),
            self.checkBox201603.isChecked(),
            self.checkBox201604.isChecked(),
            self.checkBox201605.isChecked(),
            self.checkBox201606.isChecked(),
            self.checkBox201607.isChecked(),
            self.checkBox201608.isChecked(),
            self.checkBox201609.isChecked(),
            self.checkBox201610.isChecked(),
            self.checkBox201611.isChecked(),
            self.checkBox201612.isChecked(),
            self.checkBox201701.isChecked(),
            self.checkBox201702.isChecked(),
            self.checkBox201703.isChecked(),
            self.checkBox201704.isChecked(),
            self.checkBox201705.isChecked(),
            self.checkBox201706.isChecked()
            ]
        if any(checkedBoxesReports) is True and any(checkedBoxesDates) is True:
            return True
        else:
            return False

    def setFormats2018(self, index):
        self.comboBox01_Location2018.setCurrentIndex(index)
        self.comboBox01_CLocation2018.setCurrentIndex(index)
        self.comboBox01_TLocation2018.setCurrentIndex(index)
        self.comboBox01_CLocation_t2018.setCurrentIndex(index)
        self.comboBox02_Density2018.setCurrentIndex(index)
        self.comboBox02_CDensity2018.setCurrentIndex(index)
        self.comboBox02_TDensity2018.setCurrentIndex(index)
        self.comboBox02_CDensity_t2018.setCurrentIndex(index)
        self.comboBox03_Matrix2018.setCurrentIndex(index)
        self.comboBox03_CMatrix2018.setCurrentIndex(index)
        self.comboBox03_TMatrix2018.setCurrentIndex(index)
        self.comboBox04_Matrix_HMWK2018.setCurrentIndex(index)
        self.comboBox04_CMatrix_HMWK2018.setCurrentIndex(index)
        self.comboBox04_TMatrix_HMWK2018.setCurrentIndex(index)
        self.comboBox05_Corr_Metro2018.setCurrentIndex(index)
        self.comboBox09_Times2018.setCurrentIndex(index)
        self.comboBox09_Times_H2018.setCurrentIndex(index)
        self.comboBox09_CTimes2018.setCurrentIndex(index)
        self.comboBox09_CTimes_H2018.setCurrentIndex(index)
        self.comboBox11_CMatrixM2018.setCurrentIndex(index)
        self.comboBox11_CMatrixM_H2018.setCurrentIndex(index)        
    
    def setAllGZ2018(self):
        self.setFormats2018(0)
        
    def setAllCSV2018(self):
        self.setFormats2018(1)
        
    def setFormats2015(self, index):
        self.comboBox01_Location2015.setCurrentIndex(index)
        self.comboBox01_CLocation2015.setCurrentIndex(index)
        self.comboBox01_fCLocation2015.setCurrentIndex(index)
        self.comboBox02_Density2015.setCurrentIndex(index)
        self.comboBox02_CDensity2015.setCurrentIndex(index)
        self.comboBox02_fCDensity2015.setCurrentIndex(index)
        self.comboBox03_Matrix2015.setCurrentIndex(index)
        self.comboBox04_Matrix_HMWK2015.setCurrentIndex(index)
        self.comboBox05_Corr_Metro2015.setCurrentIndex(index)
        self.comboBox06_MatrixDom2015.setCurrentIndex(index)
        self.comboBox07_Dachnik2015.setCurrentIndex(index)
        self.comboBox08_ExternalW2015.setCurrentIndex(index)
        self.comboBox09_Times2015.setCurrentIndex(index)
        self.comboBox10_Transit2015.setCurrentIndex(index)
        self.comboBox11_CMatrixM2015.setCurrentIndex(index)
        
    def setAllGZ2015(self):
        self.setFormats2015(0)
        
    def setAllCSV2015(self):
        self.setFormats2015(1)
    
    def setCheckedAllReports2018(self, state):
        self.checkBox01_Location2018.setChecked(state)
        self.checkBox01_CLocation2018.setChecked(state)
        self.checkBox01_TLocation2018.setChecked(state)
        self.checkBox01_CLocation_t2018.setChecked(state)
        self.checkBox02_Density2018.setChecked(state)
        self.checkBox02_CDensity2018.setChecked(state)
        self.checkBox02_TDensity2018.setChecked(state)
        self.checkBox02_CDensity_t2018.setChecked(state)
        self.checkBox03_Matrix2018.setChecked(state)
        self.checkBox03_Matrix2018.setChecked(state)
        self.checkBox03_CMatrix2018.setChecked(state)
        self.checkBox03_TMatrix2018.setChecked(state)
        self.checkBox04_Matrix_HMWK2018.setChecked(state)
        self.checkBox04_CMatrix_HMWK2018.setChecked(state)
        self.checkBox04_TMatrix_HMWK2018.setChecked(state)
        self.checkBox05_Corr_Metro2018.setChecked(state)
        self.checkBox09_Times2018.setChecked(state)
        self.checkBox09_Times_H2018.setChecked(state)
        self.checkBox09_CTimes2018.setChecked(state)
        self.checkBox09_CTimes_H2018.setChecked(state)
        self.checkBox11_CMatrixM2018.setChecked(state)
        self.checkBox11_CMatrixM_H2018.setChecked(state)        
    
    def selectAllReports2018(self):
        self.setCheckedAllReports2018(True)
    
    def unselectAllReports2018(self):
        self.setCheckedAllReports2018(False)
    
    def setCheckedAllReports2015(self, state):
        self.checkBox01_Location2015.setChecked(state)
        self.checkBox01_CLocation2015.setChecked(state)
        self.checkBox01_fCLocation2015.setChecked(state)
        self.checkBox02_Density2015.setChecked(state)
        self.checkBox02_CDensity2015.setChecked(state)
        self.checkBox02_fCDensity2015.setChecked(state)
        self.checkBox03_Matrix2015.setChecked(state)
        self.checkBox04_Matrix_HMWK2015.setChecked(state)
        self.checkBox05_Corr_Metro2015.setChecked(state)
        self.checkBox06_MatrixDom2015.setChecked(state)
        self.checkBox07_Dachnik2015.setChecked(state)
        self.checkBox08_ExternalW2015.setChecked(state)
        self.checkBox09_Times2015.setChecked(state)
        self.checkBox10_Transit2015.setChecked(state)
        self.checkBox11_CMatrixM2015.setChecked(state)
        
    
    def selectAllReports2015(self):
        self.setCheckedAllReports2015(True)
    
    def unselectAllReports2015(self):
        self.setCheckedAllReports2015(False)
             
    def setCheckedAllDates2015(self, state):
        self.checkBox201507.setChecked(state)
        self.checkBox201508.setChecked(state)
        self.checkBox201509.setChecked(state)
        self.checkBox201510.setChecked(state)
        self.checkBox201511.setChecked(state)
        self.checkBox201512.setChecked(state)
        self.checkBox201601.setChecked(state)
        self.checkBox201602.setChecked(state)
        self.checkBox201603.setChecked(state)
        self.checkBox201604.setChecked(state)
        self.checkBox201605.setChecked(state)
        self.checkBox201606.setChecked(state)
        self.checkBox201607.setChecked(state)
        self.checkBox201608.setChecked(state)
        self.checkBox201609.setChecked(state)
        self.checkBox201610.setChecked(state)
        self.checkBox201611.setChecked(state)
        self.checkBox201612.setChecked(state)
        self.checkBox201701.setChecked(state)
        self.checkBox201702.setChecked(state)
        self.checkBox201703.setChecked(state)
        self.checkBox201704.setChecked(state)
        self.checkBox201705.setChecked(state)
        self.checkBox201706.setChecked(state)
        
    def setCheckedAllDates2018(self, state):
        self.checkBox201802.setChecked(state)
        self.checkBox201803.setChecked(state)
        self.checkBox201804.setChecked(state)
    
    def selectAllDates2015(self, state):
        self.setCheckedAllDates2015(True)
        
    def unselectAllDates2015(self, state):
        self.setCheckedAllDates2015(False)
        
    def selectAllDates2018(self, state):
        self.setCheckedAllDates2018(True)
        
    def unselectAllDates2018(self, state):
        self.setCheckedAllDates2018(False)    
    
    def browseAdmDict2015(self):
        filePath = QtWidgets.QFileDialog.getOpenFileName(self)[0]
        filePath = filePath.replace('/','\\')
        self.labAdmDict2015.setText(filePath)
        
    def browseCellsDict2015(self):
        filePath = QtWidgets.QFileDialog.getOpenFileName(self)[0]
        filePath = filePath.replace('/','\\')
        self.labCellsDict2015.setText(filePath)
    
    def browseAdmDict2018(self):
        filePath = QtWidgets.QFileDialog.getOpenFileName(self)[0]
        filePath = filePath.replace('/','\\')
        self.labAdmDict2018.setText(filePath)
        
    def browseCellsDict2018(self):
        filePath = QtWidgets.QFileDialog.getOpenFileName(self)[0]
        filePath = filePath.replace('/','\\')
        self.labCellsDict2018.setText(filePath)
    
    def browseTrDict2018(self):
        filePath = QtWidgets.QFileDialog.getOpenFileName(self)[0]
        filePath = filePath.replace('/','\\')
        self.labTrDict2018.setText(filePath)
    
    def groupBoxRegimeState(self, radioButtonCopy, radioButtonRepack, radioButtonRecode):
        if radioButtonCopy.isChecked() == True:
            self.groupBoxDicts2015.setEnabled(False)
            self.groupBoxDicts2018.setEnabled(False)
            self.pushButtonTempDir.setEnabled(False)
            self.changeComboBoxesState(False)
        if radioButtonRepack.isChecked() == True:
            self.groupBoxDicts2015.setEnabled(False)
            self.groupBoxDicts2018.setEnabled(False)
            self.pushButtonTempDir.setEnabled(True)
            self.changeComboBoxesState(True)
        if radioButtonRecode.isChecked() == True:
            self.groupBoxDicts2015.setEnabled(True)
            self.groupBoxDicts2018.setEnabled(True)
            self.pushButtonTempDir.setEnabled(True)
            self.changeComboBoxesState(True)
        
    def changeComboBoxesState(self, state):
        self.pushButtonSetGZ2015.setEnabled(state)
        self.pushButtonSetCSV2015.setEnabled(state)
        #
        self.comboBox01_Location2015.setEnabled(state)
        self.comboBox01_CLocation2015.setEnabled(state)
        self.comboBox01_fCLocation2015.setEnabled(state)
        self.comboBox02_Density2015.setEnabled(state)
        self.comboBox02_CDensity2015.setEnabled(state)
        self.comboBox02_fCDensity2015.setEnabled(state)
        self.comboBox03_Matrix2015.setEnabled(state)
        self.comboBox04_Matrix_HMWK2015.setEnabled(state)
        self.comboBox05_Corr_Metro2015.setEnabled(state)
        self.comboBox06_MatrixDom2015.setEnabled(state)
        self.comboBox07_Dachnik2015.setEnabled(state)
        self.comboBox08_ExternalW2015.setEnabled(state)
        self.comboBox09_Times2015.setEnabled(state)
        self.comboBox10_Transit2015.setEnabled(state)
        self.comboBox11_CMatrixM2015.setEnabled(state)
        #
        self.pushButtonSetGZ2018.setEnabled(state)
        self.pushButtonSetCSV2018.setEnabled(state)
        #
        self.comboBox01_Location2018.setEnabled(state)
        self.comboBox01_CLocation2018.setEnabled(state)
        self.comboBox01_TLocation2018.setEnabled(state)
        self.comboBox01_CLocation_t2018.setEnabled(state)
        self.comboBox02_Density2018.setEnabled(state)
        self.comboBox02_CDensity2018.setEnabled(state)
        self.comboBox02_TDensity2018.setEnabled(state)
        self.comboBox02_CDensity_t2018.setEnabled(state)
        self.comboBox03_Matrix2018.setEnabled(state)
        self.comboBox03_CMatrix2018.setEnabled(state)
        self.comboBox03_TMatrix2018.setEnabled(state)
        self.comboBox04_Matrix_HMWK2018.setEnabled(state)
        self.comboBox04_CMatrix_HMWK2018.setEnabled(state)
        self.comboBox04_TMatrix_HMWK2018.setEnabled(state)
        self.comboBox05_Corr_Metro2018.setEnabled(state)
        self.comboBox09_Times2018.setEnabled(state)
        self.comboBox09_Times_H2018.setEnabled(state)
        self.comboBox09_CTimes2018.setEnabled(state)
        self.comboBox09_CTimes_H2018.setEnabled(state)
        self.comboBox11_CMatrixM2018.setEnabled(state)
        self.comboBox11_CMatrixM_H2018.setEnabled(state)
        
        
    
    def browseInputFolder(self):
        folderPath = QtWidgets.QFileDialog.getExistingDirectory(self)
        folderPath = folderPath.replace('/','\\')
        self.labInputDir.setText(folderPath)
    
    def browseTempFolder(self):
        folderPath = QtWidgets.QFileDialog.getExistingDirectory(self)
        folderPath = folderPath.replace('/','\\')
        self.labTempDir.setText(folderPath)
    
    def browseOutFolder(self):
        folderPath = QtWidgets.QFileDialog.getExistingDirectory(self)
        folderPath = folderPath.replace('/','\\')
        self.labOutDir.setText(folderPath)

        
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = configWindow()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()

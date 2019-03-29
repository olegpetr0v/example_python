#-*- coding: utf-8 -*-

import const
import check_01_Location, check_01_CLocation, check_01_TLocation, check_01_CLocation_types 
#import check_02_Density, check_02_CDensity, check_02_TDensity, check_02_CDensity_types
#import check_03_Matrix, check_03_CMatrix, check_03_TMatrix
#import check_04_Matrix_HMWK, check_04_CMatrix_HMWK, check_04_TMatrix_HMWK
#import check_05_Corr_Met
#import check_09_Times, check_09_Times_Holiday, check_09_CTimes, check_09_CTimes_Holiday
#import check_11_CMat_Metro, check_11_CMat_Metro_Holiday


class DataFiles():
    def __init__(self):
        self.files = {}
        self.checkDate = '000000'
    
    def loadfiles(self, files):
        for fileType in iter(const.fileTypes):
            currTypeFiles = {}
            for f in files:
                namePartList = f.split('\\')[-1].strip().split('_')
                nameFileType = '_'.join(namePartList[1:-2])
                if len(namePartList) in (4, 5, 6) and nameFileType == fileType:
                    try:
                        date = f.split('\\')[-1].strip().split('_')[-1].split('.')[0]
                        currTypeFiles[date] = f
                        if int(date) > int(self.checkDate):
                            self.checkDate = date
                    except Exception as msg:
                        print('Внимание! Не удалось конвертировать дату (%s).'%msg)
            self.files[fileType] = currTypeFiles
        return self
    
    def get_date(self):
        return self.checkDate
    
    def get_check_files(self):
        return { fileType : dateFiles[self.checkDate] \
                 for fileType, dateFiles in self.files.items() if self.checkDate in dateFiles.keys() }
    
    def get_extra_files(self):
        return { fileType : [f for date, f in dateFiles.items() if date!=self.checkDate] \
                 for fileType, dateFiles in self.files.items() }

    def check(self):
        checkFiles = self.get_check_files()

        report = ''
        if const.T_01_LOCATION in checkFiles.keys():
            print('\nПроверяется файл %s'%checkFiles[const.T_01_LOCATION])
            report += '\n---%s---\n%s\n'%(checkFiles[const.T_01_LOCATION],\
                                          check_01_Location.run(checkFiles[const.T_01_LOCATION], self.checkDate, self.files))
        
        if const.T_01_CLOCATION in checkFiles.keys():
            print('\nПроверяется файл %s'%checkFiles[const.T_01_CLOCATION])
            report += '\n---%s---\n%s\n'%(checkFiles[const.T_01_CLOCATION],\
                                          check_01_CLocation.run(checkFiles[const.T_01_CLOCATION], self.checkDate, self.files))
        
        if const.T_01_TLOCATION in checkFiles.keys():
            print('\nПроверяется файл %s'%checkFiles[const.T_01_TLOCATION])
            report += '\n---%s---\n%s\n'%(checkFiles[const.T_01_TLOCATION],\
                                          check_01_TLocation.run(checkFiles[const.T_01_TLOCATION], self.checkDate, self.files))
        
        if const.T_01_CLOCATION_T in checkFiles.keys():
            print('\nПроверяется файл %s'%checkFiles[const.T_01_CLOCATION_T])
            report += '\n---%s---\n%s\n'%(checkFiles[const.T_01_CLOCATION_T],\
                                          check_01_CLocation_types.run(checkFiles[const.T_01_CLOCATION_T], self.checkDate, self.files))
        
        if const.T_02_DENSITY in checkFiles.keys():
            print('\nПроверяется файл %s'%checkFiles[const.T_02_DENSITY])
            report += '\n---%s---\n%s\n'%(checkFiles[const.T_02_DENSITY],\
                                          check_02_Density.run(checkFiles[const.T_02_DENSITY], self.checkDate, self.files))
        
        if const.T_02_CDENSITY in checkFiles.keys():
            print('\nПроверяется файл %s'%checkFiles[const.T_02_CDENSITY])
            report += '\n---%s---\n%s\n'%(checkFiles[const.T_02_CDENSITY],\
                                          check_02_CDensity.run(checkFiles[const.T_02_CDENSITY], self.checkDate, self.files))
        
        if const.T_02_TDENSITY in checkFiles.keys():
            print('\nПроверяется файл %s'%checkFiles[const.T_02_TDENSITY])
            report += '\n---%s---\n%s\n'%(checkFiles[const.T_02_TDENSITY],\
                                          check_02_TDensity.run(checkFiles[const.T_02_TDENSITY], self.checkDate, self.files))
            
        if const.T_02_CDENSITY_T in checkFiles.keys():
            print('\nПроверяется файл %s'%checkFiles[const.T_02_CDENSITY_T])
            report += '\n---%s---\n%s\n'%(checkFiles[const.T_02_CDENSITY_T],\
                                          check_02_CDensity_types.run(checkFiles[const.T_02_CDENSITY_T], self.checkDate, self.files))
            
        if const.T_03_MATRIX in checkFiles.keys():
            print('\nПроверяется файл %s'%checkFiles[const.T_03_MATRIX])
            report += '\n---%s---\n%s\n'%(checkFiles[const.T_03_MATRIX],\
                                          check_03_Matrix.run(checkFiles[const.T_03_MATRIX], self.checkDate, self.files))
            
        if const.T_03_CMATRIX in checkFiles.keys():
            print('\nПроверяется файл %s'%checkFiles[const.T_03_CMATRIX])
            report += '\n---%s---\n%s\n'%(checkFiles[const.T_03_CMATRIX],\
                                          check_03_CMatrix.run(checkFiles[const.T_03_CMATRIX], self.checkDate, self.files))
            
        if const.T_03_TMATRIX in checkFiles.keys():
            print('\nПроверяется файл %s'%checkFiles[const.T_03_TMATRIX])
            report += '\n---%s---\n%s\n'%(checkFiles[const.T_03_TMATRIX],\
                                          check_03_TMatrix.run(checkFiles[const.T_03_TMATRIX], self.checkDate, self.files))
            
        if const.T_04_MATRIX_HMWK in checkFiles.keys():
            print('\nПроверяется файл %s'%checkFiles[const.T_04_MATRIX_HMWK])
            report += '\n---%s---\n%s\n'%(checkFiles[const.T_04_MATRIX_HMWK],\
                                       check_04_Matrix_HMWK.run(checkFiles[const.T_04_MATRIX_HMWK], self.checkDate, self.files))
            
        if const.T_04_CMATRIX_HMWK in checkFiles.keys():
            print('\nПроверяется файл %s'%checkFiles[const.T_04_CMATRIX_HMWK])
            report += '\n---%s---\n%s\n'%(checkFiles[const.T_04_CMATRIX_HMWK],\
                                       check_04_CMatrix_HMWK.run(checkFiles[const.T_04_CMATRIX_HMWK], self.checkDate, self.files))
            
        if const.T_04_TMATRIX_HMWK in checkFiles.keys():
            print('\nПроверяется файл %s'%checkFiles[const.T_04_TMATRIX_HMWK])
            report += '\n---%s---\n%s\n'%(checkFiles[const.T_04_TMATRIX_HMWK],\
                                       check_04_TMatrix_HMWK.run(checkFiles[const.T_04_TMATRIX_HMWK], self.checkDate, self.files))
            
        if const.T_05_CORR_MET in checkFiles.keys():
            print('\nПроверяется файл %s'%checkFiles[const.T_05_CORR_MET])
            report += '\n---%s---\n%s\n'%(checkFiles[const.T_05_CORR_MET],\
                                          check_05_Corr_Met.run(checkFiles[const.T_05_CORR_MET], self.checkDate, self.files))
 
        if const.T_09_TIMES in checkFiles.keys():
            print('\nПроверяется файл %s'%checkFiles[const.T_09_TIMES])
            report += '\n---%s---\n%s\n'%(checkFiles[const.T_09_TIMES],\
                                          check_09_Times.run(checkFiles[const.T_09_TIMES], self.checkDate, self.files))
            
        if const.T_09_TIMES_H in checkFiles.keys():
            print('\nПроверяется файл %s'%checkFiles[const.T_09_TIMES_H])
            report += '\n---%s---\n%s\n'%(checkFiles[const.T_09_TIMES_H],\
                                          check_09_Times_Holiday.run(checkFiles[const.T_09_TIMES_H], self.checkDate, self.files))
            
        if const.T_09_CTIMES in checkFiles.keys():
            print('\nПроверяется файл %s'%checkFiles[const.T_09_CTIMES])
            report += '\n---%s---\n%s\n'%(checkFiles[const.T_09_CTIMES],\
                                          check_09_CTimes.run(checkFiles[const.T_09_CTIMES], self.checkDate, self.files))
            
        if const.T_09_CTIMES_H in checkFiles.keys():
            print('\nПроверяется файл %s'%checkFiles[const.T_09_CTIMES_H])
            report += '\n---%s---\n%s\n'%(checkFiles[const.T_09_CTIMES_H],\
                                          check_09_CTimes_Holiday.run(checkFiles[const.T_09_CTIMES_H], self.checkDate, self.files))
            
        if const.T_11_CMAT_METRO in checkFiles.keys():
            print('\nПроверяется файл %s'%checkFiles[const.T_11_CMAT_METRO])
            report += '\n---%s---\n%s'%(checkFiles[const.T_11_CMAT_METRO],\
                                        check_11_CMat_Metro.run(checkFiles[const.T_11_CMAT_METRO], self.checkDate, self.files))
            
        if const.T_11_CMAT_METRO_H in checkFiles.keys():
            print('\nПроверяется файл %s'%checkFiles[const.T_11_CMAT_METRO_H])
            report += '\n---%s---\n%s'%(checkFiles[const.T_11_CMAT_METRO_H],\
                                        check_11_CMat_Metro_Holiday.run(checkFiles[const.T_11_CMAT_METRO_H], self.checkDate, self.files))
        
        return report
    
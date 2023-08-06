# -*- coding: utf-8 -*-

from mdspwrstripbackup import ExtDiscBackup


ob1 = ExtDiscBackup('backup', logfile='externbackup.log')
ob1.setIniFile('backupserver2exthd.ini')
ob1.loadConfig()

if ob1.paraCheck() == True:
    ob1.showConfig()
del ob1

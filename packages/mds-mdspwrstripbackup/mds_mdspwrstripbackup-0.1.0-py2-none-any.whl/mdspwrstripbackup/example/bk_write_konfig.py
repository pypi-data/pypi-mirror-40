# -*- coding: utf-8 -*-

from mdspwrstripbackup import ExtDiscBackup


ob1 = ExtDiscBackup('backup', logfile='externbackup.log')
ob1.setIniFile('backupserver2exthd.ini')
ob1.loadConfig()
ob1.setSmartCheck(True)
ob1.setSteckdoseTreiber('gude')
ob1.setStrategy(2, 14) # number of hard discs, number of backups per disc
ob1.setLogin('192.168.0.6', 'kennwort')
ob1.setPlatteKonfig(0, 1, 'backup1', '/dev/sdc1')
ob1.setPlatteKonfig(1, 2, 'backup2', '/dev/sdc1')
ob1.addQuellDir('/home/')
ob1.setMountPunkt('/mnt/')
ob1.addExcludeDir('poolvm1/')
ob1.setControlScript('./mdspwrstripbackup/epccontrol2.pl')
if ob1.paraCheck() == True:
    ob1.showConfig()
    ob1.saveConfig()
del ob1

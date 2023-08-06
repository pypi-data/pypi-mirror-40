#!/usr/bin/python
# -*- coding: utf-8 -*-

from extbackupsteckdose import ExtBackupSteckdose


if __name__ == '__main__':
  ob1 = ExtBackupSteckdose('backup', logfile='/var/log/externbackup.log')
  ob1.setIniFile('/etc/backupserver2exthd.ini')
  ob1.loadConfig()
  ob1.setSmartCheck(True)
  #ob1.setSteckdoseTreiber('gude')
  #ob1.setStrategie(2, 17)
  #ob1.setLogin('192.168.0.6', 'kennwort')
  #ob1.setPlatteKonfig(0, 1, 'backup1', '/dev/sdc1')
  #ob1.setPlatteKonfig(1, 2, 'backup2', '/dev/sdc1')
  #ob1.addQuellDir('/home/')
  #ob1.setMountPunkt('/mnt/backup')
  #ob1.addExcludeDir('poolvm1/')
  #ob1.setControlScript('/home/frederik/script/epccontrol2.pl')
  if ob1.paraCheck() == True:
    #ob1.showConfig()
    ob1.runConsoleCommands()
    ob1.saveConfig()
    pass
  del ob1

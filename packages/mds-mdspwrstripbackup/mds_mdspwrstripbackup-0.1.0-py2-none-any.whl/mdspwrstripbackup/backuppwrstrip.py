# -*- coding: utf-8 -*-


import sys, logging, copy, os, time
from datetime import datetime, timedelta
from mdslogger import MdsLogger, formatExceptionInfo
from mdsshellcommand import ShellCommandRun
try :
  import ConfigParser as configparser
except :
  import configparser
  
from .gude import GudePowerStrip
  

# config-file values
SECT_STRATEGY = 'strategy'
SECT_STRATEGY_CURR_DISC = 'curr-disc'                    # current hard disc
SECT_STRATEGY_NUM_DISCS = 'num-discs'                    # number of discs in backup
SECT_STRATEGY_CURR_BK_PER_DISC = 'curr-bk-per-disc'      # current copy on disc
SECT_STRATEGY_NUM_BK_PER_DISC = 'num-bk-per-disc'        # number of copys on disc

# login data
SECT_LOGIN = 'login'
SECT_LOGIN_IPADR = 'ip'
SECT_LOGIN_PASSWORD = 'password'

# disc config
SECT_DISCCFG = 'plcfg%s'
SECT_DISCCFG_PIN = 'pin'
SECT_DISCCFG_NAME = 'name'
SECT_DISCCFG_DEV = 'dev'

# source directory
SECT_SOURCEDIR = 'sourcedir'
SECT_SOURCEDIR_ANZDIR = 'numdir'
SECT_SOURCEDIR_DIR = 'dir%d'

# other
SECT_MISC = 'misc'
SECT_MISC_MOUNTPUNKT = 'mountpos'
SECT_MISC_CONTROLSCRIPT = 'controlscript'
SECT_MISC_AUTOCHECKFS = 'autocheck-fs'
SECT_MISC_CHECKSMART = 'check-smart'
SECT_MISC_PWROUTLET = 'pwroutlet'

VAL_PWROUTLET_GUDE = 'gude'
VAL_PWROUTLET_GEMBIRD = 'gembird'


# exclude directories
SECT_EXCLUDEDIRS = 'excludedirs'
SECT_EXCLUDEDIRS_ANZ = 'num'
SECT_EXCLUDEDIRS_DIR = 'dir%d'


 
class ExtDiscBackup:
    """ backup to external hard disc, using switcheable power outlets
    """

    def __init__(self, jobname, logfile=''):
        """ settings
        """
        self.__jobname = jobname
        if len(logfile) == 0:
            self.__logobj = MdsLogger(self.__jobname, conlogger=True, filelogger=False, loglev='debug', loglevcon='info', minNameLen=25)
        else :
            self.__logobj = MdsLogger(self.__jobname, conlogger=True, filelogger=True, maxlogsize=2000, logfilebackups=2, logfilename=logfile, loglev='debug', loglevcon='info', minNameLen=25)
        self.__log = self.__logobj.getLogObj()
        self.__inifile = None
        self.__konfigdict = {}
        self.__steckdose = None       # hier wird die jeweilige objektklasse für die steckdosensteuerung gespeichert
        self.__shellcmd = ShellCommandRun('extbk', self.__log)
        self.__steckdosentreiber = [VAL_PWROUTLET_GUDE, VAL_PWROUTLET_GEMBIRD]

    def __del__(self):
        """ clean up
        """
        if not isinstance(self.__steckdose, type(None)):
            del self.__steckdose
            self.__steckdose = None
        if not isinstance(self.__shellcmd, type(None)):
            del self.__shellcmd
            self.__shellcmd = None
        if not isinstance(self.__logobj, type(None)):
            del self.__logobj
            self.__log = None
            self.__logobj = None

    def getLogObj(self):
        """ get the logger
        """
        return self.__log
    
    def paraCheck(self):
        """ prüft die parameter
        """
        retval = True
        try :
            self.__log.info('+- pruefe Parameter:')
      
            # ini-datei
            if not isinstance(self.getIniFile(), type('')):
                retval = False
                self.__log.warning('|- keine INI-Datei angegeben')
            else :
                self.__log.info('|- INI-Datei: "%s"' % self.getIniFile())

            # strategie
            stg1 = self.__konfigdict.get(SECT_STRATEGY, {})
            apl1 = stg1.get(SECT_STRATEGY_NUM_DISCS, 0)
            abkp1 = stg1.get(SECT_STRATEGY_NUM_BK_PER_DISC, 0)
            aktbk1 = stg1.get(SECT_STRATEGY_CURR_BK_PER_DISC, 0)
            aktpl1 = stg1.get(SECT_STRATEGY_CURR_DISC, 0)
            if apl1 > 0:
                self.__log.info('|- Anzahl Festplatten: %d' % apl1)
            else :  
                self.__log.warning('|- keine Festplatten angegeben')
                retval = False
            if abkp1 > 0:
                self.__log.info('|- Anzahl Backups/Platte: %d' % abkp1)
            else :  
                self.__log.warning('|- Anzahl Backups/Platte muss groesser 0 sein.')
                retval = False
            self.__log.info('|- aktuelle Platte: %d' % aktpl1)
            self.__log.info('|- aktuelles Backup Nr. %d' % aktbk1)
      
            # logindaten
            (ipadr, kennw) = self.getLogin()
            if len(ipadr) > 0:
                self.__log.info('|- IP-Adresse der Steckdose: %s' % ipadr)
            else :
                self.__log.warning('|- keine IP-Adresse fuer die Steckdose angegeben')
                retval = False
            if len(kennw) > 0:
                self.__log.info('|- Kennwort gesetzt')
            else :
                self.__log.warning('|- kein Kennwort angegeben')
                retval = False

            # festplatten
            for i in range(apl1):
                plcfg = self.getPlatteCfg(i)
                pin1 = plcfg.get(SECT_DISCCFG_PIN, -1)
                name1 = plcfg.get(SECT_DISCCFG_NAME, '')
                dev1 = plcfg.get(SECT_DISCCFG_DEV, '')
                if (pin1 > 0) and (len(name1) > 0) and (len(dev1) > 0):
                    self.__log.info('|- Platte %d: Pin %d, Name %s, Geraet %s' % (i, pin1, name1, dev1))
                else :
                    self.__log.warning('|- Plattenkonfig %d fehlerhaft' % i)
                    retval = False
        
            # quellverzeichnisse
            anz1 = self.getAnzQuellDir()
            if anz1 == 0:
                self.__log.warning('|- kein Quellordner gesetzt')
                retval = False
            else :
                self.__log.info('|- Anzahl Quellordner: %d' % anz1)
                l1 = []
                for i in range(anz1):
                    fname = self.getQuellDir(i)
                    if isinstance(fname, type('')):
                        l1.append(fname)
                    else :
                        self.__log.warning('|- Quellordner %d nicht gesetzt' % i)
                        retval = False
                self.__log.info('|- Quellordner: %s' % str(l1))
      
            # excludeverzeichnisse
            anz1 = self.getAnzExcludeDir()
            if anz1 > 0:
                self.__log.info('|- Anzahl Excludeordner: %d' % anz1)
                l1 = []
                for i in range(anz1):
                    fname = self.getExcludeDir(i)
                    if isinstance(fname, type('')):
                        l1.append(fname)
                    else :
                        self.__log.warning('|- Excludeordner %d nicht gesetzt' % i)
                        retval = False
                self.__log.info('|- Excludeordner: %s' % str(l1))
      
            # mountpunkt
            mpunkt = self.getMountPunkt()
            if isinstance(mpunkt, type(None)):
                self.__log.warning('|- kein Mounktpunkt gesetzt')
                retval = False
            else :
                self.__log.info('|- Mountpunkt: %s' % mpunkt)

            # autocheck
            b1 = self.getAutocheckFs()
            if not isinstance(b1, type(True)):
                self.__log.warning('|- Autocheck muss Bool sein, ist: %s' % str(type(b1)))
                retval = False
            else :
                self.__log.info('|- Autocheck: %s' % str(b1))

            # check-smart
            b1 = self.getSmartCheck()
            if not isinstance(b1, type(True)):
                self.__log.warning('|- SMART-Check muss Bool sein, ist: %s' % str(type(b1)))
                retval = False
            else :
                self.__log.info('|- SMART-Check: %s' % str(b1))

            # auswahl des steckdosentreibers
            self.__workSteckdosenTreiber(True)
            if isinstance(self.__steckdose, type(None)):
                self.__log.warning('|- kein Steckdosentreiber gewaehlt')
                retval = False
            else :
                self.__log.info('|- Steckdose: %s' % self.getSteckdoseTreiber())

            # controlscript
            fname = self.getControlScript()
            if isinstance(fname, type(None)):
                self.__log.warning('|- Controlscript nicht gesetzt')
                retval = False
            else :
                self.__log.info('|- Controlscript: %s' % fname)

            self.__log.info('-- Parameterpruefung beendet, Ergebnis: %s' % retval)
        except :
            self.__log.error(str(formatExceptionInfo()))
            retval = False
        return retval
    
    def saveConfig(self):
        """ speichert die aktuelle konfiguration in die vorliegende konfigdatei
        """
        try :
            self.__log.debug('+- Konfiguration speichern')
            fname = self.getIniFile()
            self.__log.debug('|- INI-Datei: %s' % fname)
            if not isinstance(fname, type('')):
                self.__log.warning('keine INI-Datei angegeben')
                return

            cfg1 = configparser.ConfigParser()
            self.__log.debug('|- Configparser: %s' % str(cfg1))
            for i in self.__konfigdict:
                self.__log.debug('|- Sektion erstellen: %s' % i)
                cfg1.add_section(i)
                for k in self.__konfigdict[i]:
                    self.__log.debug('|- Wert erstellen: [%s] %s = %s' % (i, k, self.__konfigdict[i][k]))
                    self.__log.debug('|- Wert erstellen: [%s] %s = %s' % (type(i), type(k), type(self.__konfigdict[i][k])))
                    cfg1.set(i, k, str(self.__konfigdict[i][k]))
            self.__log.debug('|- Datei speichern: %s' % fname)
            fhdl = open(fname, 'w')
            cfg1.write(fhdl)
            fhdl.close()
            self.__log.debug('|- Datei speichern fertig')
            self.__log.debug('-- Konfiguration speichern fertig')
        except :
            self.__log.error(str(formatExceptionInfo()))
      
    def loadConfig(self):
        """ läd die bestehende konfiguration
        """
        try :
            self.__log.debug('+- Konfiguration laden')
            fname = self.getIniFile()
            self.__log.debug('|- INI-Datei: %s' % fname)
            if not isinstance(fname, type('')):
                self.__log.warning('keine INI-Datei angegeben')
                return

            cfg1 = configparser.ConfigParser()
            self.__log.debug('|- Configparser: %s' % str(cfg1))
            cfg1.read(fname)
            self.__log.debug('|- Konfig eingelesen, Dict fuellen')
            for i in cfg1.sections():
                if not i in self.__konfigdict.keys():
                    self.__log.debug('|- Sektion erstellen: %s' % i)
                    self.__konfigdict[i] = {}

                for k in cfg1.items(i):          
                    (k1, v1) = k
                    self.__log.debug('|- Wert hinzufuegen: [%s] %s = %s' % (i, k1, v1))
                    if ((i == SECT_STRATEGY) and (k1 == SECT_STRATEGY_NUM_DISCS)) or \
                        ((i.startswith(SECT_DISCCFG_PIN[:-2])) and (k1 == SECT_DISCCFG_PIN)) or \
                        ((i == SECT_EXCLUDEDIRS) and (k1 == SECT_EXCLUDEDIRS_ANZ)) or \
                        ((i == SECT_STRATEGY) and (k1 == SECT_STRATEGY_CURR_DISC)) or \
                        ((i == SECT_STRATEGY) and (k1 == SECT_STRATEGY_CURR_BK_PER_DISC)) or \
                        ((i == SECT_STRATEGY) and (k1 == SECT_STRATEGY_NUM_BK_PER_DISC)):
                        self.__konfigdict[i][k1] = int(v1)
          
                    elif ((i == SECT_MISC) and (k1 == SECT_MISC_PWROUTLET)):
                        if v1 in self.__steckdosentreiber:
                            self.__konfigdict[i][k1] = v1
                    elif ((i == SECT_MISC) and (k1 == SECT_MISC_AUTOCHECKFS)) or \
                        ((i == SECT_MISC) and (k1 == SECT_MISC_CHECKSMART)):
                        if v1.lower() == 'true':
                            self.__konfigdict[i][k1] = True
                        else :
                            self.__konfigdict[i][k1] = False
                    else :
                        self.__konfigdict[i][k1] = v1
            del cfg1
            self.__log.debug('-- Konfiguration laden fertig')
        except :
            self.__log.error(str(formatExceptionInfo()))

    def showConfig(self, showinlog = True):
        """ shows current configuration in console or logfile
        """
        try :
            if showinlog == True:
                self.__log.info('+- show current config')
                for i in self.__konfigdict.keys():
                    self.__log.info('|')
                    self.__log.info('|- [%s]' % i)
                    for k in self.__konfigdict[i].keys():
                        self.__log.info('|  %s = %s' % (k, self.__konfigdict[i][k]))
                self.__log.info('-- current config - done')
            else :
                print ('+- show current config')
                for i in self.__konfigdict.keys():
                    print ('|')
                    print ('|- [%s]' % i)
                    for k in self.__konfigdict[i].keys():
                        print ('|  %s = %s' % (k, self.__konfigdict[i][k]))
                print ('-- current config - done')
        except :
            self.__log.error(str(formatExceptionInfo()))

    def setSmartCheck(self, zustand):
        """ schaltet die smart-checkfunktion ein/aus
        """
        try :
            self.__log.debug('+- SMART-Check schalten: %s' % str(zustand))
            if not isinstance(zustand, type(True)):
                self.__log.warning('|- Parameterfehler: zustand --> Bool')
                return
        
            if not SECT_MISC in self.__konfigdict.keys():
                self.__konfigdict[SECT_MISC] = {}
            self.__konfigdict[SECT_MISC][SECT_MISC_CHECKSMART] = zustand
            self.__log.debug('-- SMART-Check schalten fertig')
        except:
            self.__log.error(str(formatExceptionInfo()))

    def getSmartCheck(self):
        """ holt den zustand von smart-check
        """
        try :
            b1 = self.__konfigdict.get(SECT_MISC, {}).get(SECT_MISC_CHECKSMART, True)
            self.__log.debug('check-smart: %s (type: %s)' % (str(b1), str(type(b1))))
            return b1
        except :
            self.__log.error(str(formatExceptionInfo()))
      
    def __smartGetStatus(self, plnr, inhalt):
        """ zeigt den smartstatus der gewählten platte
        """
        try :
            aktpl = self.getPlatteCfg(plnr)
            dev1 = aktpl[SECT_DISCCFG_DEV][:-1]
            self.__log.info('+- SMART-Daten anzeigen fuer %s' % dev1)
            if inhalt == 'A':     # statusregister: temp, bad sektors. etc.
                cmd1 = 'smartctl -A -d auto %s' % dev1
            elif inhalt == 't':   # temperaturstatistik
                cmd1 = 'smartctl -l scttemp -d auto %s' % dev1
            elif inhalt == 'a':   # übersicht aller daten
                cmd1 = 'smartctl -a -d auto %s' % dev1
            elif inhalt == 'x':   # sehr ausführliche übersicht aller daten
                cmd1 = 'smartctl -x -d auto %s' % dev1
            elif inhalt == 'i':   # infosektion: ser.nr., hersteller, plattengröße, etc.
                cmd1 = 'smartctl -i -d auto %s' % dev1
            elif inhalt == 's':   # health, attribute, selftest
                cmd1 = 'smartctl -d auto -H -A -l selftest %s' % dev1
            else :
                self.__log.warning('|- Parameter "%s" unbekannt, verwende "a"')
                cmd1 = 'smartctl -a -d auto %s' % dev1
      
            # werte abfragen
            self.__log.debug('|- CMD: %s' % cmd1)
            (status, text1, code1) = self.__shellcmd.runShellCmd(cmd1)
            self.__log.debug('|- Ergebnis: status=%s, text=%s, code=%s' % (str(status), str(text1), str(code1)))
            if status == True:
                l1 = text1.split('\n')
                for i in l1:
                    self.__log.info('|- %s' % i)
            else :
                self.__log.warning('Fehler rc=%d, Msg: %s' % (code1, text1))

            self.__log.info('-- SMART-Daten anzeigen fertig')
        except :
            self.__log.error(str(formatExceptionInfo()))

    def __smartEnaSave(self, plnr):
        """ aktiviert das speichern von smart-daten
        """
        try :
            aktpl = self.getPlatteCfg(plnr)
            dev1 = aktpl[SECT_DISCCFG_DEV][:-1]
            self.__log.debug('+- SMART-Daten auf Platte "%s" speichern einschalten' % dev1)
            cmd1 = 'smartctl -s on -o on -S on -d auto %s' % dev1

            self.__log.debug('|- CMD: %s' % cmd1)
            (status, text1, code1) = self.__shellcmd.runShellCmd(cmd1)
            self.__log.debug('|- Ergebnis: status=%s, text=%s, code=%s' % (str(status), str(text1), str(code1)))
            if status == True:
                self.__log.info('|- SMART-Daten speichern aktiviert auf %s' % dev1)
            else :
                self.__log.warning('Fehler rc=%d, Msg: %s' % (code1, text1))

            self.__log.debug('-- SMART-Daten speichern einschalten fertig')
        except :
            self.__log.error(str(formatExceptionInfo()))
      
    def __smartRunTest(self, plnr, testtype):
        """ startet einen test
            'testtype': s = short test, l = long test
        """
        try :
            aktpl = self.getPlatteCfg(plnr)
            dev1 = aktpl[SECT_DISCCFG_DEV][:-1]
            self.__log.debug('+- SMART-Test "%s" starten auf %s' % (testtype, dev1))
            cmd1 = None
            if testtype.lower() == 's':
                cmd1 = 'smartctl -d auto -t short %s' % dev1
            elif testtype.lower() == 'l':
                cmd1 = 'smartctl -d auto -t long %s' % dev1
            else :
                self.__log.warning('|- ungültiger Testparameter "%s" (Soll: [s|l])' % testtype)

            if not isinstance(cmd1, type(None)):
                self.__log.debug('|- CMD: %s' % cmd1)
                (status, text1, code1) = self.__shellcmd.runShellCmd(cmd1)
                self.__log.debug('|- Ergebnis: status=%s, text=%s, code=%s' % (str(status), str(text1), str(code1)))
                if status == True:
                    self.__log.info('|- SMART-Test "%s" gestartet' % testtype)
                else :
                    self.__log.warning('Fehler rc=%d, Msg: %s' % (code1, text1))

            self.__log.debug('-- SMART-Test starten fertig')
        except :
            self.__log.error(str(formatExceptionInfo()))

    def __smartCheckTest(self, plnr):
        """ prüft ob ein test noch läuft
            Ergebnis: (<testcode>, infotext)
            testcode: -1 - bei fehler, 0 - bei test fertig, >0 wenn test noch läuft
        """
        try :
            aktpl = self.getPlatteCfg(plnr)
            dev1 = aktpl[SECT_DISCCFG_DEV][:-1]
            self.__log.debug('+- SMART-Test anzeigen fuer %s' % dev1)

            cmd1 = 'smartctl -d auto -c %s' % dev1
            self.__log.debug('|- CMD: %s' % cmd1)
            (status, text1, code1) = self.__shellcmd.runShellCmd(cmd1)
            self.__log.debug('|- Ergebnis: status=%s, text=%s, code=%s' % (str(status), str(text1), str(code1)))
            t1 = ''
            testcode = -1
            if status == True:
                l1 = text1.split('\n')
                cpy = False
                for i in l1:
                    # den text bis zum nächsten parameter kopieren
                    if i.lower().startswith('self-test execution status'):
                        t1 = i[len('Self-test execution status:      (   0)'):].strip()
                        cpy = True
                        p1 = len('Self-test execution status:      (')
                        testcode = int(i[p1:p1+4])
                    elif i.startswith('\t') and (cpy == True):
                        t1 += ' ' + i.strip()
                    elif (i.startswith('\t') == False) and (cpy == True):
                        cpy = False
                self.__log.debug('|- SMART-Test auf %s: rc=%d, %s' % (dev1, testcode, t1))
            else :
                self.__log.warning('Fehler rc=%d, Msg: %s' % (code1, text1))
      
            self.__log.debug('-- SMART-Test anzeigen fertig')
            return(testcode, t1)
        except :
            self.__log.error(str(formatExceptionInfo()))

    def __smartWaitForTestresult(self, plnr, maxtimesec=600):
        """ wartet bis testergebnis vorliegt
            returnwert: True wenn ergebnis vorliegt, False bei timeout
        """
        erg1 = False
        try :
            aktpl = self.getPlatteCfg(plnr)
            dev1 = aktpl[SECT_DISCCFG_DEV][:-1]
            self.__log.info('+- warten auf SMART-Testergebnis auf %s (max. %d Minuten)' % (dev1, maxtimesec / 60))
            dt1 = datetime.now()
            testok = False
            runminute = 0
            while (testok == False) and \
                ((datetime.now() - dt1) < timedelta(seconds=maxtimesec)):
                (rc1, t1) = self.__smartCheckTest(plnr)
                self.__log.debug('|- rc1=%d (%s), t1=%s' % (rc1, str(type(rc1)), t1))
                if rc1 == 0:
                    testok = True
                    break
                elif rc1 == -1:
                    self.__log.warning('|- Fehler: %s' % t1)
                    break
                elif 'self-test routine was aborted' in t1:
                    self.__log.warning('|- Fehler: %s' % t1)
                    break
                else :
                    # wartezeit anzeigen
                    diffmin = (datetime.now() - dt1).seconds / 120  # alle 2 minuten eine textausgabe
                    if diffmin != runminute:
                        runminute = diffmin
                        self.__log.info('|- warten... %d Min (%s)' % (diffmin * 2, t1))
                    self.__log.debug('|- warten... Zeit: %d Sek., %s' % ((datetime.now() - dt1).seconds, t1))
                time.sleep(10)
            dt2 = datetime.now() - dt1
            min1 = dt2.seconds / 60
      
            # timeout?
            if (datetime.now() - dt1) < timedelta(seconds=maxtimesec):
                erg1 = True   # kein timeout

            self.__log.info('-- warten auf SMART-Testergebnis fertig (%d min %d sek)' % (min1, dt2.seconds - (min1 * 60)))
        except :
            self.__log.error(str(formatExceptionInfo()))
        return erg1

    def __workSteckdosenTreiber(self, zustand):
        """ startet/stoppt den gewählten treiber für die steckdose
        """
        try :
            self.__log.debug('+- Steckdosentreiber start/stop: %s' % str(zustand))
            if zustand == True:
                b1 = self.__konfigdict.get(SECT_MISC, {}).get(SECT_MISC_PWROUTLET, None)
                self.__log.debug('|- Wert in der Konfig: %s' % b1)
                if isinstance(b1, type('')):
                    if isinstance(self.__steckdose, type(None)):
                        (ipadr, kennwort) = self.getLogin()
                        if b1 == VAL_PWROUTLET_GUDE:
                            self.__log.debug('|- aktiviere Gude-Treiber')
                            self.__steckdose = GudePowerStrip('gudedose', self.__log, self.getControlScript(), ipadr, kennwort)
                        else :
                            self.__log.warning('|- unbekannter Steckdosentyp: "%s"' % b1)
                    else :
                        self.__log.warning('|- Steckdose bereits aktiviert: "%s"' % str(self.__steckdose))
                else :
                    self.__log.warning('|- kein Steckdosentreiber definiert') 
            else :
                if not isinstance(self.__steckdose, type(None)):
                    self.__log.debug('|- deaktiviere Treiber')
                    del self.__steckdose
                    self.__steckdose = None

            self.__log.debug('-- Steckdosentreiber start/stop fertig')
        except :
            self.__log.error(str(formatExceptionInfo()))
      
    def setSteckdoseTreiber(self, wert):
        """ wählt den treiber für die ansteuerung der steckdose
        """
        try :
            self.__log.debug('+- Steckdose auswaehlen: %s' % wert)
            if wert in self.__steckdosentreiber:
                if not SECT_MISC in self.__konfigdict.keys():
                    self.__konfigdict[SECT_MISC] = {}
                self.__konfigdict[SECT_MISC][SECT_MISC_PWROUTLET] = wert
            self.__log.debug('-- Steckdose auswaehlen fertig')
        except :
            self.__log.error(str(formatExceptionInfo()))

    def getSteckdoseTreiber(self):
        """ holt die auswahl 
        """
        try :
            b1 = self.__konfigdict.get(SECT_MISC, {}).get(SECT_MISC_PWROUTLET, False)
            if not b1 in self.__steckdosentreiber:
                self.__log.warning('|- ungültiger Steckdosentreiber in der Konfig')
                b1 = None
            self.__log.debug('Steckdosentreiber: %s' % b1)
            return b1
        except :
            self.__log.error(str(formatExceptionInfo()))

    def setAutocheckFs(self, zustand):
        """ schaltet die autocheckfunktion ein
        """
        try :
            self.__log.debug('+- Autocheck schalten: %s' % str(zustand))
            if not isinstance(zustand, type(True)):
                self.__log.warning('|- Parameterfehler: zustand --> Bool')
                return
        
            if not SECT_MISC in self.__konfigdict.keys():
                self.__konfigdict[SECT_MISC] = {}
            self.__konfigdict[SECT_MISC][SECT_MISC_AUTOCHECKFS] = zustand
            self.__log.debug('-- Autocheck schalten fertig')
        except:
            self.__log.error(str(formatExceptionInfo()))

    def getAutocheckFs(self):
        """ holt den zustand von autocheck
        """
        try :
            b1 = self.__konfigdict.get(SECT_MISC, {}).get(SECT_MISC_AUTOCHECKFS, False)
            self.__log.debug('autocheck: %s (type: %s)' % (str(b1), str(type(b1))))
            return b1
        except :
            self.__log.error(str(formatExceptionInfo()))
  
    def setLogin(self, ipadr, kennwort):
        """ speichert den login
        """
        try :
            self.__log.debug('+- Login speichern')
            self.__log.debug('|- IP-Adresse: %s, Kennwort: %s' % (ipadr, kennwort))
            if isinstance(ipadr, type('')) and isinstance(kennwort, type('')):
                if (len(ipadr) > 8) and (len(kennwort) > 4):
                    if not SECT_LOGIN in self.__konfigdict.keys():
                        self.__log.debug('|- Abschnitt erstellen: %s' % SECT_LOGIN)
                        self.__konfigdict[SECT_LOGIN] = {}
                    self.__log.debug('|- Wert speichern: %s = %s' % (SECT_LOGIN_IPADR, ipadr))
                    self.__konfigdict[SECT_LOGIN][SECT_LOGIN_IPADR] = ipadr
                    self.__log.debug('|- Wert speichern: %s = %s' % (SECT_LOGIN_PASSWORD, kennwort))
                    self.__konfigdict[SECT_LOGIN][SECT_LOGIN_PASSWORD] = kennwort
            else :
                self.__log.warning('Parameterfehler: ipadr + kennwort muss String sein')
            self.__log.debug('-- Login speichern fertig') 
        except :
            self.__log.error(str(formatExceptionInfo()))

    def getLogin(self):
        """ liefert die logindaten
        """
        try :
            ablgn = self.__konfigdict.get(SECT_LOGIN, {})
            ipadr = ablgn.get(SECT_LOGIN_IPADR, '')
            kennw = ablgn.get(SECT_LOGIN_PASSWORD, '')
            return (ipadr, kennw)
        except :
            self.__log.error(str(formatExceptionInfo()))
      
    def setStrategy(self, numdiscs, numbkperdisc):
        """ stores the backup strategy
        """
        try :
            if isinstance(numdiscs, type(1)) and isinstance(numbkperdisc, type(1)):
                if anzplatten > 0:
                    if not SECT_STRATEGY in self.__konfigdict.keys():
                        self.__konfigdict[SECT_STRATEGY] = {}
                    self.__konfigdict[SECT_STRATEGY][SECT_STRATEGY_NUM_DISCS] = numdiscs
                    self.__konfigdict[SECT_STRATEGY][SECT_STRATEGY_NUM_BK_PER_DISC] = numbkperdisc
            else :
                self.__log.warning('wrong parameter: numdiscs, numbkperdisc muss "Int" sein')
        except:
            self.__log.error(str(formatExceptionInfo()))
  
    def getStrategy(self):
        """ gets the current state of backup stategy
        """
        try :
            if SECT_STRATEGY in self.__konfigdict.keys():
                return copy.deepcopy(self.__konfigdict[SECT_STRATEGY])
            else :
                return None
        except :
            self.__log.error(str(formatExceptionInfo()))
      
    def setPlatteKonfig(self, plnr, pin, name, geraet):
        """ speichert die konfig für eine platte
            plnr = zaehlnr der platte in der konfig,
            pin = Nr der Steckdose,
            name = Label der Platte,
            geraet = Blockdevice in Linux (/dev/sda...)
        """
        try :
            self.__log.debug('+- Plattenkonfig speichern')
            self.__log.debug('|- plnr = %s, pin = %s, name = %s, geraet = %s' % (str(plnr), str(pin), name, geraet))
            if isinstance(plnr, type(1)) and isinstance(pin, type(1)) and \
                isinstance(name, type('')) and isinstance(geraet, type('')):
                maxplnr = self.__konfigdict.get(SECT_STRATEGY, {}).get(SECT_STRATEGY_NUM_DISCS, 0)
                self.__log.debug('|- Anzahl Platten: %d' % maxplnr)
                if (plnr >= 0) and (plnr < maxplnr):
                    cfgnr = SECT_DISCCFG % plnr
                    if not cfgnr in self.__konfigdict.keys():
                        self.__konfigdict[cfgnr] = {}
                    self.__log.debug('|- speichern: [%s] %s = %d' % (cfgnr, SECT_DISCCFG_PIN, pin))
                    self.__konfigdict[cfgnr][SECT_DISCCFG_PIN] = pin
                    self.__log.debug('|- speichern: [%s] %s = %s' % (cfgnr, SECT_DISCCFG_NAME, name))
                    self.__konfigdict[cfgnr][SECT_DISCCFG_NAME] = name
                    self.__log.debug('|- speichern: [%s] %s = %s' % (cfgnr, SECT_DISCCFG_DEV, geraet))
                    self.__konfigdict[cfgnr][SECT_DISCCFG_DEV] = geraet
                else :
                    self.__log.warning('Parameterfehler: plnr = %d, max: %d' % (plnr, maxplnr - 1))
            self.__log.debug('-- Plattenkonfig speichern fertig')
        except :
            self.__log.error(str(formatExceptionInfo()))
      
    def getPlatteCfg(self, plnr):
        """ liefert die konfig der angeg. platte
        """
        try :
            cfgnr = SECT_DISCCFG % plnr
            if cfgnr in self.__konfigdict.keys():
                return copy.deepcopy(self.__konfigdict[cfgnr])
            else :
                self.__log.warning('Plattenkonfig "%d" existiert nicht' % plnr)
                return {}
        except :
            self.__log.error(str(formatExceptionInfo()))

    def addExcludeDir(self, verzname):
        """ fügt ein verzeichnis zur liste hinzu, das auszuschließende verzeichnis
            muß unterhalb eines der quellverzeichnisse sein
        """
        try :
            self.__log.debug('+- Excludeordner hinzufügen')
            absexcl = self.__konfigdict.get(SECT_EXCLUDEDIRS, {})
            anzexcl = absexcl.get(SECT_EXCLUDEDIRS_ANZ, 0)
            self.__log.debug('|- Anzahl aktuell: %d, Ordner neu: %s' % (anzexcl, verzname))
      
            if not SECT_EXCLUDEDIRS in self.__konfigdict.keys():
                self.__konfigdict[SECT_EXCLUDEDIRS] = {}
      
            # prüfen ob excludedir schon bekannt ist
            for i in range(anzexcl):
                if verzname.lower() == self.__konfigdict[SECT_EXCLUDEDIRS].get(SECT_EXCLUDEDIRS_DIR % i, '').lower():
                    self.__log.info('|- Excludeordner "%s" ist bereits bekannt' % verzname)
                    return
      
            # existenz des ordners prüfen
            for i in range(self.getAnzQuellDir()):
                fname = os.path.join(self.getQuellDir(i), verzname)
                self.__log.debug('|- test existenz von: %s' % fname)
                if os.path.exists(fname) == True:
                    self.__log.debug('|- Ordner gefunden, hinzufügen...')
                    self.__konfigdict[SECT_EXCLUDEDIRS][SECT_EXCLUDEDIRS_DIR % anzexcl] = verzname
                    anzexcl += 1

            self.__konfigdict[SECT_EXCLUDEDIRS][SECT_EXCLUDEDIRS_ANZ] = anzexcl
            self.__log.debug('-- Excludeordner hinzufügen fertig')
        except:
            self.__log.error(str(formatExceptionInfo()))
      
    def getAnzExcludeDir(self):
        """ liefert die anzahl der excludeordner
        """
        try :
            quelldirs = self.__konfigdict.get(SECT_EXCLUDEDIRS, {})
            anz1 = int(quelldirs.get(SECT_EXCLUDEDIRS_ANZ, 0))
            return anz1
        except :
            self.__log.error(str(formatExceptionInfo()))
    
    def getExcludeDir(self, dirnr):
        """ liefert ein excludeordner
        """
        try :
            anz1 = self.getAnzExcludeDir()
            if (0 <= dirnr) and (dirnr < anz1):
                excldirs = self.__konfigdict.get(SECT_EXCLUDEDIRS, {})
                fname = excldirs.get(SECT_EXCLUDEDIRS_DIR % dirnr, '')
                if len(fname) > 0:
                    return fname
                else :
                    self.__log.warning('Excludedir nicht gesetzt')
                    return None
            else :
                self.__log.warning('ungueltiger Parameter - ist: %d, soll: 0 ... %d' % (dirnr, anz1 - 1))
                return None
        except :
            self.__log.error(str(formatExceptionInfo()))

    def addQuellDir(self, dirname):
        """ fügt ein verzeichnis zur liste hinzu
        """
        try :
            # parameter prüfen
            self.__log.debug('+- Ordner hinzufuegen')
            if not isinstance(dirname, type('')):
                self.__log.warning('Parameterfehler: dirname --> String')
                return
            if len(dirname) == 0:
                self.__log.warning('Parameter dirname darf nicht leer sein')
                return
            if os.path.exists(dirname) == False:
                self.__log.warning('Ordner "%s" existiert nicht' % dirname)
                return

            # abschnitt erstellen
            if not SECT_SOURCEDIR in self.__konfigdict.keys():
                self.__log.debug('|- erstelle Abschnitt %s' % SECT_SOURCEDIR)
                self.__konfigdict[SECT_SOURCEDIR] = {}
            anz1 = int(self.__konfigdict[SECT_SOURCEDIR].get(SECT_SOURCEDIR_ANZDIR, 0))

            # prüfen ob quelldir schon bekannt ist
            for i in range(anz1):
                if dirname.lower() == self.__konfigdict[SECT_SOURCEDIR].get(SECT_SOURCEDIR_DIR % i, '').lower():
                    self.__log.info('|- Quellordner "%s" ist bereits bekannt' % dirname)
                    return

            # ordner an liste anhängen
            self.__log.debug('|- aktuelle Anzahl: %d' % anz1)
            anz1 += 1
            self.__log.debug('|- neue Anzahl: %d' % anz1)
            self.__konfigdict[SECT_SOURCEDIR][SECT_SOURCEDIR_ANZDIR] = anz1
            self.__log.debug('|- neuer Ordner: %s' % dirname)
            self.__konfigdict[SECT_SOURCEDIR][SECT_SOURCEDIR_DIR % int(anz1 - 1)] = dirname
            self.__log.debug('-- Ordner hinzufuegen fertig')
        except :
            self.__log.error(str(formatExceptionInfo()))

    def getAnzQuellDir(self):
        """ liefert die anzahl quellordner
        """
        try :
            quelldirs = self.__konfigdict.get(SECT_SOURCEDIR, {})
            anz1 = int(quelldirs.get(SECT_SOURCEDIR_ANZDIR, 0))
            return anz1
        except :
            self.__log.error(str(formatExceptionInfo()))

    def getQuellDir(self, dirnr):
        """ liefert ein quellordner
        """
        try :
            anz1 = self.getAnzQuellDir()
            if (0 <= dirnr) and (dirnr < anz1):
                quelldirs = self.__konfigdict.get(SECT_SOURCEDIR, {})
                fname = quelldirs.get(SECT_SOURCEDIR_DIR % dirnr, '')
                if len(fname) > 0:
                    return fname
                else :
                    self.__log.warning('Quelldir nicht gesetzt')
                    return None
            else :
                self.__log.warning('ungueltiger Parameter - ist: %d, soll: 0 ... %d' % (dirnr, anz1 - 1))
                return None
        except :
            self.__log.error(str(formatExceptionInfo()))

    def setMountPunkt(self, mpunkt):
        """ speichert den mountpunkt
        """
        try :
            if not isinstance(mpunkt, type('')):
                self.__log.warning('Parameterfehler: mpunkt --> String')
                return
            if len(mpunkt) == 0:
                self.__log.warning('Parameter mpunkt darf nicht leer sein')
                return
            if os.path.exists(mpunkt) == False:
                self.__log.warning('Ordner "%s" existiert nicht' % mpunkt)
                return
            if not SECT_MISC in self.__konfigdict.keys():
                self.__konfigdict[SECT_MISC] = {}
            self.__konfigdict[SECT_MISC][SECT_MISC_MOUNTPUNKT] = mpunkt
        except :
            self.__log.error(str(formatExceptionInfo()))

    def getMountPunkt(self):
        """ liefert den mountpunkt
        """
        try :
            absmisc = self.__konfigdict.get(SECT_MISC, {})
            mpunkt = absmisc.get(SECT_MISC_MOUNTPUNKT, '')
            if len(mpunkt) == 0:
                self.__log.warning('Mounktpunkt nicht gesetzt')
                return None
            else :
                return mpunkt
        except :
            self.__log.error(str(formatExceptionInfo()))
    
    def setControlScript(self, fname):
        """ speichert den namen des controlscript
        """
        try :
            if not isinstance(fname, type('')):
                self.__log.warning('Parameterfehler: fname --> String')
                return
            if len(fname) == 0:
                self.__log.warning('Parameter fname darf nicht leer sein')
                return
            if os.path.exists(fname) == False:
                self.__log.warning('Ordner "%s" existiert nicht' % fname)
                return
            if not SECT_MISC in self.__konfigdict.keys():
                self.__konfigdict[SECT_MISC] = {}
            self.__konfigdict[SECT_MISC][SECT_MISC_CONTROLSCRIPT] = fname
        except :
            self.__log.error(str(formatExceptionInfo()))

    def getControlScript(self):
        """ liefert das controlscript
        """
        try :
            absmisc = self.__konfigdict.get(SECT_MISC, {})
            fname = absmisc.get(SECT_MISC_CONTROLSCRIPT, '')
            if len(fname) == 0:
                self.__log.warning('Controlscript nicht gesetzt')
                return None
            else :
                return fname
        except :
            self.__log.error(str(formatExceptionInfo()))
    
    def setIniFile(self, fname, ignormiss=True):
        """ speichert die inidatei
        """
        try :
            if (not isinstance(fname, type(''))) or (not isinstance(ignormiss, type(True))):
                self.__log.warning('Parameterfehler: fname:string, ignormiss:bool')
            else :
                if ignormiss == False:
                    if os.path.exists(fname) == False:
                        self.__log.warning('INI-Datei existiert nicht "%s"' % fname)
                        return
                self.__inifile = fname
        except :
            self.__log.error(str(formatExceptionInfo()))
      
    def getIniFile(self):
        """ liefert die ini-datei
        """
        try :
            if isinstance(self.__inifile, type(None)):
                return None
            return copy.deepcopy(self.__inifile)
        except :
            self.__log.error(str(formatExceptionInfo()))
      
    def showSyntax(self):
        """ zeigt die syntax an
        """
        try :
            print ('Syntax: mghbackup.py <k|b|s|p|w|m|u|f|r> [parameter]')
            print ('   k Default-Konfigdaten in INI-Datei schreiben (ueberschreibt bestehende INI-Datei)')
            print ('   b Backup laut INI-Datei durchfuehren')
            print ('   s Status der Steckdosen anzeigen')
            print ('   p Steckdose schalten: p <1|...%d> <on|off>' % self.__steckdose.getNumPwrOutlets())
            anzhd = self.__konfigdict.get(SECT_STRATEGY, {}).get(SECT_STRATEGY_NUM_DISCS, 0) - 1
            print ('   w nach einschalten auf Platte warten: w <0|...%s>' % anzhd)
            print ('   m Mount Platte: m <0|...%s>' % anzhd)
            print ('   u Unmount Platte: u <0|...%s>' % anzhd)
            print ('   f Dateisystemcheck: f <0|...%s>' % anzhd)
            print ('   r SMART-Status: r <0|...%s> <A|a|t|x|i|s>' % anzhd)
            print ('     (A: Attribute, a: alles, t: Temperatur, x: wirklich alles, i: info, s: selftest)')
            print ('   t SMART-Selftest starten: t <0|...%s> <l|s> (l = longtest, s = shorttest)' % anzhd)
            print ('   e SMART-Testergebnis: e <0|...%s>' % anzhd)
        except :
            self.__log.error(str(formatExceptionInfo()))

    def __convertToDatetime(self, zeittext):
        """ konvertiert einen text in ein datetime-Objekt
            'Tue Jan 28 11:53:33 2014'
        """
        erg1 = None
        try :
            self.__log.debug('+- Datum umwandeln: %s' % zeittext)
      
            # doppelte leerzeichen entfernen
            zeittext = zeittext.replace('  ',' ').replace('  ',' ').replace('  ',' ')
            l1 = zeittext.split(' ')
            if len(l1) != 5:
                self.__log.warning('|- Zeittext unklar: %s (Soll: TTT MMM DD HH:MM:ss YYYY)' % zeittext)
            t1 = {'jan':1,'feb':2,'mar':3,'apr':4,'may':5,'jun':6,'jul':7,'aug':8,'sep':9,'oct':10,'nov':11,'dec':12}
            mon1 = t1.get(l1[1].lower(), 0)
            tag1 = int(l1[2])
            jahr1 = int(l1[4])
            h1 = int(l1[3][:2])
            m1 = int(l1[3][3:5])
            s1 = int(l1[3][6:])
            self.__log.debug('|- umgewandelt: YMD: %s.%s.%s, HMS: %s:%s:%s' % (jahr1, mon1, tag1, h1, m1, s1))
            erg1 = datetime(jahr1, mon1, tag1, h1, m1, s1)
            self.__log.debug('+- Datum umwandeln fertig: %s' % str(erg1))
        except :
            self.__log.error(str(formatExceptionInfo()))
        return erg1
      
    def __getFilesystemStatistik(self, plnr):
        """ fragt statistische werte vom dateisystem ab
        """
        erg1 = {}
        try :
            self.__log.debug('+- Dateisystemstatistik auslesen')
            if not isinstance(plnr, type(1)):
                self.__log.warning('|- Parameterfehler: plnr --> Int')
                return {}
            if (plnr < 0) or (plnr >= self.__konfigdict[SECT_STRATEGY][SECT_STRATEGY_NUM_DISCS]):
                self.__log.warning('|- Parameterfehler: 0 <= plnr < %d' % self.__konfigdict[SECT_STRATEGY][SECT_STRATEGY_NUM_DISCS])
        
            # dateisystem abfragen
            cmd1 = 'dumpe2fs -h %s' % self.getPlatteCfg(plnr)[SECT_DISCCFG_DEV]
            self.__log.debug('|- CMD: %s' % cmd1)
            (status, text1, code1) = self.__shellcmd.runShellCmd(cmd1)
            self.__log.debug('|- Ergebnis: status=%s, text=%s, code=%s' % (str(status), str(text1), str(code1)))

            if status == True:
                l1 = text1.split('\n')
                for i in l1:
                    if not ':' in i:
                        continue
                    l2 = i.split(':')
                    if len(l2) > 1:
                        key1 = l2[0].strip()
                        val1 = ''
                        for k in l2[1:]:
                            if len(val1) > 0:
                                val1 += ':'
                            val1 += k.strip()
    
                        if key1 in ['Inode count','Block count','Reserved block count','Free blocks',\
                                'Free inodes','First block','Block size','Fragment size','Reserved GDT blocks',\
                                'Blocks per group','Fragments per group','Inodes per group',\
                                'Inode blocks per group','Flex block group size','Mount count',\
                                'Maximum mount count','First inode','Inode size','Required extra isize',\
                                'Desired extra isize','Journal inode','Journal-Start']:
                            erg1[key1] = int(val1)
                        elif key1 in ['Filesystem created','Last mount time','Last write time','Last checked']:
                            erg1[key1] = self.__convertToDatetime(val1)
                        else :
                            erg1[key1] = val1
                self.__log.debug('|- Wert: %s' % str(erg1))
            else :
                self.__log.warning('|- Fehler: rc=%d, Msg: %s' % (code1, text1))
      
            self.__log.debug('-- Dateisystemstatistik auslesen fertig')
        except :
            self.__log.error(str(formatExceptionInfo()))
        return erg1

    def showSteckdosen(self):
        """ zeigt den zustand der steckdosen an
        """
        try :
            l1 = self.__steckdose.getStatePwrOutlet(0)
            self.__log.info('+- Status der Steckdosen:')
            cnt1 = 1
            for i in l1:
                self.__log.info('|-  %s: %s' % (cnt1, i))
                cnt1 += 1
            self.__log.info('-- Status der Steckdosen fertig')
        except :
            self.__log.error(str(formatExceptionInfo()))

    def mountPlatte(self, plattenr, zustand):
        """ mountet eine festplatte,
            plattenr - Nr der Plattendefinition,
            zustand - True = mounten, False = unmounten
        """
        erg1 = False
        try :
            self.__log.debug('+- Platte un/mounten: %s, %s' % (plattenr, zustand))
            if (not isinstance(plattenr, type(1))) and (not isinstance(zustand, type(True))):
                self.__log.warning('|- Parameterfehler: plattenr --> Int (ist: %s), zustand --> Bool (ist: %s)' % \
                        (str(type(plattenr)), str(type(zustand))))
                return erg1
            if (plattenr < 0) or (plattenr >= self.__konfigdict[SECT_STRATEGY][SECT_STRATEGY_NUM_DISCS]):
                self.__log.warning('|- Parameterfehler: 0 <= plattenr < %d (ist: %d)' % \
                    self.__konfigdict[SECT_STRATEGY][SECT_STRATEGY_NUM_DISCS], plattenr)
                return erg1

            if zustand == True:
                dev1 = self.getPlatteCfg(plattenr)[SECT_DISCCFG_DEV]
                cmd1 = 'mount %s %s' % (dev1, self.__konfigdict[SECT_MISC][SECT_MISC_MOUNTPUNKT])
                self.__log.info('|- mounte %s --> %s' % (dev1, self.__konfigdict[SECT_MISC][SECT_MISC_MOUNTPUNKT]))
            else :
                cmd1 = 'umount %s' % (self.__konfigdict[SECT_MISC][SECT_MISC_MOUNTPUNKT])
                self.__log.info('|- unmounte %s' % self.__konfigdict[SECT_MISC][SECT_MISC_MOUNTPUNKT])
            self.__log.debug('|- CMD: %s' % cmd1)
            (status, text1, code1) = self.__shellcmd.runShellCmd(cmd1)
            self.__log.debug('|- Ergebnis: status=%s, text=%s, code=%s' % (str(status), str(text1), str(code1)))
            if status == True:
                self.__log.info('|- u/mount fertig (%s)' % self.__konfigdict[SECT_MISC][SECT_MISC_MOUNTPUNKT])
                erg1 = True
            else :
                self.__log.warning('|- Fehler: rc=%d, Msg: %s' % (code1, text1))
            self.__log.debug('-- Platte un/mounten fertig')
        except :
            self.__log.error(str(formatExceptionInfo()))
        return erg1

    def __warteAufPlatte(self, plattenr):
        """ wartet auf das auftauchen der angegebenen festplatte
        """
        erg1 = False
        try :
            self.__log.debug('+- auf Platte warten')
            if not isinstance(plattenr, type(1)):
                self.__log.warning('|- Parameterfehler: plattenr --> Int')
                return erg1
            if (plattenr < 0) or (plattenr >= self.__konfigdict[SECT_STRATEGY][SECT_STRATEGY_NUM_DISCS]):
                self.__log.debug('|- Parameterfehler: 0 <= plattenr < %d' % self.__konfigdict[SECT_STRATEGY][SECT_STRATEGY_NUM_DISCS])
                return erg1
            
            # auf platte warten
            dt1 = datetime.now()
            dev1 = self.getPlatteCfg(plattenr)[SECT_DISCCFG_DEV]
            self.__log.info('|- warte auf %s...' % dev1)

            while ((datetime.now() - dt1) < timedelta(seconds=90.0)):
                cmd1 = 'ls %s' % dev1
                self.__log.debug('|- CMD: %s' % cmd1)
                (status, text1, code1) = self.__shellcmd.runShellCmd(cmd1)
                self.__log.debug('|- Ergebnis: status=%s, text=%s, code=%s' % (str(status), str(text1), str(code1)))
                if status == True:
                    erg1 = True
                    break
                else :
                    if code1 != 2:
                        self.__log.warning('|- OS-Error unerwartet: %d, Msg: %s' % (code1, text1))
                time.sleep(1.0)

            if erg1 == True:
                # label der platte abfragen
                cmd1 = 'e2label %s' % dev1
                self.__log.debug('|- Label abfragen, CMD: %s' % cmd1)
                (status, text1, code1) = self.__shellcmd.runShellCmd(cmd1)
                self.__log.debug('|- Ergebnis: status=%s, text=%s, code=%s' % (str(status), str(text1), str(code1)))
                if status == True:
                    plname = text1.strip()
                else :
                    plname = 'kein Zugriff - sudo noetig'
                self.__log.info('|- warten ende, Platte aktiv (Label: %s)' % plname)
            else :
                self.__log.info('|- warten ende, Timeout')
            self.__log.debug('-- auf Platte warten fertig')
        except :
            self.__log.error(str(formatExceptionInfo()))
        return erg1

    def runRsync(self, dname, aktpl):
        """ den kopiervorgang ausführen
        """
        erg1 = False
        try :
            self.__log.debug('+- rsync ausfuehren')

            # evtl. zielverzeichnis erstellen
            ziel = os.path.join(self.getMountPunkt(), dname)
            if os.path.exists(ziel) == False:
                self.__log.info('Verzeichnis erstellen: %s' % ziel)
                os.makedirs(ziel)
            lastdir = os.path.join(self.getMountPunkt(), 'last')

            for i in range(self.getAnzQuellDir()):
                # exclude-dirs erstellen, sofern diese im quellverzeichnis existieren
                excudedirs = ''
                for k in range(self.getAnzExcludeDir()):
                    exclname = os.path.join(self.getQuellDir(i), self.getExcludeDir(k))
                    if os.path.exists(exclname):
                        excudedirs += '--exclude=%s ' % self.getExcludeDir(k)

                # existiert 'last'-verzeichnis?
                if os.path.exists(lastdir) == False:
                    cmd1 = 'rsync -aRrv --progress --delete --delete-excluded %s %s %s' % \
                        (excudedirs, self.getQuellDir(i), ziel)
                else :
                    # hard-links erstellen, wenn die datei nicht geändert wurde
                    cmd1 = 'rsync -aRr --link-dest=%s --delete --delete-excluded %s %s %s' % \
                        (lastdir, excudedirs, self.getQuellDir(i), ziel)

                # dateien kopieren
                self.__log.debug('|- CMD: %s' % cmd1)
                self.__log.info('|- kopiere "%s" --> "%s"' % (self.getQuellDir(i), ziel))
                (status, text1, code1) = self.__shellcmd.runShellCmd(cmd1)
                self.__log.debug('|- Ergebnis: status=%s, text=%s, code=%s' % \
                        (str(status), str(text1), str(code1)))
                if status == True:
                    self.__log.info('|- Ordner "%s" erfolgreich nach "%s" kopiert' % (self.getQuellDir(i), ziel))
                else :
                    self.__log.warning('|- Fehler bei rsync: rc=%d, Msg: %s' % (code1, text1))
                    erg1 = False

            # alten lastdir-link löschen
            self.__log.debug('|- Lastdir-Link loeschen: %s' % lastdir)
            if os.path.exists(lastdir) == True:
                cmd1 = 'rm %s' % (lastdir)
                self.__log.debug('|- CMD: %s' % cmd1)
                (status, text1, code1) = self.__shellcmd.runShellCmd(cmd1)
                self.__log.debug('|- Ergebnis: status=%s, text=%s, code=%s' % (str(status), str(text1), str(code1)))
                if status == True:
                    self.__log.info('|- Link loeschen fertig: %s' % (lastdir))
                else :
                    self.__log.warning('Fehler beim Link loeschen: rc=%d, Msg: %s' % (code1, text1))

            # lastdir auf neues verzeichnis setzen
            cmd1 = 'ln -s %s %s' % (ziel, lastdir)
            self.__log.debug('|- CMD: %s' % cmd1)
            (status, text1, code1) = self.__shellcmd.runShellCmd(cmd1)
            self.__log.debug('|- Ergebnis: status=%s, text=%s, code=%s' % (str(status), str(text1), str(code1)))
            if status == True:
                self.__log.info('|- Link setzen fertig: %s --> %s' % (ziel, lastdir))
            else :
                self.__log.warning('Fehler beim Link setzen: rc=%d, Msg: %s' % (code1, text1))

            self.__log.debug('-- rsync ausfuehren fertig')
        except :
            self.__log.error(str(formatExceptionInfo()))
        return erg1

    def showPlatzAufRechner(self):
        """ zeigt den platz auf dem Rechner an
        """
        try :
            cmd1 = 'df -h'
            self.__log.debug('|- CMD: %s' % cmd1)
            (status, text1, code1) = self.__shellcmd.runShellCmd(cmd1)
            self.__log.debug('|- Ergebnis: status=%s, text=%s, code=%s' % (str(status), str(text1), str(code1)))
            if status == True:
                l1 = text1.split('\n')
                self.__log.info('+- Platz auf dem System')
                for i in l1:
                    self.__log.info('|- %s' % i)
                self.__log.info('-- Platz auf dem System fertig')
            else :
                self.__log.warning('|- Fehler: rc=%d, Msg: %s' % (code1, text1))
        except :
            self.__log.error(str(formatExceptionInfo()))

    def cleanOldBackups(self):
        """ löscht alte backups
        """
        try :
            self.__log.debug('+- alte Backups loeschen')
            l1 = os.listdir(self.__konfigdict[SECT_MISC][SECT_MISC_MOUNTPUNKT])
            self.__log.debug('|- Ordner in "%s": %s' % \
                        (self.__konfigdict[SECT_MISC][SECT_MISC_MOUNTPUNKT], str(l1)))
            if 'last' in l1:
                l1.remove('last')
            if 'lost+found' in l1:
                l1.remove('lost+found')
            l1.sort() # älteste zuerst

            oldlen = len(l1)
            while len(l1) > self.__konfigdict[SECT_STRATEGY][SECT_STRATEGY_NUM_BK_PER_DISC]:
                rmdir = os.path.join(self.__konfigdict[SECT_MISC][SECT_MISC_MOUNTPUNKT], l1[0])
                cmd1 = 'rm -r %s' % rmdir

                self.__log.debug('|- CMD: %s' % cmd1)
                (status, text1, code1) = self.__shellcmd.runShellCmd(cmd1)
                self.__log.debug('|- Ergebnis: status=%s, text=%s, code=%s' % (str(status), str(text1), str(code1)))
                if status == True:
                    self.__log.info('|- Verzeichnis "%s" geloescht' % rmdir)
                else :
                    self.__log.warning('|- Fehler beim Loeschen: rc=%d, Msg: %s' % (code1, text1))
                del l1[0]
            if oldlen == len(l1):
                self.__log.info('|- nichts zu loeschen, Anzahl Backups: %d' % oldlen)

            self.__log.debug('-- alte Backups loeschen fertig')
        except :
            self.__log.error(str(formatExceptionInfo()))
      
    def autofixFilesystem(self, plnr):
        """ prüft und repariert evtl. das dateisystem
        """
        try :
            if self.getAutocheckFs():
                fsdat = self.__getFilesystemStatistik(plnr)
                mountcount = fsdat.get('Mount count', 0)
                lastcheck = fsdat.get('Last checked', datetime.now())
                fsstatus = fsdat.get('Filesystem state', 'clean')
                self.__log.debug('|- Mountcount = %d, Lastcheck: %s, Filesystem state: %s' % \
                        (mountcount, str(lastcheck), fsstatus))

                # evtl. reparatur auslösen
                dev1 = self.getPlatteCfg(plnr)[SECT_DISCCFG_DEV]
                if (fsstatus != 'clean') or (mountcount > 60) or \
                    ((datetime.now() - lastcheck) > timedelta(days=90)):
                    self.__log.info('|- Dateisystemcheck auf "%s" noetig' % dev1)
                    cmd1 = 'fsck -f -y %s' % dev1
                    self.__log.debug('|- CMD: %s' % cmd1)
                    (status, text1, code1) = self.__shellcmd.runShellCmd(cmd1)
                    self.__log.debug('|- Ergebnis: status=%s, text=%s, code=%s' % (str(status), str(text1), str(code1)))
                    if status == True:
                        self.__log.info('|- Dateisystem "%s" geprueft, keine Fehler' % dev1)
                    else :
                        if code1 == 1:
                            self.__log.warning('|- Dateisystem "%s" geprueft, es wurden Fehler korrigiert (%s)' % (dev1, text1))
                        elif code1 == 2:
                            self.__log.warning('|- Dateisystem "%s" geprueft, System should be rebooted' % dev1)
                        elif code1 == 4:
                            self.__log.warning('|- Dateisystem "%s" geprueft, Filesystem errors left uncorrected' % dev1)
                        elif code1 == 8:
                            self.__log.warning('|- Dateisystem "%s" geprueft, Operational error' % dev1)
                        elif code1 == 16:
                            self.__log.warning('|- Dateisystem "%s" geprueft, Usage or syntax error' % dev1)
                        elif code1 == 32:
                            self.__log.warning('|- Dateisystem "%s" geprueft, Fsck canceled by user request' % dev1)
                        elif code1 == 128:
                            self.__log.warning('|- Dateisystem "%s" geprueft, Shared-library error' % dev1)
                else :
                    self.__log.warning('|- Fehler beim pruefen: rc=%d, Msg: %s' % (code1, text1))
            else :
                self.__log.info('|- Dateisystemcheck auf "%s" nicht noetig' % dev1)
        except :
            self.__log.error(str(formatExceptionInfo()))
    
    def doBackup(self):
        """ führt das backup aus
        """
        try :
            dt1 = datetime.now()
            self.__log.info('Vollbackup starten... (%s)' % dt1.strftime('%H:%M:%S, %d.%m.%Y'))
      
            # platte auswählen
            aktpl = self.__konfigdict[SECT_STRATEGY].get(SECT_STRATEGY_CURR_DISC, 0)
  
            # anzahl platten in verwendung
            anzhd = self.__konfigdict[SECT_STRATEGY][SECT_STRATEGY_NUM_DISCS]
            # nr des verzeichnisses
            anzbk = self.__konfigdict[SECT_STRATEGY][SECT_STRATEGY_NUM_BK_PER_DISC]
            aktbk = self.__konfigdict[SECT_STRATEGY].get(SECT_STRATEGY_CURR_BK_PER_DISC, -1)
            self.__log.debug('|- Strategie, alt: aktpl=%d, anzhd=%d, anzbk=%d, aktbk=%d' % \
                        (aktpl, anzhd, anzbk, aktbk))

            # verzeichniszähler erhöhen
            aktbk += 1
            if aktbk >= anzbk:
                # nächste platte wählen
                aktbk = 0
                aktpl += 1
                if aktpl >= anzhd:
                    aktpl = 0

            # geänderte einstellung merken
            self.__konfigdict[SECT_STRATEGY][SECT_STRATEGY_CURR_BK_PER_DISC] = aktbk
            self.__konfigdict[SECT_STRATEGY][SECT_STRATEGY_CURR_DISC] = aktpl
            self.__log.debug('|- Strategie, neu: aktpl=%d, anzhd=%d, anzbk=%d, aktbk=%d' % \
                        (aktpl, anzhd, anzbk, aktbk))

            # backupverzeichnis wählen
            dname = datetime.now().strftime('%Y%m%d')

            aktdict = self.__konfigdict[SECT_DISCCFG % aktpl]
            self.__log.info('|- Verz: %s, Platte: %s' % (dname, str(aktdict)))
      
            # platte einschalten
            if self.__steckdose.schaltSteckdose(aktdict[SECT_DISCCFG_PIN], True):
                # auf das hochlaufen der platte warten
                self.__log.info('|- Platte %s eingeschaltet (Dose: %s)' % \
                        (aktdict[SECT_DISCCFG_NAME], aktdict[SECT_DISCCFG_PIN]))
                if self.__warteAufPlatte(aktpl):
                    # smart-daten speichern einschalten
                    if self.getSmartCheck() == True:
                        self.__smartEnaSave(aktpl)

                    # autocheck?
                    self.autofixFilesystem(aktpl)
    
                    # platte mounten + backup   
                    if self.mountPlatte(aktpl, True):
                        self.runRsync(dname, aktpl)
                        self.cleanOldBackups()
                        self.showPlatzAufRechner()
                        self.mountPlatte(aktpl, False)
              
                    # nach dem backup wird der plattentest durchgeführt
                    if self.getSmartCheck() == True:
                        # das erste backup in der serie auf der aktuellen platte wird mit long-check gemacht
                        if aktbk == 0:
                            self.__smartRunTest(aktpl, 'l') # long-test starten
                        else :
                            self.__smartRunTest(aktpl, 's') # short-test starten
    
                    # SMART-Daten auswerten
                    if self.getSmartCheck() == True:
                        # ergebnis abwarten
                        if aktbk == 0:
                            rc1 = self.__smartWaitForTestresult(aktpl, maxtimesec=60 * 400)  # 400 minuten, 6,5h
                        else :
                            rc1 = self.__smartWaitForTestresult(aktpl, maxtimesec=60 * 10)   # 10 minuten
                        if rc1 == True:
                            self.__smartGetStatus(aktpl, 's')
                        else :
                            self.__log.info('|- Selftest noch nicht fertig')
                            self.__smartGetStatus(aktpl, 's')

                # ein paar sekunden warten bevor die platte abgeschaltet wird
                self.__log.info('|- vor dem Abschalten der Platte 7 Sekunden warten...')
                time.sleep(7)
                self.__steckdose.schaltSteckdose(aktdict[SECT_DISCCFG_PIN], False)

            dt1 = datetime.now()
            self.__log.info('Vollbackup fertig (%s)' % dt1.strftime('%H:%M:%S, %d.%m.%Y'))
        except :
            self.__log.error(str(formatExceptionInfo()))

    def runConsoleCommands(self):
        """ führt kommandos der console aus
        """
        try :
            if len(sys.argv) > 1:
                if os.name == 'posix':
                    unbekpara = []
                    argp = 1
                    step = 0
                    for i in sys.argv[1:]:
                        if step > 0:
                            step -= 1
                            continue
                        if i.lower() == 'k':    # write config
                            self.saveConfig()
                        elif i.lower() == 'b':  # run backup
                            self.doBackup()
                        elif i.lower() == 's':  # show power outlet
                            self.showSteckdosen()
                        elif i.lower() == 'w':  # wait for hard disc spin up
                            if len(sys.argv) > (argp + 1):
                                step = 1
                                self.__warteAufPlatte(int(sys.argv[2]))
                            else :
                                self.showSyntax()
                        elif i.lower() == 'p':  # steckdosen schalten
                            if len(sys.argv) > (argp + 2):
                                step = 2
                                if (sys.argv[2] in ['1','2','3','4']) and (sys.argv[3].lower() in ['on','off']):
                                    zu1 = False
                                    if sys.argv[3].lower() == 'on':
                                        zu1 = True
                                    self.__steckdose.schaltSteckdose(int(sys.argv[2]), zu1)
                                else :
                                    self.showSyntax()
                            else :
                                self.showSyntax()
                        elif i.lower() == 'm':  # mount disc
                            if len(sys.argv) > (argp + 1):
                                step = 1
                                self.mountPlatte(int(sys.argv[2]), True)
                            else :
                                self.showSyntax()
                        elif i.lower() == 'u':  # unmount disc
                            if len(sys.argv) > (argp + 1):
                                step = 1
                                self.mountPlatte(int(sys.argv[2]), False)
                            else :
                                self.showSyntax()
                        elif i.lower() == 'r':    # smart-werte
                            if len(sys.argv) > (argp + 2):
                                step = 2
                                self.__smartEnaSave(int(sys.argv[2]))
                                self.__smartGetStatus(int(sys.argv[2]), sys.argv[3])
                            else :
                                self.showSyntax()
                        elif i.lower() == 't':    # smart-selftest starten
                            if len(sys.argv) > (argp + 2):
                                step = 2
                                if sys.argv[3] in ['s','l']:
                                    self.__smartRunTest(int(sys.argv[2]), sys.argv[3])
                                else :
                                    self.showSyntax()
                            else :
                                self.showSyntax()
                        elif i.lower() == 'e':    # smart-test-ergebnis
                            if len(sys.argv) > (argp + 1):
                                step = 1
                                aktpl = int(sys.argv[2])
                                if self.__smartWaitForTestresult(aktpl) == True:
                                    self.__smartGetStatus(aktpl, 's')
                                else :
                                    self.__log.info('|- Selftest noch nicht fertig')
                                    self.__smartGetStatus(aktpl, 's')
                            else :
                                self.showSyntax()
                        elif i.lower() == 'f':  # dateisystemcheck
                            if len(sys.argv) > (argp + 1):
                                step = 1
                                self.autofixFilesystem(int(sys.argv[2]))
                            else :
                                self.showSyntax()
                        else :
                            unbekpara.append(i)
                        argp += 1
          
                    if len(unbekpara) > 0:
                        self.showSyntax()
                        self.__log.warning('unbekannte Parameter: %s' % str(unbekpara))
                else :
                    self.__log.warning('Falsches Betriebssystem: "%s", Linux wird benoetigt. Stop.' % os.name)
            else :
                self.showSyntax()
        except :
            self.__log.error(str(formatExceptionInfo()))
# ende ExtBackupSteckdose

# -*- coding: utf-8 -*-

from mdsshellcommand import ShellCommandRun
from mdslogger import formatExceptionInfo


class GudePowerStrip:
    """ control a power strip of company 'Gude'
    """
    def __init__(self, jobname, logger, ctrlscript, ipadr, password):
        """ settings
        """
        self.__jobname = jobname
        self.__log = logger
        self.__controlscript = ctrlscript
        self.__password = password
        self.__ipadr = ipadr
        self.__shellcmd = ShellCommandRun('gudebox', self.__log)

    def __del__(self):
        """ clean up
        """
        if not isinstance(self.__shellcmd, type(None)):
            del self.__shellcmd
            self.__shellcmd = None

    def __checkDeviceAnswer(self, ergtxt, outletnr):
        """ read the state of a power outlet from the answer text of the control script
        """
        erg1 = None
        try :
            self.__log.debug('+- reading answer of control script')

            l1 = ergtxt.split('\n')
            for i in l1:
                if (len(i) == 0) or (i.startswith('sending')):
                    continue
                l2 = i.split(' ')
                if len(l2) == 5:
                    if (l2[0].lower() == 'power') and \
                        (l2[1].lower() == 'port') and \
                        (l2[3].lower() == 'is'):
                        if l2[2] == str(outletnr):
                            if l2[4].lower() == 'on':
                                erg1 = True
                                break
                            elif l2[4].lower() == 'off':
                                erg1 = False
                                break
                            else :
                                self.__log.warning('wrong state answer: %s [on, off]' % l2[4].lower())
                                erg1 = None
                                break
                    else :
                        self.__log.warning('wrong description: %s %s %s (expected: power port is)' % \
                            (l2[0].lower(), l2[1].lower(), l2[3].lower()))
                else :
                    self.__log.warning('undefind answer, wrong length: %s (expected 5)' % len(l2)) 
      
            self.__log.debug('-- reading answer of control script - done, Result=%s' % str(erg1))
        except :
            self.__log.error(str(formatExceptionInfo()))
        return erg1
      
    def getNumPwrOutlets(self):
        """ get number of available power outets
        """
        return 4
    
    def getStatePwrOutlet(self, outletnr):
        """ queries the state of the power outlet,
            'outletnr' - nr of power outlet [1,...] 0 = all (list),
            retuen: True if active, False if inactive, None if error
        """
        erg1 = None
        try :
            self.__log.debug('+- show state of power outlets')
            if not isinstance(outletnr, type(1)):
                self.__log.warning('|- wrong parameter: socketnr must be Int (got: %s)' % str(type(outletnr)))
                return None
            if not outletnr in [0, 1, 2, 3, 4]:
                self.__log.warning('|- wrong parameter - allowed range: 0 <= socketnr <= 4, got: %s' % str(outletnr))
                return None
      
            cmd1 = '%s --host=%s --password=%s' % (self.__controlscript, self.__ipadr, self.__password)
            self.__log.debug('|- CMD: %s' % cmd1)
            (status, text1, code1) = self.__shellcmd.runShellCmd(cmd1)
            self.__log.debug('|- result: state=%s, text=%s, code=%s' % (str(status), str(text1), str(code1)))

            if status == True:
                if outletnr == 0:
                    erg1 = []
                    for i in range(4):
                        erg1.append(self.__checkDeviceAnswer(text1, i + 1))
                else :
                    erg1 = self.__checkDeviceAnswer(text1, outletnr)
            else :
                self.__log.warning('|- error: %s (rc=%s)' % text, code1)
            self.__log.debug('-- show state of power outlets - done, erg=%s' % str(erg1))
        except :
            self.__log.error(str(formatExceptionInfo()))
        return erg1
  
    def switchPwrOutlet(self, outletnr, state):
        """ turns power outlet on/off,
            outletnr: Int 1...4 - No of power outlet to turn,
            state: Bool - True = an, False = aus,
            return: True = success, False = error
        """
        try :
            self.__log.debug('+- turning outlet: %s --> %s' % (str(outletnr), str(state)))
            if (not isinstance(outletnr, type(1))) or (not isinstance(state, type(True))):
                self.__log.warning('|- wrong parameter - outletnr: expected String (got: %s), state: expected Bool (got: %s)' % \
                    (str(type(outletnr)), str(type(state))))
                return False
        
            # create command
            zu1 = 'off'
            if state == True:
                zu1 = 'on'
            cmd1 = '%s --host=%s --password=%s -p=%d -%s' % \
                (self.__controlscript, self.__ipadr, self.__password, outletnr, zu1)
            self.__log.debug('|- CMD: %s' % cmd1)

            # run action
            (rstat, text1, code1) = self.__shellcmd.runShellCmd(cmd1)
            self.__log.debug('|- result: state=%s, text=%s, code=%s' % (str(rstat), str(text1), str(code1)))

            if rstat == True:
                self.__log.info('power outlet "%d" turned successful, new state: %s' % (outletnr, str(state)))
            else :
                self.__log.warning('|- error while turning power outlet: Text=%s, Code=%s' % (text1, str(code1)))
                return False
      
            self.__log.debug('-- turning outlet - done')
            return True
        except :
            self.__log.error(str(formatExceptionInfo()))
            return False

# ende GudePowerStrip


from subprocess import Popen, PIPE
import sys
import os
import logging
import xml.parsers.expat

from .Utils import Stack, DefaultDict


class Shell(object):
    """Base Shell class for gathering shell environment information"""
    
    def __init__(self):
        super(Shell, self).__init__()
        self.GDI = None
        self.err = sys.stderr
        self.out = sys.stdout
    
    def env():
        doc = "the current shell environmnet"

        def fget(self):
            return dict(os.environ)

        def fset(self, **args):
            for k, v in args.items():
                os.environ[k] = v
        return locals()
    env = property(**env())

    def getConnection(self):
        """Return the GDI connection instance"""
        raise NotImplementedError("Shell.getConnection()")

    def getErr(self):
        """
        get the error output writer, for redirecting any error output to,
        by default this is sys.stderr
        """
        return self.err if self.err is not None else sys.stderr

    def getOut(self):
        """
        get the stadard output writer, for redirecting any standard output to,
        by default this is sys.stdout
        """
        return self.out if self.out is not None else sys.stdout

    def getLogger(self):
        """return the logger instance if it exists ready for logging command output"""
        return logging.getLogger(self.__name__)


class AbstractCommand(object):
    """
    Base commad class used to create and run commandline applications,
    this class is inherited by other command classes
    """
    def __init__(self, shell=None):
        if not isinstance(shell, Shell):
            self.shell = Shell()
        else:
            self.shell = shell

        self.gdi = None  # pointer to GDI interface instance (not implimented yet)
        self.commad = "ls"
        self.exit_code = 0
        self.out = ""
        self.err = ""

    def run(self, *args, **kwargs):
        """run the given arguments in the shell"""
        
        _cmd = [self.command]
        for a in args:  # needs a little clean-up and sanity check happening here
            _cmd += a
        for k, v in kwargs:  # needs a little clean-up and sanity check happening here
            _cmd += k
            _cmd += v

        print ' '.join(_cmd)
        process = Popen(_cmd, stdout=PIPE, stderr=PIPE)
        out, err = process.communicate()
        process.wait()
        self.out = out
        self.err = err

        return process.returncode

    @classmethod
    def getExitCode(self):
        """Return the exit status of this command"""
        return self._exit_code

    @classmethod
    def setExitCode(self, code):
        """Return the exit status of this command"""
        self._exit_code = code
        return self._exit_code

    @classmethod
    def getUsage(self):
        """Return the usage stringfor the command"""
        return ""

    @classmethod
    def printCommand(self):
        """Print the command that was ran to stdout"""
        print self._cmd
    
    @classmethod
    def function(self):
        pass


class QConfOptions(object):
    """
    QConfOptions object for convienence of setting and editing the
    commandline arguments of the QConfCommand Class
    """

    args = {}


class QConfCommand(AbstractCommand):
    """
    QConfCommand class for running configuration querys and commands
    """
    def __init__(self):
        super(QConfCommand, self).__init__()
    
    def addAdminHost(self, options):
        _args = {}
    
    def addSubmitHost(self, options):
        pass
    
    def addCalendar(self):
        pass
    
    def addOperator(self):
        pass
    
    def addManager(self):
        pass
    
    def addHostgroup(self):
        pass
    
    def addConfiguration(self):
        pass
    
    def addCheckpoint(self):
        pass
    
    def addUserSet(self):
        pass
    
    def addShareTree(self):
        pass
    
    def addExecHost(self):
        pass
    
    def modifyComplexEntry(self):
        pass
    
    def modifyComplexEntryFromFile(self):
        pass
    
    def modifyShareTree(self):
        pass
    
    def modifyShareTreeFromFile(self):
        pass
    
    def modifyExecHost(self):
        pass
    
    def modifyResourceQuotaSet(self):
        pass
    
    def cleanQueue(self):
        pass
    
    def clearUsage(self):
        pass
    
    def deleteAdminHost(self, oi):
        pass
           
    def deleteAttribute(self, oi):
        pass
           
    def deleteManager(self, oi):
        pass
           
    def deleteOperator(self, oi):
        pass

    def deleteShareTree(self, oi):
        pass
           
    def deleteSubmitHost(self, oi):
        pass
           
    def deleteUserSet(self, oi):
        pass
           
    def deleteUserSetList(self, oi):
        pass

    def showClusterQueue(self, oi):
        pass
           
    def showComplexEntry(self, oi):
        pass
           
    def showConfiguration(self, oi):
        pass
           
    def showDetachedSettings(self, oi):
        pass
           
    def showEventClientList(self, oi):
        pass
           
    def showHostgroupResolved(self, oi):
        pass
           
    def showHostgroupTree(self, oi):
        pass
           
    def showParallelEnvironment(self, oi):
        pass
           
    def showProcessors(self, oi):
        pass
           
    def showProject(self, oi):
        pass
           
    def showResourceQuotaSet(self, oi):
        """Implements qconf -srqs option"""
        pass
          
    def showSchedulerState(self, oi):
        pass
           
    def showShareTree(self, oi):
        pass
           
    def triggerSchedulerMonitoring(self, oi):
        pass


class QModCommand(AbstractCommand):
    """Wrapper class for qmod command line"""
    def __init__(self, arg):
        super(QModCommand, self).__init__()
        self.arg = arg
        
    def parseJobList(self, arg):
        pass
           
    def parseJobWCQueueList(self, arg):
        pass
           
    def parseWCQueueList(self, arg):
        pass


class QHostCommand(AbstractCommand):
    """Wrapper command for qgost command line program"""
    def __init__(self, **args):
        super(QHostCommand, self).__init__()
        self.args = args

    def function(self):
        pass


class QStatJob(dict):
    '''data structure to hold SGE job information'''
    def __str__(self):
        return ''.join(['{}: {}\n'.format(x, y) for x, y in self.items()])
    

class QStatCommand(AbstractCommand):

    def __init__(self, *args):
        super(QStatCommand, self).__init__()
        self.command = 'qstat'
        self.args = ['-r', '-xml']
        self.args += args

        self._stack = Stack()
        self._jobs = []
        self._curr_job = DefaultDict(None)

    def start_element(self, name, attrs):
        self._stack.push((name, attrs))
        
    def end_element(self, name):
        if name == 'job_list':
            self._jobs.append(QStatJob(self._curr_job))
            self._curr_job.clear()
        self._stack.pop()

    def char_data(self, data):
        tag, attr = self._stack.getLast()
        if tag == 'job_list':
            self._curr_job['state'] = attr['state']
        if tag == 'state':
            self._curr_job['flags'] = data
        if tag == 'JB_job_number':
            self._curr_job['jobnumber'] = data
        if tag == 'JB_name':
            self._curr_job['name'] = data
        if tag == 'JB_owner':
            self._curr_job['owner'] = data
        if tag == 'tasks':
            self._curr_job['tasks'] = data
        if tag == 'hard_request':
            if 'hard_request' not in self._curr_job:
                self._curr_job['hard_request'] = {}
            self._curr_job['hard_request'][attr['name']] = data
        if tag == 'hard_request':
            if 'hard_request' not in self._curr_job:
                self._curr_job['hard_request'] = {}
            self._curr_job['hard_request'][attr['name']] = data

    def listJobs(self, args=[], **kwargs):
        cmd_args = self.args
        for a in args:
            cmd_args.append(a)
        self.run(cmd_args)

        p = xml.parsers.expat.ParserCreate()
        p.StartElementHandler = self.start_element
        p.EndElementHandler = self.end_element
        p.CharacterDataHandler = self.char_data

        p.Parse(self.out)

        return self._jobs

    def function(self):
        pass


from subprocess import Popen, PIPE
import sys
import os
import logging
import re
import xml.parsers.expat
import xml.etree.ElementTree as ET
from copy import copy, deepcopy

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
        self.args = []

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


def qstatus(stat_id):

    return stat_id


def str_to_digit(text):

    if text.isdigit():
        if re.match(r'^\d+\.\d+$', text):
            return  float(text)
        else:
            return int(text)

    return text


class QXmlStackManager(object):

    def __init__(self, object_name, out_object):

        self.attr_map = {}

        self._stack = Stack()
        self._object_name = object_name
        self._out_object = out_object
        self._out_list = []

        # self._parser = xml.parsers.expat.ParserCreate()

        # self._parser.StartElementHandler = self.start_element
        # self._parser.EndElementHandler = self.end_element
        # self._parser.CharacterDataHandler = self.char_data

        self.__current_obj = DefaultDict(None)

    def parse(self, data):
        self._out_list = []
        root = ET.fromstring(data)
        # self._parser.Parse(data)

        # root = tree.getroot()
        e_list = []
        for e in root.iter(self._object_name):
            e_list.append(e)

            _o_list = self.populate_data(e, self.attr_map)
            for o in _o_list:
                sj = self._out_object(o)
                self._out_list.append(sj)

        return self._out_list

    def populate_data(self, element, attr_map):

        __current_obj = DefaultDict(None)
        _out_list = []
        for e in element.iter():

            tag = e.tag
            attr = e.attrib
            data = e.text

            if tag in attr_map:
                tag_map = attr_map[tag]
                d_name = tag_map.get('name')
                if 'name_attr' in tag_map:
                    name_attr = tag_map['name_attr']
                    if name_attr in attr:
                        d_name = attr[name_attr]
                d_type = tag_map.get('type')
                if d_name in __current_obj and d_type is not 'raw_list':
                    _out_list.append(__current_obj.copy())
                    __current_obj.clear()
                if d_name and tag_map.get('use_data', True):
                    if d_type not in [list, 'raw', 'raw_list']:
                        __current_obj[d_name] = d_type(data)
                    elif d_type is list:
                        if d_name not in __current_obj:
                            __current_obj[d_name] = []
                    elif d_type is 'raw':
                        __current_obj[d_name] = {}
                        for c in e.iter():
                            if c.tag in tag_map.get('children', {}):
                                c_dict = tag_map['children'][c.tag]
                                c_name = c_dict['name']
                                if 'name' in c.attrib:
                                    c_name = c.attrib['name']
                                c_type = c_dict.get('type', str)
                                __current_obj[d_name][c_name] = c_type(c.text)
                    elif d_type is 'raw_list':
                        if not __current_obj[d_name]:
                            __current_obj[d_name] = []
                        result = self.populate_data(e, tag_map.get('children', {}))
                        if len(result):
                            __current_obj[d_name] += result

                if 'attrs' in tag_map:
                    d_attrs = tag_map['attrs']
                    for a, d in d_attrs.items():
                        if a in attr:
                            a_name = d.get('name')
                            a_type = d.get('type')
                        __current_obj[a_name] = a_type(attr[a])
        _out_list.append(__current_obj.copy())

        return _out_list


class QStatJob(dict):
    '''data structure to hold SGE job information'''
    def __str__(self):
        return ''.join(['{}: {}\n'.format(x, y) for x, y in self.items()])


class QStatJobInfo(dict):

    def __str__(self):
        return ''.join(['{}: {}\n'.format(x, y) for x, y in self.items()])
    

class QStatCommand(AbstractCommand):

    def __init__(self, *args):
        super(QStatCommand, self).__init__()
        self.command = 'qstat'
        self.args = ['-r', '-xml']
        self.args += args

        self._job_stack = QXmlStackManager('job_list', QStatJob)
        self._job_stack.attr_map = {'job_list': {'attrs': {'state': {'name': 'state', 'type': str}}},
                                    'state': {'name': 'flags', 'type': str},
                                    'JB_job_number': {'name': 'jobid', 'type': int},
                                    'JB_name': {'name': 'name', 'type': str},
                                    'JB_owner': {'name': 'owner', 'type': str},

                                    'JB_submission_time': {'name': 'submission_time', 'type': str},
                                    'JAT_start_time': {'name': 'start_time', 'type': str},
                                    'tasks': {'name': 'tasks', 'type': str},
                                    'queue_name': {'name': 'running_queue', 'type': str},
                                    'hard_req_queue': {'name': 'requested_queue', 'type': str},
                                    'ad_predecessor_jobs_req': {'name': 'dependencies', 'type': list}
                                    }
        self._job_info_stack = QXmlStackManager('djob_info', QStatJobInfo)
        self._job_info_stack.attr_map = {'JB_merge_stderr': {'name': 'merge_err', 'type': bool},
                                         'JB_job_number': {'name': 'jobid', 'type': int},
                                         'JB_script_file': {'name': 'script_file', 'type': str},
                                         'JB_job_name': {'name': 'name', 'type': str},
                                         'JB_owner': {'name': 'owner', 'type': str},
                                         'JB_cwd': {'name': 'cwd', 'type': str},
                                         'JB_pe': {'name': 'pe', 'type': str},
                                         'JB_pe_range': {'name': 'pe_range', 'type': 'raw',
                                                         'children': {'RN_min': {'name': 'min', 'type': int},
                                                                      'RN_max': {'name': 'max', 'type': int},
                                                                      'RN_step': {'name': 'step', 'type': int}}},
                                         'task_id_range': {'name': 'task_range', 'type': 'raw',
                                                         'children': {'RN_min': {'name': 'min', 'type': int},
                                                                      'RN_max': {'name': 'max', 'type': int},
                                                                      'RN_step': {'name': 'step', 'type': int}}},
                                         'JB_stdout_path_list': {'name': 'out_log_paths', 'type': 'raw_list',
                                                         'children': {'PN_path': {'name': 'path', 'type': str}}},
                                         'JB_stderr_path_list': {'name': 'err_log_paths', 'type': 'raw_list',
                                                         'children': {'PN_path': {'name': 'path', 'type': str}}},
                                         'JB_shell_list': {'name': 'shell', 'type': 'raw_list',
                                                         'children': {'PN_path': {'name': 'path', 'type': str}}},
                                         # 'JB_env_list': {'name': 'envs', 'type': 'raw_list',
                                         #                 'children': {'VA_variable': {'name': 'key', 'type': str},
                                         #                              'VA_value': {'name': 'value', 'type': str}}},
                                         'JB_jid_predecessor_list': {'name': 'predecessors', 'type': 'raw_list',
                                                         'children': {'JRE_job_number': {'name': 'id', 'type': int}}},
                                         'JB_jid_successor_list': {'name': 'successors', 'type': 'raw_list',
                                                         'children': {'JRE_job_number': {'name': 'id', 'type': int}}},
                                         'JB_hard_queue_list': {'name': 'requested_queues', 'type': 'raw_list',
                                                         'children': {'QR_name': {'name': 'name', 'type': str}}},
                                         'JB_ja_tasks': {'name': 'array_tasks', 'type': 'raw_list',
                                                         'children': {'JAT_status': {'name': 'status', 'type': int},
                                                                      'JAT_task_number': {'name': 'task_id', 'type': int},
                                                                      'JAT_scaled_usage_list': {'name': 'usage', 'type': 'raw_list',
                                                                            'children': {'UA_name': {'name': 'name', 'type': str},
                                                                                         'UA_value': {'name': 'value', 'type': float}}}
                                                         }}
                                        }

    def listJobs(self, args=[], **kwargs):
        cmd_args = copy(self.args)
        for a in args:
            cmd_args.append(a)
        self.run(cmd_args)

        return self._job_stack.parse(self.out)

    def getJobInfo(self, jobid):
        cmd_args = copy(self.args)
        cmd_args += ['-j', str(jobid)]
        self.run(cmd_args)

        # sanitise the xml so no tags have spaces
        # tags_spaces = re.findall(r'<([\[a-zA-Z0-9+\s]*)>', '<mail list>')
        out = self.out.replace('mail list', 'mail_list')
        out = out.replace('<>', '<empty>')
        out = out.replace('</>', '</empty>')

        return self._job_info_stack.parse(out)


class QHostInfo(dict):
    '''data structure to hold SGE job information'''
    def __str__(self):
        return ''.join(['{}: {}\n'.format(x, y) for x, y in self.items()])


class QHostCommand(AbstractCommand):
    """Wrapper command for qgost command line program"""
    def __init__(self, *args):
        super(QHostCommand, self).__init__()
        self.command = 'qhost'
        self.args = ['-xml']
        self.args += args

        self._host_stack = QXmlStackManager('host', QHostInfo)
        self._host_stack.attr_map = {'host': {'attrs': {'name': {'name': 'hostname', 'type': str}}},
                                     'hostvalue': {'name': 'hostvalue', 'name_attr': 'name', 'type': str_to_digit},
                                     'job': {'name': 'jobs', 'type': 'raw_list',
                                             'children': {'jobvalue': {'name': 'jobvalue', 'name_attr': 'name', 'type': str_to_digit, 
                                                                              'attrs': {'jobid': {'name': 'jobid', 'type': int}}
                                                                              }}}
                                    }

    def listHosts(self, show_jobs=False):
        cmd_args = copy(self.args)
        cmd_args.append('-cb')

        if show_jobs:
            cmd_args.append('-j')

        self.run(cmd_args)

        return self._host_stack.parse(self.out)

    def getHostInfo(self, hostname, show_jobs=False):
        cmd_args = copy(self.args)
        cmd_args.append('-cb')
        cmd_args += ['-h', hostname]
        if show_jobs:
            cmd_args.append('-j')

        self.run(cmd_args)

        return self._host_stack.parse(self.out)


class QModCommand(AbstractCommand):
    """Wrapper class for qmod command line"""
    def __init__(self, *args):
        super(QModCommand, self).__init__()
        self.command = 'qmod'
        self.args += args

    def __run_args(self, o_list, arg, force=False):
        cmd_args = copy(self.args)
        if force:
            cmd_args.append('-f')
        cmd_args.append(arg)
        cmd_args += o_list

        self.run(cmd_args)

        return self.out

    def clear_error(self, o_list, force=False):
        return self.__run_args(o_list, '-c', force)

    def reschedule(self, o_list, force=False):
        return self.__run_args(o_list, '-r', force)

    def suspend(self, o_list, force=False):
        return self.__run_args(o_list, '-s', force)

    def unsuspend(self, o_list, force=False):
        return self.__run_args(o_list, '-us', force)

    def disable_queue(self, queue_list, force=False):
        if not isinstance(queue_list, list):
            queue_list = [queue_list]

        return self.__run_args(queue_list, '-d', force)

    def enable_queue(self, queue_list, force=False):
        if not isinstance(queue_list, list):
            queue_list = [queue_list]

        return self.__run_args(queue_list, '-e', force)


class QDelCommand(AbstractCommand):
    """Wrapper class for qdel command line"""
    def __init__(self, *args):
        super(QDelCommand, self).__init__()
        self.command = 'qdel'
        self.args += args

    def __run_args(self, o_list, arg='', force=False):
        cmd_args = copy(self.args)
        if force:
            cmd_args.append('-f')
        if arg:
            cmd_args.append(arg)
        cmd_args += o_list

        self.run(cmd_args)

        return self.out

    def delete_user_jobs(self, username, force=False):
        return self.__run_args([username], '-u', force=force)

    def delete_jobs(self, jobids, force=False):
        return self.__run_args([str(j) for j in jobids], force=force)


class QAcctCommand(AbstractCommand):
    """Wrapper class for qdel command line"""
    def __init__(self, *args):
        super(QDelCommand, self).__init__()
        self.command = 'qacct'
        self.args += args

    def __run_args(self, o_list, arg=''):
        cmd_args = copy(self.args)
        if arg:
            cmd_args.append(arg)
        cmd_args += o_list

        self.run(cmd_args)

        return self.out

    def get_finished_tasks(self, jobid):
        return self.__run_args(str(jobid), '-j')

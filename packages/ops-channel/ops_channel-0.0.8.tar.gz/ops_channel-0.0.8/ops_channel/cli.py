#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'xiaozhang'

import atexit
from signal import SIGTERM
import signal
import sys
import os
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
import urllib
if PY2:
    import urllib2 as urllib2
    import httplib
    from urlparse import urlparse
    import Queue as queue
    reload(sys)
    sys.setdefaultencoding('utf-8')

if PY3:
    import urllib.request as urllib2
    import queue as queue
    from urllib.parse import urlparse
    urllib.urlencode=urllib.parse.urlencode
    import http.client as httplib





import subprocess
import time
import datetime
import re
import logging
import hashlib
import base64

import tempfile
import threading
import getopt
from logging.handlers import RotatingFileHandler
import json
import random
import platform
import socket

import uuid
import inspect
import getpass



pidfile="/var/cli.pid"
server_url='server_url'
server_url="http://127.0.0.1:8005" #server_url
CLI_GROUP='cli_group'
CLI_GROUP='default' #

configfile='/etc/cli'
default_module='cli'
bin_name='cli'
client_filename='/bin/%s' % bin_name
script_path= tempfile.gettempdir()+ os.path.sep+'script'
global_debug=False

PLATFORM=platform.system().lower()
PYTHON_PATH='/usr/bin/python'
CLI_VERSION='2.0.20171120'






def init_log():
    dirs=['/tmp/','/var/','/etc/','/bin/','/var/log/']
    for d in dirs:
        if not os.path.exists(d):
            os.mkdir(d)
    user=getpass.getuser()
    client_log_filename='/var/log/cli.log'
    try:
        if PLATFORM!='windows':
            _p=os.popen('which python').read().strip()
            if _p!='' and len(_p)>0:
                PYTHON_PATH=_p
    except Exception as er:
        pass

    log_dir= os.path.dirname(client_log_filename)
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    # if user=='root':
    #     os.chmod(log_dir,0666)
    log_fmt_str='%(asctime)-25s %(module)s:%(lineno)d  %(levelname)-8s %(message)s'
    if PY2:
        logging.basicConfig(level=logging.DEBUG,
                format=log_fmt_str,
                filemode='a+')
    if PY3:
        log_fmt_str='%(asctime)s %(module)s:%(lineno)d  %(levelname)s %(message)s'
        logging.basicConfig(level=logging.DEBUG,
                format=log_fmt_str)
    logger = logging.getLogger('CLI')
    file_handler=RotatingFileHandler(filename=client_log_filename,maxBytes=100 * 1024 * 1024, backupCount=3)
    formatter= logging.Formatter(log_fmt_str)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter )
    logger.addHandler(file_handler)
    if user=='root' and PLATFORM!='windows':
        try:
            if len(os.popen('command -v chattr').read())>1:
                os.popen('chattr -a %s'%(client_log_filename)).read()
                os.chmod(client_log_filename,766)
                # os.popen('chattr +a %s'%(client_log_filename)).read()
        except Exception as er:
            pass
    try:
        os.chmod(client_log_filename, 766)
    except Exception as er:
        pass
    return logger

logger=init_log()





class LongHttp(object):

    Connections={}

    def __init__(self):
        pass
    @staticmethod
    def digest(url):
        import hashlib
        md5 = hashlib.md5()
        if PY2:
            md5.update(url.encode('utf-8'))
        if PY3:
            md5.update(url.encode('utf-8'))
        return md5.hexdigest()

    @staticmethod
    def request(url,data={},method='GET',headers={},timeout=30):
        # ParseResult(scheme='http', netloc='www.baidu.com', path='/index.html', params='', query='', fragment='')
        url_info = urlparse(url)
        tid = str(threading.current_thread().ident)
        md5 = 'thread_%s_' % (tid) + LongHttp.digest(url_info[1])
        def get_connetion(url):
            if md5 in LongHttp.Connections:
                conn = LongHttp.Connections[md5]
                return conn
            else:
                url_info=urlparse(url)
                host=url_info[1]
                conn=httplib.HTTPConnection(host=host,timeout=timeout)
                LongHttp.Connections[md5]=conn
                return conn

        conn=get_connetion(url)
        params=urllib.urlencode(data)
        headers['Connection']='keep-alive'
        # headers['Connection']='close'
        try:
            conn.request(method,url_info[2]+'?'+url_info[4],body=params,headers=headers)
            response= conn.getresponse()
            return response.read()
        except Exception as er:
            del LongHttp.Connections[md5]
            print(er)

# class CertificateError(ValueError):
#     pass
# try:
#     import ssl
# except ImportError:
#     ssl = None
#     import warnings
#     msg = ("Can't import ssl. HTTPS won't work."
#            "Run `pip install ssl` if Python < 2.6")
#     try:
#         ImportWarning
#     except NameError:
#         warnings.warn(msg)
#     else:
#         warnings.warn(msg, ImportWarning)
# else:
#     try:
#         from http import client
#     except ImportError:
#         import httplib as client
#     import re
#     try:
#         import urllib2 as request
#     except ImportError:
#         from urllib import request
#     class HTTPSConnection(client.HTTPSConnection):
#         def __init__(self, host, **kwargs):
#             self.ca_certs = kwargs.pop('ca_certs', None)
#             self.checker = kwargs.pop('checker', None)
#             self.timeout = kwargs.get('timeout', socket.getdefaulttimeout())
#             client.HTTPSConnection.__init__(self, host, **kwargs)
#
#
#         def connect(self):
#             try:
#                 args = [(self.host, self.port), self.timeout,]
#                 if hasattr(self, 'source_address'):
#                     args.append(self.source_address)
#                 sock = socket.create_connection(*args)
#                 if getattr(self, '_tunnel_host', None):
#                     self.sock = sock
#                     self._tunnel()
#                 kwargs = {}
#                 if self.ca_certs is not None:
#                     kwargs.update(
#                         cert_reqs=ssl.CERT_REQUIRED,
#                         ca_certs=self.ca_certs)
#                 self.sock = ssl.wrap_socket(sock,
#                                             keyfile=self.key_file,
#                                             certfile=self.cert_file,
#                                             **kwargs)
#             except Exception as er:
#                 logger.error(er)
#             if self.checker is not None:
#                 try:
#                     self.checker(self.sock.getpeercert(), self.host)
#                 except CertificateError:
#                     self.sock.shutdown(socket.SHUT_RDWR)
#                     self.sock.close()
#                 except Exception as er:
#                     print(er)
#                     logger.error(er)
#                     pass
#     class HTTPSHandler(request.HTTPSHandler):
#         def __init__(self, key_file=None, cert_file=None, ca_certs=None,
#                      checker=None):
#             request.HTTPSHandler.__init__(self)
#             self.key_file = key_file
#             self.cert_file = cert_file
#             self.ca_certs = ca_certs
#             self.checker = self.match_hostname
#         def _dnsname_to_pat(self,dn):
#             pats = []
#             for frag in dn.split(r'.'):
#                 if frag == '*':
#                     pats.append('[^.]+')
#                 else:
#                     frag = re.escape(frag)
#                     pats.append(frag.replace(r'\*', '[^.]*'))
#             return re.compile(r'\A' + r'\.'.join(pats) + r'\Z', re.IGNORECASE)
#         def match_hostname(self,cert, hostname):
#             return
#             if not cert:
#                 raise ValueError("empty or no certificate")
#             dnsnames = []
#             san = cert.get('subjectAltName', ())
#             for key, value in san:
#                 if key == 'DNS':
#                     if self._dnsname_to_pat(value).match(hostname):
#                         return
#                     dnsnames.append(value)
#             if not dnsnames:
#                 for sub in cert.get('subject', ()):
#                     for key, value in sub:
#                         if key == 'commonName':
#                             if self._dnsname_to_pat(value).match(hostname):
#                                 return
#                             dnsnames.append(value)
#
#             if len(dnsnames) > 1:
#                 raise CertificateError("hostname %r "
#                     "doesn't match either of %s"
#                     % (hostname, ', '.join(map(repr, dnsnames))))
#             elif len(dnsnames) == 1:
#                 raise CertificateError("hostname %r "
#                     "doesn't match %r"
#                     % (hostname, dnsnames[0]))
#             else:
#                 raise CertificateError("no appropriate commonName or "
#                     "subjectAltName fields were found")
#         def https_open(self, req):
#             return self.do_open(self.getConnection, req)
#         def getConnection(self, host, **kwargs):
#             d = dict(cert_file=self.cert_file,
#                      key_file=self.key_file,
#                      ca_certs=self.ca_certs,
#                      checker=self.checker)
#             d.update(kwargs)
#             return HTTPSConnection(host, **d)

class Daemon(object):
        def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
                self.stdin = stdin
                self.stdout = stdout
                self.stderr = stderr
                self.pidfile = pidfile
                self.salt=''
                self.pid=''
                self.shellstr=''

        def daemonize(self):
                try:
                        pid = os.fork()
                        if pid > 0:
                                # exit first parent
                                sys.exit(0)
                except OSError as  e:
                        sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
                        sys.exit(1)
                os.chdir("/")
                os.setsid()
                os.umask(0o022)

                # do second fork
                try:
                        pid = os.fork()
                        if pid > 0:
                                # exit from second parent
                                sys.exit(0)
                except OSError as  e:
                        sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
                        sys.exit(1)

                # redirect standard file descriptors
                sys.stdout.flush()
                sys.stderr.flush()
                si = open(self.stdin, 'r')
                so = open(self.stdout, 'a+')
                se = open(self.stderr, 'a+')
                os.dup2(si.fileno(), sys.stdin.fileno())
                os.dup2(so.fileno(), sys.stdout.fileno())
                os.dup2(se.fileno(), sys.stderr.fileno())

                # write pidfile
                atexit.register(self.delpid)
                pid = str(os.getpid())
                self.pid=pid
                open(self.pidfile,'w+').write("%s\n" % pid)

        def delpid(self):
                os.remove(self.pidfile)

        def _start(self):
                try:
                        pf = open(self.pidfile,'r')
                        pid = int(pf.read().strip())
                        pf.close()
                except Exception as er:
                        pid = None
                if pid:
                        message = "pidfile %s already exist. Daemon already running?\n"
                        sys.stderr.write(message % self.pidfile)
                        sys.exit(1)
                self.daemonize()
                self.run()
        def start(self):
            self.restart()

        def kill(self):
            try:
                self.daemonize()
                kill='''
                  ps aux|grep -v grep|grep -v -w '%s'|grep python|grep -w 'cli daemon'|awk '{print $2}'|xargs -n 1 kill -9
                  ''' % (self.pid)
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
                ZbxCommand(kill,is_log=False).run()
            except Exception as er:
                pass

        def status(self):
            try:
                shell_status='''
                  ps aux|grep -v grep|grep python|grep -w 'cli daemon'|awk '{print $2}'
                  '''
                _pid=ZbxCommand(shell_status,is_log=False).run()
                try:
                    pid=re.split(r'\n|\r',_pid.strip())
                    if len(pid)>1:
                        print('cli is running')
                    else:
                        print('cli is not running')
                except Exception as e:
                    pass
            except Exception as er:
                pass

        def stop(self):
                try:
                        pf = open(self.pidfile,'r')
                        pid = int(pf.read().strip())
                        pf.close()
                except Exception as er:
                        pid = None
                self.kill()
                if not pid:
                        message = "pidfile %s does not exist. Daemon not running?\n"
                        sys.stderr.write(message % self.pidfile)
                        return # not an error in a restart

                # Try killing the daemon process
                try:
                        while 1:
                                os.kill(pid, SIGTERM)
                                time.sleep(0.1)
                except OSError as  err:
                        err = str(err)
                        if err.find("No such process") > 0:
                                if os.path.exists(self.pidfile):
                                        os.remove(self.pidfile)
                        else:
                                print(str(err))
                                sys.exit(1)
        def restart(self):
                self.stop()
                self._start()


class ZbxCommand(object):
    def __init__(self, cmd,is_log='0'):
        mc=re.match('^su\s+[\'"a-zA-z09]+?\s+\-c',cmd)
        if PLATFORM=='windows' and mc!=None:
            cmd=cmd.replace(mc.group(0),'')
            cmd=cmd.strip()
            cmd=re.sub('^\"|\"$','',cmd)
        self.cmd = cmd
        self.process = None
        self.is_log=is_log
        self.return_code=-1
        self.util=ZbxCommon()
        self.messge_success=''
        self.message_error=''
        self.uuid=str(datetime.datetime.now()).replace(' ','').replace(':','').replace('-','').replace('.','')
        self.uuid_error=self.uuid+'error'
        self.result=open(tempfile.gettempdir()+ os.path.sep +self.uuid,'a+')
        self.result_error=open(tempfile.gettempdir()+ os.path.sep +self.uuid_error,'a+')


    def run(self, timeout=30,task_id='', url_success='',url_error='',url='',ip=''):
        def feedback(url,result,task_id,return_code=0,ip=''):
            try:
                machine_id=self.util.get_product_uuid()
                if ip=='':
                    ip=self.util.get_one_ip()
                data=self.util.url_fetch_witherr(url,{ 'cmd':self.cmd,'machine_id':machine_id,'result':result,'task_id':task_id,
                'success':self.messge_success,'error':self.message_error,'return_code':return_code,'ip':machine_id,'s':self.util.get_hostname(),'i':ip},timeout=8)
                if PY2:
                    if isinstance(data,str):
                        logger.info('feedback result:%s'+ str(data))
                    if isinstance(data,unicode):
                        logger.info('feedback result:%s' + str(data.encode('utf-8','ignore')))
                if PY3:
                    if isinstance(data,str):
                        logger.info('feedback result:%s'+ str(data))
            except Exception as er:
                data={'task_id':task_id,'result':result,'url':url}
                logger.error('feedback error:\t'+str(er)+json.dumps(data))


        def target():
            if self.is_log=='1':
                logger.info("task_id:%s"%(task_id)+"\t"+str(self.cmd))
            elif self.is_log=='2':
                logger.info("task_id:%s" % (task_id) + "\t cmd:mask")

            self.process = subprocess.Popen(self.cmd, shell=True,stdout=self.result,stderr=self.result_error)
            self.process.communicate()
            self.process.poll()
            self.return_code = self.process.returncode
            if self.return_code==None:
                self.return_code=-1
        thread = threading.Thread(target=target)
        thread.start()
        if timeout==-1:
            thread.join()
        thread.join(timeout)


        def get_result():
            result=''
            error=''
            try:
                result= open(tempfile.gettempdir()+ os.path.sep+self.uuid,'r').read()
                if self.is_log=='1':
                    logger.info("task_id:%s\tSuccess Result:" %(task_id) + str(result))
                elif self.is_log=='2':
                    logger.info("task_id:%s\tSuccess Result:mask" % (task_id))
                elif self.is_log=='3':
                    logger.info("task_id:%s\tSuccess Result:" % (task_id) + str(result))
            except Exception as er:
                print(self.cmd)
                print('get_result:\t'+str(er))
                logger.error(er)
            finally:
                try:
                    self.result.close()
                    os.unlink(tempfile.gettempdir()+ os.path.sep+self.uuid)
                except Exception as er:
                    print('get_result:\t' + str(er))
                    logger.error(er)
                    pass
            try:
                error = open(tempfile.gettempdir() + os.path.sep + self.uuid_error, 'r').read()
            except Exception as err:
                logger.error(er)
                print(err)
                if self.is_log == '1' or self.is_log == '2' or self.is_log == '3':
                    logger.error("task_id:%s\tException Result:" % (task_id) + str(error))
            finally:
                try:
                    self.result_error.close()
                    os.unlink(tempfile.gettempdir() + os.path.sep + self.uuid_error)
                except Exception as er:
                    print('get_result close :\t' + str(er))
                    logger.error(er)

            try:
                if PLATFORM == 'windows':
                    result = result.decode('gbk').encode('utf-8', 'ignore')
                    error = error.decode('gbk').encode('utf-8','ignore')
            except Exception as er:
                pass
            return result.strip(),error.strip()
        if thread.is_alive():
            logger.warn(self.cmd)
            result, error = get_result()
            if url != '':
                feedback(url, result, task_id, self.return_code,ip)
            if url_error!='':
                feedback(url_error, "(error)timeout\n%s"%(str(result)+str(error)), task_id, -1,ip)
                if self.is_log == '1' or self.is_log == '2' or self.is_log == '3':
                    logger.info("task_id:%s\ttimeout result has feedback to url:%s result:%s error:%s" % (task_id,url_error,result,error))
            else:
                logger.info('timeout task_id:%s' % (task_id))
            self.process.terminate()
            thread.join()
            if result!='':
                return "(error)timeout \nresult:%s error:%s" % (str(result), str(error))
                #return result
            return "(error)timeout \nresult:%s error:%s" % (str(result), str(error))
            #util.url_fetch(server_url+'/slowlog',{'param':{ 'cmd':self.cmd,'ip':util.get_one_ip()}})
        result,error= get_result()
        try:
            if re.findall(r'\(error\)\s+file\s+not\s+found', result):
                self.return_code=127
        except Exception as er:
            pass

        self.messge_success=result
        self.message_error=error

        if result=='' and error!='':
            result='finish'
        if url!='':
            feedback(url, result, task_id, self.return_code,ip)
            if self.is_log=='1' or self.is_log=='2' or self.is_log=='3':
                logger.info("task_id:%s\t result has feedback to url:%s "%(task_id,url))
        if  self.return_code==0 and url_success!='':
            feedback(url_success,result,task_id,self.return_code,ip)
            if self.is_log=='1' or self.is_log=='2' or self.is_log=='3':
                logger.info("task_id:%s\tsuccess result has feedback to url:%s "%(task_id,url_success))
        if self.return_code!=0 and url_error!='':
            feedback(url_error,result,task_id,self.return_code,ip)
            if self.is_log=='1' or self.is_log=='2' or self.is_log=='3':
                logger.info("task_id:%s\terror result has feedback to url:%s " % (task_id,url_error))
        if error.strip()!='':
            return result+"\n"+error
        else:
            return result



class ZbxDaemonWin(object):

    def __init__(self,daemon=None):
        bflag=False
        self.daemon=daemon

    def action(self,action='daemon'):
        try:
            import win32serviceutil
            import win32event
            import win32service
        except Exception as er:
            print('please instll pywin32,  pip install pywin32')
            ZbxCommand('pip install pywin32').run(timeout=600)
            sys.exit(0)
        class Daemon(win32serviceutil.ServiceFramework):
            _svc_name_ = "Cli Service"
            _svc_display_name_ = "Cli Service"
            def __init__(self,args,daemon=None):
                # win32serviceutil.ServiceFramework.__init__(self, args)
                self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
                self.daemon=daemon

            def SvcStop(self):
                self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
                win32event.SetEvent(self.hWaitStop)

            def SvcDoRun(self):
                self.daemon.run()
                win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)

        action=''
        daemon = Daemon({},daemon=self.daemon)
        for i in ['start','install']:
            if sys.argv.count(i)>0:
                sys.argv.remove(i)
                action=i
                break
        # print(action)
        sys.argv.remove('-s')
        sys.argv.remove('daemon')
        if action=='start':
            sys.argv.append('install')
            win32serviceutil.HandleCommandLine(Daemon)
            sys.argv.remove('install')
        sys.argv.append(action)
        win32serviceutil.HandleCommandLine(Daemon)





class ZbxCommon(object):
    def __init__(self):
        self.machine_id=''
        self.config={}

    def urlencode(self,str):
        reprStr=repr(str).replace(r'\x','%')
        return reprStr[1:-1]

    def get_basic_auth(self,user='',pwd=''):
        s=user.strip()+':'+pwd.strip()
        if PY2:
            return 'Basic '+ base64.encodestring(s).strip()
        if PY3:
            return 'Basic ' + str(base64.encodestring(s.encode('utf-8')),'utf-8').strip()

    def download(self,filename,directory,filepath):
        try:
            data={'file':filename,'dir':directory}
            data=urllib.urlencode(data)
            if filename.startswith('http://') or filename.startswith('https://'):
                http_url=filename
                if http_url.endswith('/'):
                    http_url=http_url[0:len(http_url)-1]
                if http_url.rindex('/')>0 and http_url.rindex('/')<len(http_url):
                    filename=http_url[http_url.rindex('/')+1:]
                filename=filename.replace('?','')
                filepath=filename
            else:
                http_url = '%s/%s/download?%s' % (server_url, default_module, data)
            def _download(url,data,filepath):
                #logger.info('download file url:%s'%(str(url)))
                request = urllib2.Request(url)
                request.add_header('User-Agent', 'CLI(1.0)')
                if filename.startswith('http://') or filename.startswith('https://'):
                    request.add_header('auth-uuid', self._get_config('auth-uuid'))
                conn = urllib2.urlopen(request)
                f = open(filepath,'wb')
                f.write(conn.read())
                f.close()
            _download(http_url,data,filepath)
            try:
                line=''
                with open(filepath, 'r') as _file:
                    if PY3:
                        try:
                            _file.readline().encode()
                        except Exception as er:
                            pass
                    else:
                        line=str(_file.readline()).strip()
                if line.startswith('redirect:http://') or line.startswith('redirect:https://'):
                    _download(line,data,filepath)
            except Exception as er:
                print('(error) %s' % (str(er)))
                logger.error(er)
        except Exception as e:
            logger.error(e)
            print('(error) %s'%(str(e)))

    def upload(self,url,filepath,directory):
        boundary = '----------%s' % hex(int(time.time() * 1000))
        data = []
        data.append('--%s' % boundary)
        fr=open(filepath,'rb')
        filename=os.path.basename(filepath)
        data.append('Content-Disposition: form-data; name="%s"\r\n' % 'filename')
        data.append(filename)
        data.append('--%s' % boundary)
        data.append('Content-Disposition: form-data; name="%s"\r\n' % 'dir')
        data.append(directory)
        data.append('--%s' % boundary)
        data.append('Content-Disposition: form-data; name="%s"; filename="%s"' % ('file',filename))
        data.append('Content-Type: %s\r\n' % 'image/png')

        if PY3:
            http_body = "\r\n".join(data)+'\r\n'
            from io import BytesIO, StringIO
            f = BytesIO()
            f.write(http_body.encode(encoding="utf-8"))
            f.write(fr.read())
            f.write(('\r\n--%s--\r\n' % boundary).encode(encoding="utf-8"))
        else:
            data.append(fr.read())
            data.append('--%s--\r\n' % boundary)
            http_body = '\r\n'.join(data)
        fr.close()


        try:
            if PY3:
                req=urllib2.Request(url, data=f.getvalue())
            else:
                req = urllib2.Request(url, data=http_body)
            req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)
            req.add_header('User-Agent','Mozilla/5.0')
            req.add_header('Referer','http://remotserver.com/')
            req.add_header('auth-uuid',self._get_config('auth-uuid'))
            resp = urllib2.urlopen(req, timeout=5)
            qrcont=resp.read()
            print(qrcont.decode())
        except Exception as e:
            logger.error(e)
            print('(error)%s'%(str(e)))


    def url_fetch_witherr(self,url,data=None,header={},timeout=30,httpCmd=''):
        return self._url_fetch(url,data=data,header=header,timeout=timeout,httpCmd=httpCmd)

    def url_fetch(self,url,data=None,header={},timeout=30,httpCmd='',debug=False):
        try:
            return self._url_fetch(url,data=data,header=header,timeout=timeout,httpCmd=httpCmd,debug=debug)
        except Exception as er:
            #logger.error('url_fetch error:%s'+str(er))
            print(er)
            return ''

    def _get_config(self,key):
        home= os.path.expanduser('~')
        fn=home+'/.cli'
        content=''
        data={}
        try:
            if os.path.isfile(fn):
                with open(fn) as f:
                    content=f.read()
                    content=str(content).strip()
                lines=re.split(r'\n',content)
                for line in lines:
                    line=line.strip()
                    pos=line.find('=')
                    if pos>0:
                        data[line[0:pos]]=line[pos+1:]
                if len(data)>0:
                    self.config=data
        except Exception as er:
            logger.error(er)
        if key in self.config.keys():
            return self.config[key]
        else:
            return ''

    def _set_config(self,key,value):
        home= os.path.expanduser('~')
        fn=home+'/.cli'
        kv=[]
        ks=['token','auth-uuid']
        for _k in  ks:
            if not _k in self.config.keys():
                self.config[_k]=''
        self.config[key]=value
        for k,v in self.config.items():
            kv.append('%s=%s'%(k,v))
        try:
            if os.path.isfile(fn):
                with open(fn,'w') as f:
                    f.write("\n".join(kv))
                return True
            else:
                try:
                    with open(fn, 'w') as f:
                        f.write("\n".join(kv))
                except Exception as e:
                    logger.error(e)
        except Exception as er:
            logger.error(er)
            return False

    def _url_fetch(self,url,data=None,header={},timeout=30,httpCmd='',debug=False):
        html=''
        handle=None
        machine_id=self.get_product_uuid()
        key= self._get_config('auth-uuid')
        try:
            headers = {
                'User-Agent':'CLI agent(1.0)',
                'auth-uuid':key,
                'token':self._get_config('token'),
                'machine-id':machine_id,
            }
            if len(header)>0:
                for k,v in header.items():
                    headers[k]=v
            if data!=None:
                data=urllib.urlencode(data)
                if PY3:
                    data=data.encode('utf-8','ignore')
                # print(data)

            req = urllib2.Request(
                url =url,
                headers = headers,
                data=data
            )
            if httpCmd != "":
                req.get_method = lambda: httpCmd

            handle=urllib2.urlopen(req,timeout=timeout)



            html=handle.read()
            cm=r'<meta[^>]*charset=[\'\"]*?([a-z0-8\-]+)[\'\"]?[^>]*?>'
            if PY3:
                cm=cm.encode('utf-8','ignore')
            charset=re.compile(cm,re.IGNORECASE).findall(html)
            if len(charset) >0:
                if charset[0]=='gb2312':
                    charset[0]='gbk'
                if PY2:
                    html=unicode(html,charset[0])
            if PY3:
                return html.decode('utf-8','ignore')
        except Exception as e:
            raise Exception(e)
        finally:
            if handle!=None and handle.fp!=None:
                try:
                    handle.fp.close()
                except Exception as er:
                    pass

        return html

    def cmdline_args(self,s):
        import re
        s = re.subn(r'\\"', '{,,}', s)[0]
        s = re.subn(r"\\'", '{,}', s)[0]
        l = re.findall(r"'[^']+?'|\"[^\"]*?\"", s, re.IGNORECASE | re.MULTILINE)
        # l= re.findall(r"'[\s\S]*[\']?'|\"[\s\S]*[\"]?\"",s,re.IGNORECASE|re.MULTILINE)
        for i,v in enumerate(l):
            s=s.replace(v,'{'+str(i)+'}')
        p=re.split(r'\s+',s)
        ret=[]
        def repl(a):
            i=re.findall(r'\{\d+\}', a.group(0))
            a =  re.sub('\{\d+\}',  l[int(re.sub(r'^{|}$', '', i[0]))],a.group(0))
            return a

        for a in p:
            # print a
            i = re.findall(r'\{\d+\}', a)
            if len(i)>0:
                a=re.sub(r'[\s\S]+',repl,a)
            if re.match(r"'[\s\S]+'",a) or re.match(r'"[\s\S]+"',a):
                a=re.sub("^'|'$|^\"|\"$",'',a)
            a = re.subn(r"\{\,\,\}", '\"', a)[0]
            a = re.subn(r"\{\,\}", "\'", a)[0]
            ret.append(a)
        return ret

    # def cmdline_args(self,s):
    #     import re
    #     l= re.findall(r"'[\s\S]*[\']?'|\"[\s\S]*[\"]?\"",s,re.IGNORECASE|re.MULTILINE)
    #     for i,v in enumerate(l):
    #         s=s.replace(v,'{'+str(i)+'}')
    #     p=re.split(r'\s+',s)
    #     ret=[]
    #     for a in p:
    #         if re.match(r'\{\d+\}',a):
    #             a=l[int(re.sub(r'^{|}$','',a))]
    #         ret.append(a)
    #     return ret

    def getopt(self,inputs):
        def ptype(input):
            if input == "":
                return (0,"")
            if "-" == input[0] and len(input) == 2:
                return (1,input[1])
            if "--" == input[:2] and len(input) >= 4:
                return (2,input[2:])
            return (0,"")
        def istype(input):
            if len(input) <= 0:
                return 0
            if "-" == input[0]:
                return 1
            return 0
        ret = {}
        ret['__ctrl__']=''
        ret['__func__']=''
        u = 0
        ucount = len(inputs)
        icount = 0
        ls = []
        if ucount >= 1:
            while 1:
                if u >= ucount:
                    break
                if istype(inputs[u]) == 1:
                    break

                ls.append(inputs[u])
                u += 1

            inputs = inputs[u:]
            icount = len(inputs)

        if icount >= 1:
            i = 0
            state = 0
            while 1:
                t,name = ptype(inputs[i])
                for c in range(1):
                    if t == 0 :
                        i += 1
                        break
                    if i+1 < icount:
                        tt,tname = ptype(inputs[i+1])
                        if tt != 0:
                            ret[name] = ""
                            i += 1
                            break
                        ret[name] = inputs[i+1]
                        i += 2
                        break
                    ret[name] = ""
                    i += 1
                    break
                if i >= icount:
                    break
        if len(ls)==2:
            ret['__ctrl__']=ls[0]
            ret['__func__']=ls[1]
        elif len(ls)==1:
            ret['__ctrl__']=''
            ret['__func__']=ls[0]
        return (ret)

    def parse_argv(self,argv):
        data={}
        long_args=[]
        short_args=[]
        for v in argv:
            if v.startswith('--'):
                long_args.append(v.replace('--','')+"=")
            elif v.startswith('-'):
                short_args.append(v.replace('-',''))
        opts= getopt.getopt(argv,":".join(short_args)+":",long_args)
        for opt in opts[0]:
            data[opt[0].replace('-','')]=opt[1]
        if len(data)>0:
            return data
        else:
            return argv

    def md5(self, src):
        m2 = hashlib.md5()
        if PY3:
            src=str(src).encode('utf-8','ignore')
        m2.update(src)
        return m2.hexdigest()

    def now_datetime(self):
        now_datetime = time.strftime('_%Y-%m-%d_%H_%M_%S', time.localtime(time.time()))
        return now_datetime

    def execute(self,cmd,timeout=30):
        try:
            return ZbxCommand(cmd).run(timeout=timeout)
            # return os.popen(cmd).read()
        except Exception as err:
            logger.error(err)
            return ""


    def get_all_ip_list(self):
        if platform.system().lower()=='windows':
            name,xx,ips=socket.gethostbyname_ex(socket.gethostname())
            return ips
        else:
            # cmdline = "ip a | egrep \"^\s*inet.*\" | grep -v inet6 | awk '{print $2}' | awk -v FS='/' '{print $1}'"
            cmdline = "ip a"
            ret = self.execute(cmdline)
            ips= re.findall(r'inet\s*(\d+\.\d+\.\d+\.\d+)',ret)
            if len(ips)==0:
                return [self.get_host_ip()]
            else:
                return ips
            # lip=re.split(r'\n',ret)
            # ips=[]
            # for ip in lip:
            #     if str(ip).strip ()!='':
            #       ips.append(ip.strip())
            # return ips


    def get_uuid(self):
        return str(uuid.uuid4())

    def get_host_ip(self):
        ip='127.0.0.1'
        s=None
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        finally:
            try:
                if s!=None:
                    s.close()
            except Exception as er:
                pass
        return ip

    def get_one_ip(self):
        ips=self.get_all_ip_list()
        ips.sort()
        ret = [x for x in ips if x.startswith('10.') or  x.startswith('172.') or  x.startswith('192.') ]
        if len(ret)>1:
            return ret[0]
        return ''.join(ret)

    def get_product_uuid(self):
        if self.machine_id!='' and len(self.machine_id)==36:
            return self.machine_id
        product_uuid=''
        # if os.path.isfile('/sys/devices/virtual/dmi/id/product_uuid'):
        #     product_uuid=self.execute('cat /sys/devices/virtual/dmi/id/product_uuid').strip()
        if product_uuid=="":
            uuid_file='/etc/machine_id'
            if not os.path.exists(uuid_file):
                product_uuid=self.get_uuid()
                with open(uuid_file,'w') as file:
                    file.write(product_uuid)
            else:
                with open(uuid_file,'r') as file:
                    product_uuid=file.read()
        self.machine_id=product_uuid
        return product_uuid


    def get_hostname(self):
        os_name = os.name
        host_name = ""
        try:
            if os_name == 'nt':
                host_name = os.getenv('computername')
            elif os_name == 'posix':
                host = os.popen('hostname')
                try:
                    host_name = host.read().strip()
                except:
                    host_name=''
                finally:
                    host.close()
            if host_name.strip()=='':
                host_name= socket.gethostbyname()
        except Exception as er:
            logger.error(er)
            return ""
        return host_name.strip()


    def exec_filename(self):
        path = os.path.realpath(sys.path[0])
        if os.path.isfile(path):
            path = os.path.dirname(path)
            return os.path.abspath(path)+ os.path.sep+__file__
        else:
            caller_file = inspect.stack()[1][1]
            return os.path.abspath(os.path.dirname(caller_file))+ os.path.sep+__file__



    def tuple2list(self,*args):
        print(args)
        l=[]
        for i in args:
            l.append(i)
        return l

    def command_args(self,args):
        if isinstance(args,list) or isinstance(args,tuple):
            return '"%s"' % '" "'.join(args)
        else:
            return str(args)

class ZbxCli():

    def __init__(self,default_module):
        self.entry=server_url+'/'+default_module+"/%s"
        self.util=ZbxCommon()
        # self.etcd_prefix=etcd_prefix
    def ip(self,args):
        ips=self.util.get_all_ip_list()
        ip=''
        try:
            ip=self.util.url_fetch_witherr(self.entry%"ip").strip()
        except Exception as er:
            pass
        if ip!='' and ip in ips:
            print(ip)
        else:
            print(self.util.get_one_ip().strip())



    def download(self,args):
        argv= self.util.parse_argv(args)
        if isinstance(argv,list):
            argv={}
        if 'f' in argv.keys():
            f=argv['f']
        else:
            return '(error) -f(filename) require'
        if 'd' not in argv:
            d='/'
            try:
                d=getpass.getuser()
            except Exception as er:
                pass
            argv['d']=d
        if 'o' not in argv:
            argv['o']=argv['f']
        self.util.download(argv['f'],argv['d'],argv['o'])

    def httpserver(self,args):
        bflag=False
        try:
            __import__('simplefileserver')
            bflag = True
        except Exception as er:
            self.util.execute('pip install simplefileserver', timeout=300)
            try:
                __import__('simplefileserver')
                bflag=True
            except Exception as er:
                pass
        argv = self.util.parse_argv(args)
        port=8000
        directory='./'
        if 'p' in argv:
            port=argv['p']
        if 'd' in argv:
            directory=argv['d']
        cmd="cd %s && python -m SimpleHTTPServer %s"%(directory,port)
        if bflag:
            from simplefileserver import server
            server(int(port))
        else:
            zbxcli=ZbxCommand(cmd)
            zbxcli.run(timeout=-1)

    def ftpserver(self,args):
        argv = self.util.parse_argv(args)
        try:
            __import__('pyftpdlib')
        except Exception as er:
            self.util.execute('pip install pyftpdlib',timeout=180)
        port=21
        directory='./'
        user=''
        password=''
        if 'P' in argv:
            port=argv['P']
        if 'u' in argv:
            user=argv['u']
        if 'd' in argv:
            directory=argv['d']
        if 'p' in argv:
            password=argv['p']
        from pyftpdlib.authorizers import DummyAuthorizer
        from pyftpdlib.handlers import FTPHandler
        from pyftpdlib.servers import FTPServer
        authorizer = DummyAuthorizer()
        if user=='':
            authorizer.add_anonymous(homedir=directory)
        else:
            authorizer.add_user(username=user, password=password, homedir=directory, perm='elradfmw')
        handler = FTPHandler
        handler.authorizer = authorizer
        server = FTPServer(('0.0.0.0', port), handler)
        server.serve_forever()


    def upload(self,args):
        argv= self.util.parse_argv(args)
        if isinstance(argv,list):
            argv={}
        if 'f' in argv.keys():
            f=argv['f']
        else:
            return '(error) -f(filename) require'
        if 'd' not in argv:
            d='/'
            try:
                d=getpass.getuser()
            except Exception as er:
                pass
            argv['d']=d
        self.util.upload(self.entry%"upload", argv['f'],argv['d'])

    def help(self,args):
        ret=self.util.url_fetch(self.entry%'help')
        try:
            print(ret)
        except Exception as er:
            pass

    def upgrade(self,args):
        fn=self.util.exec_filename()
        content=self.util.url_fetch(self.entry%'upgrade')
        if content!='':
            open('/tmp/cli','w').write(content)
            os.system('chmod +x /tmp/cli')
            os.system('mv -f /tmp/cli %s' %(client_filename))
            print('success')
        else:
            print('fail')
    def adddoc(self,args):
        argv=self.util.getopt(args)
        if 'f' in argv:
            argv['d']=open(argv['f'],'r').read()

        ret=self.util.url_fetch(self.entry%'adddoc',{'param':json.dumps(argv)})
        print(ret)

    def daemon(self,argv):
        daemon = ZbxDaemon(pidfile)
        setattr(daemon,'zbxcli',self)
        key_file='/etc/cli/etcd-worker-key.pem'
        cert_file='/etc/cli/etcd-worker.pem'
        if os.path.exists(key_file) and os.path.exists(cert_file):
            opener=urllib2.build_opener(HTTPSHandler(cert_file=cert_file,key_file=key_file))
            urllib2.install_opener(opener)
        data= self.util.getopt(sys.argv[1:])
        opt = data.get('s')
        if PLATFORM=='windows':

            winDaemon=ZbxDaemonWin(daemon)
            if 'start' == opt:
                print("cli daemon start")
                winDaemon.action('start')
            elif 'stop' == opt:
                print("cli daemon stop")
                winDaemon.action('stop')
            elif 'restart' == opt:
                print("cli daemon restart")
                winDaemon.action('restart')
            elif 'debug' == opt:
                global_debug = True
                daemon.run()
            elif 'kill' == opt:
                daemon.kill()
            elif 'install' == opt:
                winDaemon.action('install')
            elif 'status' == opt:
                winDaemon.action('status')
            elif 'remove' == opt:
                winDaemon.action('remove')
            else:
                print("usage: cli deamon -s debug|start|stop|restart|status")
                sys.exit(2)
            sys.exit(0)
        else:
            if 'start' == opt:
                print("cli daemon start")
                daemon.start()
            elif 'stop' == opt:
                print("cli daemon stop")
                daemon.stop()
            elif 'restart' == opt:
                print("cli daemon restart")
                daemon.restart()
            elif 'debug' == opt:
                global_debug=True
                daemon.run()
            elif 'kill' == opt:
                daemon.kill()
            elif 'install'==  opt:
                pass
            elif 'status' == opt:
                daemon.status()
            else:
                print("usage: cli deamon -s debug|start|stop|restart|status")
                sys.exit(2)
            sys.exit(0)

    def logout(self,argv):
        home= os.path.expanduser('~')
        fn=home+'/.cli'
        if os.path.isfile(fn):
            with open(fn,"w") as f:
                f.write('')
    def register(self,argv):
        data= self.util.getopt(sys.argv[1:])
        if 'u' not in data:
            if PY3:
                data['u']=input('please input username: ')
            else:
                data['u']=raw_input('please input username: ')
        if 'p' not in data:
            data['p']=getpass.getpass('please input password: ')
        ret=self.util.url_fetch(server_url+'/%s/%s'%(module,action),{'param':json.dumps(data)})
        print(ret)

    def login(self,argv):
        data= self.util.getopt(sys.argv[1:])
        if 'u' not in data:
            if PY3:
                data['u'] = input('please input username: ')
            else:
                data['u'] = raw_input('please input username: ')
        if 'p' not in data:
            data['p']=getpass.getpass('please input password: ')
        ret=self.util.url_fetch(server_url+'/%s/%s'%(module,action),{'param':json.dumps(data)})
        if len(ret) == 36:
            self.util._set_config('auth-uuid',str(ret).strip())
            print('success')
        else:
            print(ret)

    def rexec(self,argv):
        data= self.util.getopt(sys.argv[1:])
        if 'u' not in data:
            if PY3:
                data['u']=input('please input username: ')
            else:
                data['u']=raw_input('please input username: ')
        if 'p' not in data:
            data['p']=getpass.getpass('please input password: ')
        ret=self.util.url_fetch(server_url+'/%s/%s'%(module,action),{'param':json.dumps(data)})
        print(ret)


    def config(self,argv):
        conf='''
pidfile=/var/zbxcli.pid
server_url=http://127.0.0.1:8005
'''
        with open(configfile,'w') as f:
            f.write(conf)

    def default(self,module,action,args):
        #argv= self.util.parse_argv(args)
        argv=self.util.getopt(args)
        if isinstance(argv,list):
            argv={}
        if isinstance(argv,dict):
            if not 's' in argv:
                argv['s']=self.util.get_hostname()
            if not 'i' in argv:
                argv['i']=self.util.get_one_ip()
            files=['file','key_file','key','f']
            for fk in files:
                if fk in argv and os.path.isfile(argv[fk]):
                    argv['filename'] = argv[fk]
                    fp=open(argv[fk],'rb')
                    argv[fk]=fp.read()
                    fp.close()

            #if not 'g' in argv:
            #    argv['g']="Discovered hosts"
            #if not 't' in argv:
            #    argv['t']="Meizu-System"
        ret=self.util.url_fetch(server_url+'/%s/%s'%(module,action),{'param':json.dumps(argv)},timeout=3*60)
        if ret.strip()!='':
            try:
                ret=json.dumps(json.loads(ret),sort_keys=True,indent=2,ensure_ascii=False)
            except Exception as er:
                pass
        print(ret)
        return ret

    def request(self,args):
        argv=self.util.getopt(args)
        url=''
        if not 'url' in argv.keys():
            print('--url(url) url is request')
            return
        else:
            url=argv['url']
        keys=['__func__','__ctrl__','url']
        data={}
        header={}
        for key in keys:
            if key in argv.keys():
                del argv[key]
        if 'd' in argv:
            d=argv['d']
            try:
                kv=json.loads(d)
                for k in kv.keys():
                    data[k]=kv[k]
            except Exception as er:
                pass
        if 'h' in argv:
            d=argv['h']
            try:
                kv=json.loads(d)
                for k in kv.keys():
                    header[k]=kv[k]
            except Exception as er:
                pass
        for key in argv.keys():
            if key not in ['d','d']:
                data[key]=argv[key]
        method="GET"
        if len(data)>0:
            method="POST"
        result=self.util._url_fetch(url,data=data,header=header,httpCmd=method)
        print(result)
        return result

    def info(self,argv):
        info={'server':server_url,'version':CLI_VERSION,'python':platform.python_version(),'group':CLI_GROUP}
        print(json.dumps(info,sort_keys=True,indent=2))

    def md5(self,argv):
        data= self.util.getopt(sys.argv[1:])
        if not 's' in data and not 'f' in data:
            print('-s(string) is required or -f(file name) is required')
            return
        if 'f' in data:
            if os.path.exists(data['f']):
                with open(data['f'],'rb') as fp:
                    data['s']=fp.read()
            else:
                print('-f(filename) is not found ')
                return
        print(self.util.md5(data['s']))

    def uuid(self,argv):
        print(self.util.get_uuid())

    def machine_id(self,argv):
        print(self.util.get_product_uuid())

    def eval(self,argv):
        context={}
        argv= self.util.getopt(sys.argv[1:])
        source=''
        method='dir'
        filename=''
        args=''
        if 'm' in argv:
            method=argv['m']
        if 's' in argv:
            source=argv['s']
        if 'f' in argv:
            filename=argv['f']
        if 'a' in argv:
            args=argv['a']
        if 'f' in argv:
            filename=argv['f']
            with open(filename,'r') as ff:
                source=ff.read()
            exec(source,context)
        if 's' in argv:
            print(eval(source))
            return
        infile = sys.stdin
        with infile:
            if source == '':
                source = infile.read()
            exec(source,context)
        if method=='dir':
            if hasattr(context,method):
                print(getattr(context,method)())
                return
        if not callable(context[method]):
            print( context[method])
        if args!='':
            print(context[method](*args.split(' ')))
        else:
            print(context[method]())



    def pq(self, argv):
        argv = self.util.getopt(sys.argv[1:])
        selector='html'
        method='text'
        html=''
        filename=''
        args=''
        if 's' in argv:
            selector=argv['s']
        if 'm' in argv:
            method=argv['m']
        if 'c' in argv:
            html=argv['c']
        if 'f' in argv:
            filename=argv['f']
        if 'a' in argv:
            args=argv['a']
        try:
            if filename!='':
                with open(filename,'r') as ff:
                    html=ff.read()
            else:
                if html=='':
                    infile=sys.stdin
                    with infile:
                        if html=='':
                            html= infile.read()
        except Exception as er:
            data={}
            pass
        def _jq(html, selector='html', method='html', args=''):
            try:
                from pyquery import PyQuery as PQ
            except Exception as er:
                ZbxCommand('pip install pyquery').run(timeout=120)
                try:
                    from pyquery import PyQuery as PQ
                except Exception as er:
                    print('please run cmd ,  pip install pyquery')

            doc = PQ(html)
            doc = doc(selector)
            if hasattr(doc, method):
                if args != '':
                    return getattr(doc, method)(args)
                else:
                    return getattr(doc, method)()
        print(_jq(html,selector,method,args))

    def len(self, argv):
        argv = self.util.getopt(sys.argv[1:])
        s=''
        try:
            infile=sys.stdin
            with infile:
                if s=='':
                    s= infile.read()
                    try:
                        d=json.loads(s)
                        if isinstance(d,list) or isinstance(d,dict):
                            print(len(d))
                            return
                    except Exception as er:
                        pass
                    print(len(s.strip()))
                    return
        except Exception as er:
            print(len(s.strip()))

    def keys(self, argv):
        argv = self.util.getopt(sys.argv[1:])
        s=''
        try:
            infile=sys.stdin
            with infile:
                if s=='':
                    s= infile.read()
                    try:
                        d=json.loads(s)
                        if isinstance(d,dict):
                            print(json.dumps(d.keys(),sort_keys=True, indent=2, ensure_ascii=False))
                            return
                    except Exception as er:
                        pass
                    print('')
                    return
        except Exception as er:
            print('')

    def kvs(self, argv):
        argv = self.util.getopt(sys.argv[1:])
        s=''
        key=''
        ks=[]
        readonly=False
        if 'r' in argv:
            readonly=True
        if 'k' in argv:
            key=argv['k']
            if key.find(',')>0:
                ks=key.split(',')
            else:
                ks=key.split('.')
        try:
            infile=sys.stdin
            with infile:
                if s=='':
                    s= infile.read()
                    try:
                        d=json.loads(s)
                        ret = []
                        if isinstance(d,dict):
                            for k in d.keys():
                                if len(ks)>0 and k not in ks:
                                    continue
                                if isinstance(d[k],dict) or isinstance(d[k],list):
                                    ret.append(k + '="%s"' % ( json.dumps(d[k]).replace('\\','\\\\').replace('"','\\"')))
                                    if readonly:
                                        ret.append('readonly %s'%(k))
                                else:
                                    ret.append(k+'="%s"'%( str(d[k]).replace('"','\"')))
                                    if readonly:
                                        ret.append('readonly %s' % (k))
                            print("\n".join(ret))
                            return
                        if isinstance(d,list):
                            j=0
                            for i in d:
                                ret.append('a'+str(j) + '="%s"' % (str(i).replace('"', '\"')))
                                j=j+1
                            print("\n".join(ret))
                            return
                    except Exception as er:
                        pass
                    print('')
                    return
        except Exception as er:
            print('')

    def cut(self, argv):
        argv = self.util.getopt(sys.argv[1:])
        s=''
        p=''
        if 'p' in argv:
            p=argv['p']
        try:
            infile=sys.stdin
            with infile:
                if s=='':
                    s= infile.read()
        except Exception as er:
            data={}
            pass

        def _cut(s, p):
            pos=p.split(':')
            if len(pos)==1:
                return s[int(pos[0])]
            if len(pos)==2:
                return s[int(pos[0]):int(pos[1])]
        print(_cut(s,p))

    def join(self, argv):
        argv = self.util.getopt(sys.argv[1:])
        s=''
        sep=','
        wrap = ''
        trim=False
        if 't' in argv:
            trim=True
        if 'w' in argv:
            wrap=argv['w']
        if 's' in argv:
            if argv['s']!=self.util.get_hostname():
                sep=argv['s']
        try:
            infile=sys.stdin
            with infile:
                if s=='':
                    s= json.loads( infile.read())
        except Exception as er:
            data={}
            pass

        def _join(s, sep):
            if isinstance(s,list):
                if trim:
                    t=[]
                    for i in s:
                        if isinstance(i,str) or isinstance(i,unicode):
                            if i.strip()=='':
                                continue
                        if i==None:
                            continue
                        t.append(i)
                    s=t
                if wrap!='':
                    s=['%s%s%s'%(wrap,str(i),wrap)  for i in s]
                return sep.join(s)
            return s
        print( _join(s,sep))


    def tail(self, argv):
        argv = self.util.getopt(sys.argv[1:])
        s=''
        num=10
        if 'n' in argv:
            try:
                num=int(argv['n'])
            except Exception as er:
                pass
        try:
            infile=sys.stdin
            with infile:
                if s=='':
                    s= infile.read()
        except Exception as er:
            data={}
            pass

        def _tail(s):
            lines=re.split("\n",s)
            return "\n".join( lines[-num:])
        print(_tail(s))

    def head(self, argv):
        argv = self.util.getopt(sys.argv[1:])
        s=''
        num=10
        if 'n' in argv:
            try:
                num=int(argv['n'])
            except Exception as er:
                num =argv['n']
        try:
            infile=sys.stdin
            with infile:
                if s=='':
                    s= infile.read()
        except Exception as er:
            data={}
            pass

        def _head(s,num):
            lines=re.split("\n",s)
            if str(num).find(":") > 0:
                nums=str(num).split(":")
                if len(nums)==2 and nums[1]!="":
                    return "\n".join( lines[ int(nums[0]):int(nums[1])])
                else:
                    return "\n".join(lines[int(nums[0]):])
            return "\n".join( lines[0:int(num)])
        print(_head(s,num))

    def split(self, argv):
        argv = self.util.getopt(sys.argv[1:])
        s=''
        sep=','
        if 's' in argv:
            if argv['s']!=self.util.get_hostname():
                sep=argv['s']
        try:
            infile=sys.stdin
            with infile:
                if s=='':
                    s= infile.read()
        except Exception as er:
            data={}
            pass

        def _split(s, sep):
            s=s.strip()
            return re.split(re.compile(sep, re.MULTILINE | re.IGNORECASE),s)
        print(json.dumps( _split(s,sep)))

    def splitj(self, argv):
        argv = self.util.getopt(sys.argv[1:])
        s=''
        sep=','
        field_pat='\s{1,}'
        line_pat='\n'
        header=''
        ftype='table'
        if 't' in argv:
            ftype=argv['t']
            if ftype=='kv':
                if not 'l' in argv:
                    line_pat='\s{1,}'
                if not 'f' in argv:
                    field_pat='='
        if 'f' in argv:
            field_pat=argv['f']
        if 'l' in argv:
            line_pat=argv['l']
        if 'h' in argv:
            header=argv['h']
        if 's' in argv:
            if argv['s']!=self.util.get_hostname():
                sep=argv['s']
        try:
            infile=sys.stdin
            with infile:
                if s=='':
                    s= infile.read()
        except Exception as er:
            data={}
            pass

        def _splitj(s, line_pat,field_pat,header,ftype):
            s=s.strip()
            lines=re.split(line_pat,s)
            if len(lines)==0:
                return []
            data=[]
            if ftype=='table':
                if header == '':
                    header = lines[0]
                fields = re.split(field_pat, header)
                for i in lines[1:]:
                    vals=re.split(field_pat,i)
                    k=0
                    row={}
                    if len(vals)<=len(fields):
                        for j in vals:
                            row[fields[k]]=vals[k]
                            k=k+1
                        data.append(row)
            elif ftype=='kv':
                data={}
                for i in lines:
                    vals=re.split(field_pat,i)
                    if len(vals)==2:
                        data[vals[0]]=vals[1]
            return data
        print(json.dumps( _splitj(s,line_pat,field_pat,header,ftype),sort_keys=True, indent=2, ensure_ascii=False))


    def rand(self,argv):
        argv = self.util.getopt(sys.argv[1:])
        print(random.random())

    def randstr(self,argv):
        argv = self.util.getopt(sys.argv[1:])
        l='10'
        if 'l' in argv:
            try:
                l=int(argv['l'])
            except Exception as er:
                pass
        seq=[chr(x) for x in range(65,91)]
        ret=[]
        i=int(l)
        while i>0:
            i=i-1
            ret.append(seq[random.randint(0,len(seq)-1)])
        print(''.join(ret))


    def randint(self,argv):
        argv = self.util.getopt(sys.argv[1:])
        r='1:100'
        if 'r' in argv:
            if len(argv['r'].strip().split(':'))==2:
                r=argv['r']
        r=r.split(':')
        if len(r)==2:
            print(random.randint(int(r[0]),int(r[1])))
        else:
            print(random.randint(0,100))


    def lower(self, argv):
        argv = self.util.getopt(sys.argv[1:])
        s=''
        try:
            infile=sys.stdin
            with infile:
                if s=='':
                    s= infile.read()
        except Exception as er:
            data={}
            pass
        print(s.strip().lower())

    def upper(self, argv):
        argv = self.util.getopt(sys.argv[1:])
        s=''
        try:
            infile=sys.stdin
            with infile:
                if s=='':
                    s= infile.read()
        except Exception as er:
            data={}
            pass
        print(s.strip().upper())


    def replace(self, argv):
        argv = self.util.getopt(sys.argv[1:])
        s=''
        n=''
        o=''
        if 'o' in argv:
            o=argv['o']
        if 'n' in argv:
            n=argv['n']
        try:
            infile=sys.stdin
            with infile:
                if s=='':
                    s= infile.read()
        except Exception as er:
            data={}
            pass

        def _replace(s, o, n):
            ret= re.subn(re.compile(o, re.MULTILINE | re.IGNORECASE), n, s)
            if len(ret)>0:
                return ret[0].strip()
            else:
                return s.strip()
        print(_replace(s,o,n))


    def match(self, argv):
        argv = self.util.getopt(sys.argv[1:])
        s=''
        o='im'
        m='.*'
        if 'o' in argv:
            o=argv['o']
        if 's' in argv:
            s=argv['s']
        if 'm' in argv:
            m=argv['m']
        try:
            infile=sys.stdin
            with infile:
                if s=='':
                    s= infile.read()
        except Exception as er:
            data={}
            pass
        def _match(s, m, o='ima'):
            flags = 0
            is_all=False
            for i in range(0, len(o)):
                if o[i] == 'i':
                    flags = flags | re.IGNORECASE
                if o[i] == 'm':
                    flags = flags | re.MULTILINE
                if o[i]=='a':
                    is_all=True
            r = re.compile(m, flags=flags)
            ret = r.findall(s)
            if is_all:
                return json.dumps(ret)
            if len(ret) > 0:
                return ret[0]
            else:
                return ''
        print(_match(s,m,o))

    def jq(self, argv):
        return self.json_val(argv)

    def json_val(self,argv):
        argv= self.util.getopt(sys.argv[1:])
        data=None
        sep=' '
        quote=''
        key=''
        ignore_eror=True
        pretty=True
        output='json'
        if 'p' in argv:
            pretty=False
        if 'v' in argv:
            ignore_eror = False
        if 'q' in argv:
            quote=argv['q']
        if 's' in argv:
            sep=argv['s']
        if 'k' in argv:
            key=argv['k']
        if 'o' in argv:
            output=argv['o']
        if 'd' in argv:
            data= json.loads(argv['d'])
        try:
            infile=sys.stdin
            with infile:
                if data==None:
                    data= json.loads(infile.read())
        except Exception as er:
            data={}
            pass
        ret=[]

        def get_json(data, key, output='text', sep=' ', quote='', pretty=False):
            def parse_dict(data, key):
                return data.get(key, None)

            def parse_list(data, key):
                ret = []
                if re.match(r'^\d+$', key):
                    return data[int(key)]

                for i in range(0, len(data)):
                    if isinstance(data[i], dict):
                        if key=='*':
                            for j in data[i].keys():
                                ret.append(data[i].get(j, None))
                        else:
                            ret.append(data[i].get(key, None))
                    elif isinstance(data[i], list):
                        for j in range(0, len(data[i])):
                            if key == '*':
                                ret.append(data[i][j])
                            else:
                                ret.append(data[i][j].get(key, None))

                return ret

            if key.find(',') != -1:
                ks = key.split(',')
            else:
                ks = key.split('.')

            for k in ks:
                if isinstance(data, list):
                    data = parse_list(data, k)
                    # print(k,data)
                elif isinstance(data, dict):
                    data = parse_dict(data, k)
                    # print(k,data)

            if output == 'json':
                if isinstance(data, dict) or isinstance(data, list):
                    if pretty:
                        return json.dumps(data, sort_keys=True, indent=2, ensure_ascii=False)
                    else:
                        return json.dumps(data)
                else:
                    return data

            if isinstance(data, list):
                if isinstance(data[0], dict):
                    if pretty:
                        return json.dumps(data, sort_keys=True, indent=2, ensure_ascii=False)
                    else:
                        return json.dumps(data)
                ret = []
                for i in data:
                    ret.append('%s%s%s' % (quote, str(i), quote))
                return sep.join(ret)
            if isinstance(data, dict):
                if pretty:
                    return json.dumps(data, sort_keys=True, indent=2, ensure_ascii=False)
                else:
                    return json.dumps(data)
            return data
        if key=='':
            if pretty:
                print(json.dumps(data,sort_keys=True,indent=2,ensure_ascii=False))
            else:
                print(json.dumps(data))
            return
        try:
            ret=get_json(data,key,output,sep,quote,pretty)
            if ret==None or ret=='':
                print('')
            else:
                print(ret)
        except Exception as er:
            if  ignore_eror:
                print('')
            else:
                print('(error)check -d(data) or -k(key)')


    def remote_server(self,module,action,argv,is_log="1"):
        if isinstance(argv,dict):
            if not 's' in argv:
                argv['s']=self.util.get_hostname()
            if not 'i' in argv:
                argv['i']=self.util.get_one_ip()
            #if not 'g' in argv:
            #    argv['g']="Discovered hosts"
            #if not 't' in argv:
            #    argv['t']="Meizu-System"

        try:
            ret=self.util.url_fetch_witherr(server_url+'/%s/%s'%(module,action),
                                    {'param':json.dumps(argv)})
            if is_log=='1':
                argv['kw']={}
                logger.info('remote_server: module:%s action:%s param:%s'%(module,action,json.dumps(argv)))
        except UnicodeDecodeError as er:
            try:
                ret = self.util.url_fetch_witherr(server_url + '/%s/%s' % (module, action),
                                      {'param': json.dumps(argv, encoding='gbk')})
                if is_log == '1':
                    argv['kw'] = {}
                    logger.info('remote_server with gbk: module:%s action:%s param:%s' % (module, action, json.dumps(argv)))
            except Exception as er:
                logger.error('remote_server with gbk'+str(er))
                ret=str(er)
        except Exception as er:
            if is_log == '1':
                logger.error('remote_server'+str(er)+ 'module:%s action:%s param:%s'%(module,action,json.dumps(argv)))
            ret=str(er)
        return ret

    def lshell(self, args):
        return self.localshell(args)

    def localshell(self,args):
        argv = self.util.getopt(args)
        result=''
        if 'f' in argv.keys():
            filename = argv['f']
        else:
            result= '(error) -f(filename) require'
            logger.error(result)
        if not os.path.exists(filename):
            result= '(error) -f(filename) %s  not found' % (filename)
            logger.error(result)
            return result
        src = open(filename, 'r').read()
        lines = re.split(r'\n', src)
        for line in lines:
            if line.strip() != '':
                break;
        is_python=False
        argstr=''
        if line.find('python') > 0:
            is_python = True
        if 'a' in argv.keys():
            argstr = argv['a']
        shell_argv = self.util.cmdline_args(argstr)
        timeout=60*10
        if 't' in argv.keys():
            try:
                timeout=int(argv['t'])
            except Exception as er:
                pass
        if is_python:
            cmd = ZbxCommand('%s %s %s' % (PYTHON_PATH, filename, " ".join(shell_argv)))
            result = cmd.run(timeout)
        elif line.find('bash') > 0:
            cmd = ZbxCommand('/bin/bash %s %s' % (filename, " ".join(shell_argv)))
            result = cmd.run(timeout)
        else:
            os.system("chmod +x %s" % (filename))
            cmd = ZbxCommand('%s %s' % (filename, " ".join(shell_argv)))
            result = cmd.run(timeout)
        print(result)
        return result

    def shell(self,args):
        if len(args)<1:
            print('ERROR: param is not enough')
            sys.exit(0)

        #path=tempfile.gettempdir()+os.sep+'zbxcli';
        filename=''
        dir='shell'
        # argv= self.util.parse_argv(args)
        argv= self.util.getopt(args)
        debug=False
        if 'f' in argv.keys():
            filename=argv['f']
        else:
            return '(error) -f(filename) require'
        if 'd' in argv.keys():
            dir=argv['d']
        else:
            dir='/'
            try:
                dir=getpass.getuser()
            except Exception as er:
                pass
        if 'x' in argv.keys():
            debug=True
        path=script_path+os.path.sep+dir
        # print(path)
        if not os.path.exists(path):
            if PLATFORM=='windows':
                self.util.execute('mkdir "%s"'%path)
            else:
                self.util.execute('mkdir -p %s' % path)

        self.util.execute('chmod 777 -R %s'% script_path,timeout=3)
        fn=path+os.path.sep+filename
        src=''
        is_python=False
        result=-1
        if not os.path.exists(fn) or  'u' in argv.keys():
            try:
                src=self.util.url_fetch_witherr(self.entry%'shell',{ 'file':filename, 'param': json.dumps(args[1:]),'dir':dir},timeout=60*10)
                def merge(src):
                    try:
                        def build_dir(path):
                            if not os.path.exists(path):
                                self.util.execute('mkdir -p %s' % path)
                        def save_file_content(param):
                            path=script_path + os.path.sep + param.get('dir','')
                            fn = path + os.path.sep + param.get('file','')
                            build_dir(path)
                            src = self.util.url_fetch_witherr(self.entry % 'shell',param,timeout=60 * 10)
                            if src!='':
                                open(fn, 'w').write(src)
                        pat ='#include\s+-f\s+(?P<filename>[a-zA-Z.0-9_-]+)?\s+-d\s+(?P<dir>[a-zA-Z.0-9_-]+)?|#include\s+-d\s+(?P<dir2>[a-zA-Z.0-9_-]+)?\s+-f\s+(?P<filename2>[a-zA-Z.0-9_-]+)?'
                        m = re.findall(pat, src)
                        flist = []
                        for i in m:
                            if i[0] != '':
                                flist.append({'file': i[0], 'dir': i[1],'param': json.dumps(args[1:])})
                            else:
                                flist.append({'file': i[3], 'dir': i[2],'param': json.dumps(args[1:])})
                        for i in flist:
                            save_file_content(i)

                        if len(flist)>0:
                            def replace(a):
                                try:
                                    filename = (a.group('filename') or a.group('filename2'))
                                    dir2 = (a.group('dir') or a.group('dir2'))
                                    fn=script_path + os.path.sep+dir2+os.path.sep+filename
                                    return open(fn,'r').read()
                                except Exception as er:
                                    logger.error(er)
                                    logger.error(flist)
                                    return a.group(0)
                            src=re.sub(pat,replace,src)
                    except Exception as er:
                        logger.error(er)
                    return src
                src=merge(src)


            except Exception as er:
                logger.error(er)
                logger.error('download error:file:%s param:%s dir:%s'%(filename),json.dumps(args[1:]),dir)
        if src!='':
            open(fn,'w').write(src)
        else:
            src=open(fn,'r').read()
        self.util.execute('chmod 777 -R %s' % script_path, timeout=3)
        lines=re.split(r'\n',src)
        for line in lines:
            if line.strip()!='':
                break;
        if line.find('python')>0:
                is_python=True
        argstr=''
        timeout=60*10
        if 'a' in argv.keys():
            argstr=argv['a']
        if 't' in argv.keys():
            try:
                timeout=int(argv['t'])
            except Exception as er:
                pass
        shell_argv=self.util.cmdline_args(argstr)
        shell_argv = ['"%s"' % (str(x).replace('\\', '\\\\').replace('\"', '\\\"')) for x in shell_argv]
        cmd=None
        if is_python:
            cmd=ZbxCommand('%s %s %s'% ( PYTHON_PATH, fn, " ".join(shell_argv)))
            result=cmd.run(timeout)
        elif line.find('bash')>0:
            if debug:
                cmd=ZbxCommand('/bin/bash -x %s %s'% (fn," ".join(shell_argv)))
            else:
                cmd = ZbxCommand('/bin/bash %s %s' % (fn, " ".join(shell_argv)))
            result=cmd.run(timeout)
        else:
            os.system("chmod +x %s" % (fn))
            cmd=ZbxCommand('%s %s'% (fn," ".join(shell_argv)))
            result=cmd.run(timeout)
        print(result)

        if cmd!=None:
            exit(cmd.return_code)

class ZbxDaemon(Daemon):


    def __getattr__(self,attr):
        if hasattr(self,'zbxcli'):
            if hasattr(self.zbxcli,attr):
                return getattr(self.zbxcli,attr)
        return None

    def get_etcd(self):
        try:
            now = time.time()
            if now - self.update_time > 600:
                print("=== get etcd")
                # self.etcd_conf =  json.loads(self.remote_server('cli','getetcd',{}) )
                # print(self.etcd_conf)
                # self.etcd_list=self.etcd_conf['server']
                # self.etcd_prefix=self.etcd_conf['prefix']
                if not isinstance(self.etcd_list,list):
                    raise Exception("get etcd list error")
                for host in self.etcd_list:
                    print(self.util.url_fetch_witherr("%s%s/heartbeat" % (host,self.etcd_prefix) ,data={'ttl':60,'value':'heartbeat'},httpCmd = 'PUT' ))
                    print(self.util.url_fetch_witherr("%s%s/servers" % (host,self.etcd_prefix) ,data={'ttl':60,'value':'servers'},httpCmd = 'PUT' ))
                self.update_time = now
        except Exception as er:
            print('get_etcd:'+str(er))
            time.sleep(3)
            # return self.get_etcd()

    def status2(self):
        try:
            filename='heartbeat'
            file_path=script_path+os.path.sep+'.'+filename
            if not os.path.exists(script_path):
                self.util.execute('mkdir -p %s'%script_path)
            if self.shellstr!='':
                open(file_path,'w').write(self.shellstr)
                os.chmod(file_path,755)
            cmd=ZbxCommand('%s %s'%(PYTHON_PATH,file_path),is_log=False)
            ret= cmd.run()
            return json.dumps(json.loads(ret))
        except Exception as er:
            if global_debug:
                print('status2'+str(er))
            return '{}'

    def heartbeat2server(self):
        try:
            ips=",".join(self.util.get_all_ip_list())
            # ret = self.zbxcli.default(default_module,'heartbeat',['--uuid',self.util.get_product_uuid(),
            #                                                       '--ips',ips,'--status', self.status(),'--platform',
            #                                                  platform.system().lower(),'--hostname',self.util.get_hostname() ])
            python_version='unknown'
            try:
                python_version=platform.python_version()
            except Exception as er:
                pass
            data={'uuid':self.util.get_product_uuid(),'ips':ips,'status':self.status2(),
                  'platform':platform.system().lower(),'hostname':self.util.get_hostname(),'python_version':python_version,'cli_version':CLI_VERSION }
            ret=self.util.url_fetch(server_url+'/%s/%s'%(module,'heartbeat'),{'param':json.dumps(data)})

            objs= json.loads(ret)

            self.salt=objs['salt']
            self.etcd_conf=objs['etcd']
            if 'shell' in objs.keys():
                self.shellstr=objs['shell']

                # print(self.util.execute(self.shellstr))

            self.etcd_list=objs['etcd']['server']
            self.etcd_prefix=objs['etcd']['prefix']
            self.etcd_user=objs['etcd'].get('user','guest')
            self.etcd_password = objs['etcd'].get('password','guest')
            self.etch_basic_auth=self.util.get_basic_auth(self.etcd_user,self.etcd_password)
            # print('salt',self.salt)
            logger.info("heartbeat2server %s OK"%(server_url))
            return 'ok'
        except Exception as er:
            print('heartbeat2server:\t'+str(er))
            time.sleep(3)
            logger.error('heartbeat2server'+str(er)+str(ret))
            return 'fail'

    def heartbeat(self):
        try:
            logger.info("=== heartbeat start")
            ip = self.util.get_product_uuid()
            for host in self.etcd_list:
                # print("heartbeat:  %s%s/heartbeat/%s" % (host,self.etcd_prefix,ip))
                ips=",".join(self.util.get_all_ip_list())
                try:
                    html=''
                    html = self.util.url_fetch_witherr("%s%s/heartbeat/%s" % (host,self.etcd_prefix,ip) ,data={'ttl':60*5,'value':ips},httpCmd = 'PUT' )
                    logger.info("heartbeat2etcd OK")
                    self.has_heartbeat_error=False
                except Exception as her:
                    pass
                if html != "":
                    break
            logger.info("=== heartbeata end")
        except Exception as er:

            time.sleep(3)
            print('heartbeat:\t'+str(er))
            if not self.has_heartbeat_error:
                logger.error('heartbeat error:'+str(er))
                self.has_heartbeat_error=True


    def watch_commmand2(self,wait_block=True):
        try:
            ip = self.util.get_product_uuid()
            # print("watch_commmand",ip,self.etcd_list)
            for host in self.etcd_list:
                content=''
                header={'Authorization':self.etch_basic_auth}
                try:
                    # content = self.util.url_fetch_witherr("%s%s/servers/%s?recursive=true" % (host,self.etcd_prefix,ip),header=header,timeout = 10 )
                    content=LongHttp.request("%s%s/servers/%s?recursive=true" % (host,self.etcd_prefix,ip),{},headers=header)

                except Exception as er:
                    time.sleep(5)
                    self.heartbeat2server()
                    pass
                if content!='':
                    rjson=json.loads(content)
                    if rjson['node'].get('nodes'):
                        self.queue.put({'ip': ip, 'content': content, 'host': host})
                        # self.feedback_result(ip,host,content)
                        break
                if wait_block:
                    #self.util.url_fetch("%s%s/servers/%s?wait=true&recursive=true" % (host,self.etcd_prefix,ip),header=header,timeout = 20+ random.randint(1,10) )
                    LongHttp.request("%s%s/servers/%s?wait=true&recursive=true" % (host,self.etcd_prefix,ip),headers=header,timeout = 20+ random.randint(1,10) )
                    try:
                        # content = self.util.url_fetch_witherr("%s%s/servers/%s?recursive=true" % (host,self.etcd_prefix,ip),header=header,timeout = 10 )
                        content = LongHttp.request("%s%s/servers/%s?recursive=true" % (host,self.etcd_prefix,ip),headers=header,timeout = 10 )
                    except Exception as her:
                        # print(her)
                        pass
                    # print("content   "+content)
                    if content != "":
                        self.queue.put({'ip': ip, 'content': content, 'host': host})
                        # self.feedback_result(ip,host,content)
                        break
        except Exception as er:
            print('watch_commmand:\t'+str(er))
            time.sleep(3)
            #logger.error('watch_commmand error:'+str(er))


    def watch_commmand(self,wait_block=True):
        content=''
        try:
            ip = self.util.get_product_uuid()
            # print("watch_commmand",ip,self.etcd_list)
            for host in self.etcd_list:
                content=''
                header={'Authorization':self.etch_basic_auth}
                try:
                    content = self.util.url_fetch_witherr("%s%s/servers/%s?recursive=true" % (host,self.etcd_prefix,ip),header=header,timeout = 10 )
                except Exception as er:
                    time.sleep(5)
                    self.heartbeat2server()
                    pass
                if content!='':
                    rjson=json.loads(content)
                    if rjson['node'].get('nodes'):
                        self.queue.put({'ip': ip, 'content': content, 'host': host})
                        # self.feedback_result(ip,host,content)
                        break
                if wait_block:
                    self.util.url_fetch("%s%s/servers/%s?wait=true&recursive=true" % (host,self.etcd_prefix,ip),header=header,timeout = 20+ random.randint(1,10) )
                    try:
                        content = self.util.url_fetch_witherr("%s%s/servers/%s?recursive=true" % (host,self.etcd_prefix,ip),header=header,timeout = 10 )
                    except Exception as her:
                        # print(her)
                        pass
                    # print("content   "+content)
                    if content != "":
                        rjson = json.loads(content)
                        if rjson['node'].get('nodes'):
                            self.queue.put({'ip': ip, 'content': content, 'host': host})
                        # self.feedback_result(ip,host,content)
                        break
        except Exception as er:
            print('watch_commmand:\t'+str(er))
            print(content)
            time.sleep(3)
            #logger.error('watch_commmand error:'+str(er))

    def delete_cmd(self,host, key):
        try:
            url = "%s%s?recursive=true" % (host,key)
            # self.util.url_fetch(url,httpCmd= 'DELETE' )
            data={'host':host,'key':key}
            self.util.url_fetch(server_url+'/%s/%s'%(module,'del_etcd_key'),data)
        except Exception as er:
            print('delete_cmd:\t'+(er))


    def consumer(self):
        cnt=0
        while True:
            try:
                if self.queue.qsize()>0:
                    cnt=0
                    data=self.queue.get()
                    # try:
                    #     self.feedback_result2(data['ip'],data['host'],data['content'])
                    # except Exception as er:
                    #     self.feedback_result(data['ip'],data['host'],data['content'])

                    self.feedback_result2(data['ip'],data['host'],data['content'])
                else:
                    interval=0.1
                    time.sleep(interval)
                    cnt=cnt+1
                    if cnt*interval>10:
                        cnt=0
                        self.watch_commmand(wait_block=False)
            except Exception as er:
                logger.error(er)
                print(er)

    def feedback_result(self,ip,host,content):
            if content==None or content=='':
                return
            try:
                # logger.info("process cmd")
                if content == "Not Found":
                    print("no found key")
                    return
                rjson = json.loads(content)
                if not rjson['node'].get('dir',False):
                    url = "%s/%s?recursive=true" % (host,rjson['node']['key'])
                    print("feedback_result"+ url)
                    self.util.url_fetch(url,httpCmd= 'DELETE' )
                    logger.info("publish is no dir")
                    return

                if not rjson['node'].get('nodes'):
                    # logger.info("no found command")
                    return

                logger.info("process cmd")
                key=''
                data={}
                for cNode in  rjson['node']['nodes']:
                    key = cNode['key']
                    createdIndex = cNode['createdIndex']
                    if createdIndex in self.index:
                        # self.delete_cmd(host, key)
                        continue
                    else:
                        self.index.append(createdIndex)
                    if len(self.index) > 5000:
                        self.index = self.index[-4800:]

                    # try:
                    #     cNode=json.loads(cNode['value'])
                    # except Exception as er:
                    #     pass
                    try:
                        # cNode=json.loads(cNode['value'])
                        cmd_uuid=str(cNode['value'])
                    except Exception as er:
                        logger.error('json error lost command : '+str(cNode))
                        self.delete_cmd(host,key)
                        print('json error lost command : '+str(er))
                        continue
                    # cmd=cNode['cmd']
                    # if PY2:
                    #     cmd = cmd.encode('utf-8')
                    # md5 = str(cNode['md5'])
                    argv={'uuid':cmd_uuid,'index':createdIndex,'host':host,'key':key}
                    ret=self.util.url_fetch_witherr(server_url+'/%s/%s'%(module,'get_cmd'),{'param':json.dumps(argv)},timeout=10)
                    if ret=='' or ret=='{}' or len(json.loads(ret))==0:
                        self.delete_cmd(host,key)
                        continue
                    data=json.loads(ret)
                    if PY2:
                        cmd = data['cmd'].encode('utf-8')
                    if PY3:
                        cmd=data['cmd']
                    md5 = str(data['md5'])

                    url_success=data.get('url_success','')
                    url_error=data.get('url_error','')
                    url = data.get('url', '')
                    feedback = data.get('feedback', '1')
                    _ip = data.get('ip', '')
                    log_to_file = data.get('log_to_file', '1')


                    if 'timeout' in data.keys():
                        timeout = float(data['timeout'])
                    else:
                        timeout=30
                    if md5==self.util.md5(cmd+str(self.salt)):

                        # self.keys.append(key)
                        self.delete_cmd(host,key)
                        def tmp(cmd,cmd_uuid,createdIndex,url_success,url_error,url,feedback,_ip,kw=None):
                            if global_debug:
                                print('cmd:',cmd)
                            if log_to_file=='0':
                                zbxcmd = ZbxCommand(cmd, is_log=False)
                            else:
                                zbxcmd = ZbxCommand(cmd,is_log=True)
                            result=zbxcmd.run(float(timeout),task_id=cmd_uuid,url_success=url_success,url_error=url_error,url=url,ip=_ip)
                            try:
                                result=result.decode('utf-8')
                            except Exception as utfer:
                                try:
                                    result=result.decode('gbk')
                                except Exception as gbker:
                                    try:
                                        result=result.decode('utf-8','ignore')
                                    except Exception as ler:
                                        pass
                            message = {'ip':ip, 'cmd':cmd, 'result':result,'index':createdIndex,'task_id':cmd_uuid,
                                       'error':zbxcmd.message_error,'return_code':zbxcmd.return_code,'success':zbxcmd.messge_success,
                                       "i":_ip,'kw':data}
                            #print(message)
                            # print(type(message))
                            if feedback=='1':
                                self.remote_server('cli','feedback_result',message,log_to_file)
                            # print(json.dumps(message))
                        threading.Thread(target=tmp,args=(cmd,cmd_uuid,createdIndex,url_success,url_error,url,feedback,_ip,data,)).start()
                    else:
                        print('salt error',self.salt)
                        logger.error('miss command %s ' %(cmd))
                        self.delete_cmd(host,key)
                        message = {'ip':ip, 'cmd':cmd, 'result':'valid salt','index':createdIndex}
                        self.remote_server('cli','feedback_result',message,log_to_file)

            except Exception as e:
                try:
                    self.delete_cmd(host,key)
                    logger.error('lost command : '+str(data))
                except Exception as er:
                    pass
                logger.error('feedback_result error:'+str(e))
                print('feedback_result:\t'+str(e))


    def feedback_result2(self,ip,host,content):
        if content == None or content == '':
            return
        try:
            # logger.info("process cmd")
            if content == "Not Found":
                print("no found key")
                return
            rjson = json.loads(content)
            if not rjson['node'].get('dir',False):
                url = "%s/%s?recursive=true" % (host,rjson['node']['key'])
                print("feedback_result2"+ url)
                self.util.url_fetch(url,httpCmd= 'DELETE' )
                logger.info("publish is no dir")
                return

            if not rjson['node'].get('nodes'):
                # logger.info("no found command")
                return

            key=''
            for cNode in  rjson['node']['nodes']:
                key = cNode['key']
                createdIndex = cNode['createdIndex']
                if createdIndex in self.index:
                    #self.delete_cmd(host, key)
                    continue
                else:
                    self.index.append(createdIndex)
                if len(self.index) > 5000:
                    self.index = self.index[-4800:]
                try:
                    cNode=json.loads(cNode['value'])
                except Exception as er:
                    logger.error('json error lost command : '+str(cNode))
                    self.delete_cmd(host,key)
                    print('json error lost command : '+str(er))
                    continue
                cmd=cNode['cmd']
                logger.info("process cmd")
                if PY2:
                    cmd = cmd.encode('utf-8')
                md5 = str(cNode['md5'])
                url_success = cNode.get('url_success', '')
                url_error = cNode.get('url_error', '')
                url = cNode.get('url', '')
                cmd_uuid=cNode.get('task_id', '')
                feedback=cNode.get('feedback', '1')
                _ip = cNode.get('ip', '')
                log_to_file=cNode.get('log_to_file', '1')

                if 'timeout' in cNode.keys():
                    timeout = float(cNode['timeout'])
                else:
                    timeout=30
                if md5==self.util.md5(cmd+str(self.salt)):

                    # self.keys.append(key)
                    self.delete_cmd(host,key)

                    def tmp(cmd, cmd_uuid, createdIndex, url_success, url_error, url,feedback,_ip,kw=None):
                        print('cmd:',cmd)
                        # result = ZbxCommand(cmd,is_log=True).run(float(timeout))
                        if log_to_file=='0':
                            zbxcmd = ZbxCommand(cmd, is_log=log_to_file)
                        else:
                            zbxcmd = ZbxCommand(cmd, is_log=log_to_file)
                        result = zbxcmd.run(float(timeout), task_id=cmd_uuid, url_success=url_success,url_error=url_error, url=url,ip=_ip)
                        try:
                            result=result.decode('utf-8')
                        except Exception as utfer:
                            try:
                                result=result.decode('gbk')
                            except Exception as gbker:
                                try:
                                    result=result.decode('utf-8','ignore')
                                except Exception as ler:
                                    pass
                        # message = {'ip':ip, 'cmd':cmd, 'result':result,'index':createdIndex,'task_id':cmd_uuid}
                        message = {'ip': ip, 'cmd': cmd, 'result': result, 'index': createdIndex, 'task_id': cmd_uuid,
                                   'error': zbxcmd.message_error, 'return_code': zbxcmd.return_code,
                                   'success': zbxcmd.messge_success,'i':_ip,'kw':kw}
                        # print(message)
                        # print(type(message))
                        if feedback=='1':
                            self.remote_server('cli','feedback_result',message,log_to_file)
                        # print(json.dumps(message))
                    # threading.Thread(target=tmp).start()
                    threading.Thread(target=tmp,args=(cmd, cmd_uuid, createdIndex, url_success, url_error, url,feedback,_ip,cNode,)).start()
                else:
                    print('salt error',self.salt)
                    logger.error('miss command %s ' %(cmd))
                    self.delete_cmd(host,key)
                    message = {'ip':ip, 'cmd':cmd, 'result':'valid salt','index':createdIndex}
                    self.remote_server('cli','feedback_result',message,log_to_file)

        except Exception as e:
            try:
                self.delete_cmd(host,key)
                logger.error('lost command : '+str(cNode))
            except Exception as er:
                pass
            logger.error('feedback_result error:'+str(e))
            print(e)


    def check(self):
        try:
            import psutil
            process=psutil.Process(os.getpid())
            def get_info(p,methods):
                val=0
                for m in methods:
                    if hasattr(process,m):
                        val=getattr(process,m)()
                        return val
            mem = get_info(process, ['memory_info', 'get_memory_info'])
            #cpu = get_info(process, ['cpu_percent', 'get_cpu_percent'])
            if mem.rss/1024/1024>500:
                logger.warning('cli client memory>500M ,exit')
                process.terminate()
        except ImportError as er:
            if random.random()<0.1:
                ZbxCommand('pip install psutil').run()
            logger.error(er)
        except Exception as er:
            pass





    def sync_conf(self):
        try:
            self.heartbeat2server()
        except Exception as er:
            pass
        while True:
            try:
                # self.get_etcd()
                ok=self.heartbeat2server()
                time.sleep(2)
                self.check()
                ## todo
                ##self.heartbeat() remove to server
                if ok!='ok':
                    time.sleep(5)
                elif not global_debug:
                    time.sleep(60*2+ random.randint(1,60*2))
                else:
                    time.sleep(10)
            except Exception as er:
                logger.error('sync_conf error:'+str(er))
                pass

    def run(self):
        self.queue=queue.Queue(50)
        self.index=[]
        self.update_time=time.time()-800
        self.has_heartbeat_error=False
        sync=threading.Thread(target=self.sync_conf)
        sync.setDaemon(True)
        sync.start()


        tc=threading.Thread(target=self.consumer)
        tc.setDaemon(True)
        tc.start()

        time.sleep(3)

        while True:
            try:
                # self.get_etcd()
                # self.heartbeat()
                self.watch_commmand()
                time.sleep(0.5)
            except Exception as e:
                pass
                time.sleep(5)



if __name__ == '__main__':

    if os.path.isfile(configfile):
        with open(configfile) as f:
            try:
                for l in f.read().strip().split("\n"):
                    k,v=l.split('=',1)
                    if k.strip()=='server_url' and v!='':
                        server_url=v.strip()
                    if k.strip()=='pidfile' and v!='':
                        pidfile=v.strip()
            except Exception as er:
                logger.error(er)
                pass

    server=os.environ.get('CLI_SERVER',server_url)
    default_module=os.environ.get('CLI_MODULE',default_module)

    parts=urlparse(server)
    server_url=parts.scheme+'://'+parts.netloc
    if parts.path.strip()!='':
        default_module= parts.path[1:]

    global_debug=os.environ.get('CLI_DEBUG',global_debug)
    module=default_module
    action='help'
    cli=ZbxCli(default_module)
    util = ZbxCommon()
    data= util.getopt(sys.argv[1:])

    try:
        def quit(signum, frame):
            logger.warning("ctrl+c quit")
            sys.exit(1)
        signal.signal(signal.SIGINT, quit)
        signal.signal(signal.SIGTERM, quit)
    except Exception as er:
        pass


    if data['__ctrl__']=='':
        if data['__func__']=='':
            action='help'
        else:
            action=data['__func__']
    else:
        module=data['__ctrl__']
        action=data['__func__']
    if hasattr(cli,action):
       getattr(cli,action)(sys.argv[2:])
    else:
       cli.default(module,action,sys.argv[1:])
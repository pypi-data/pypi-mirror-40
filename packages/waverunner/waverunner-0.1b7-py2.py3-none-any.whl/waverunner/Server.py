from __future__ import print_function

import sys
import os
import os.path as path
import fnmatch
import argparse
import hashlib
import binascii
import traceback
import threading
import time

from random import randint, getrandbits
from netifaces import interfaces, ifaddresses, AF_INET
from concurrent.futures import ThreadPoolExecutor
from socket import gethostname
from socket import error as socketerror
from collections import OrderedDict
from multiprocessing import cpu_count


if sys.version_info.major == 2:
    # for Python2
    from SocketServer import ThreadingMixIn
    from DocXMLRPCServer import DocXMLRPCServer, resolve_dotted_attribute
    from xmlrpclib import ServerProxy, Fault
    from Tkinter import *  ## notice capitalized T in Tkinter
    from ttk import Notebook
    import tkFileDialog
    import imp
    from Queue import Queue

    PY_SYSVER = 2

elif sys.version_info.major == 3:
    # for Python3
    from socketserver import ThreadingMixIn
    from xmlrpc.server import DocXMLRPCServer, resolve_dotted_attribute
    from xmlrpc.client import ServerProxy, Fault
    from tkinter import *  ## notice lowercase 't' in tkinter here
    from tkinter.ttk import Notebook
    from tkinter import filedialog as tkFileDialog
    import importlib
    from queue import Queue

    PY_SYSVER = 3

iflist = {}
for interface in interfaces():
    config = ifaddresses(interface)
    # AF_INET is not always present
    if AF_INET in config.keys():
        for link in config[AF_INET]:
            # loopback holds a 'peer' instead of a 'broadcast' address
            # if 'addr' in link.keys() and 'peer' not in link.keys():
            if 'addr' in link.keys():
                iflist.update({str(interface): link['addr']})
del interface

default_port = 11234
default_interface = [key for key in iflist.keys() if 'lo' not in key][0]
default_remote_ips = (('143.215.156.66', default_port),)
default_password = 'ratsofftoya'
default_notify_interval = 3 * 60
default_poll_interval = 1 * 60
default_max_outstanding_challenges = 5
default_challeng_ttl = 60
default_max_challenge_retries = 3
default_challenge_retry_interval = 3
default_job_queue_size = 100
default_max_n_workers = cpu_count()

thisfile = os.path.abspath(__file__)
thispath = os.path.split(thisfile)[0]


def PublicMethod(fn):
    setattr(fn, '_waverunner_public', True)
    return fn


def SecureMethod(fn):
    setattr(fn, '_waverunner_public', False)
    return fn


def PublicInstance(instance):
    setattr(instance, '_waverunner_public', True)
    return instance


def SecureInstance(instance):
    setattr(instance, '_waverunner_public', False)
    return instance


class OutOfChallengesError(RuntimeError):
    pass


class NoWaverunnerThereError(RuntimeError):
    pass


class MaxRetriesError(RuntimeError):
    pass


class ChallengeNotValidError(RuntimeError):
    pass


class ConflictingHostError(RuntimeError):
    pass


class JobQueueEmpty(RuntimeError):
    pass


class Client(threading.local):
    def __init__(self):
        self.address = None


class Job(object):
    def __init__(self, func, args, kwargs, host=None, timeout=None):
        self.host = str(host)
        self.fn = str(func)
        if isinstance(args, str):
            args = tuple([args])
        self.args = tuple(args) if args is not None else None
        self.kwargs = tuple((key, val) for key, val in kwargs.items()) if kwargs is not None else None
        self.timeout = int(timeout) if timeout is not None and timeout >= 0 else None
        self.accepted_time = time.time()
        self.completed_time = None
        self.id = str(hash(self))
        self.result = None

    def __hash__(self):
        return hash((
            hash(self.host),
            hash(self.fn),
            hash(self.args),
            hash(self.kwargs),
            hash(self.accepted_time)
        ))


class ThreadingRPCServer(ThreadingMixIn, DocXMLRPCServer, object):
    def __init__(self, *args, **kwargs):
        super(ThreadingRPCServer, self).__init__(*args, **kwargs)
        self.client = Client()
        self.lock = threading.Lock()

    def process_request_thread(self, request, client_address):
        # self.lock.acquire()
        self.client.address = client_address
        return super(ThreadingRPCServer, self).process_request_thread(request, client_address)

    # def _dispatch(self, method, params):
    #     """Dispatches the XML-RPC method.
    #
    #     This is monkeypatched from the source.
    #     Releasing the lock only in order to run the external code.
    #     """
    #     try:
    #         # call the matching registered function
    #         func = self.funcs[method]
    #     except KeyError:
    #         pass
    #     else:
    #         if func is not None:
    #             return func(*params)
    #         raise Exception('method "%s" is not supported' % method)
    #
    #     if self.instance is not None:
    #         if hasattr(self.instance, '_dispatch'):
    #             # call the `_dispatch` method on the instance
    #             self.lock.release()
    #             return self.instance._dispatch(method, params)
    #
    #         # call the instance's method directly
    #         try:
    #             func = resolve_dotted_attribute(
    #                 self.instance,
    #                 method,
    #                 self.allow_dotted_names
    #             )
    #         except AttributeError:
    #             pass
    #         else:
    #             if func is not None:
    #                 self.lock.release()
    #                 return func(*params)
    #
    #     raise Exception('method "%s" is not supported' % method)


class RPCServer(DocXMLRPCServer, object):
    def __init__(self, *args, **kwargs):
        super(RPCServer, self).__init__(*args, **kwargs)
        self.client = Client()

    def process_request(self, request, client_address):
        self.client.address = client_address
        return super(RPCServer, self).process_request(request, client_address)


class HookedDict(dict):
    def __init__(self, hookfn, *args, **kwargs):
        super(HookedDict, self).__init__(*args, **kwargs)
        self.hook = hookfn

    def __setitem__(self, *args, **kwargs):
        super(HookedDict, self).__setitem__(*args, **kwargs)
        self.hook()

    def update(self, *args, **kwargs):
        super(HookedDict, self).update(*args, **kwargs)
        self.hook()


class Waverunner(object):

    def __init__(self,
                 port=default_port,
                 interface=default_interface,
                 remote_ips=default_remote_ips,
                 path_to_serve=None,
                 password=default_password,
                 notify_interval=default_notify_interval,
                 polling_interval=default_poll_interval,
                 max_outstanding_challenges=default_max_outstanding_challenges,
                 challenge_ttl=default_challeng_ttl,
                 max_challenge_retries=default_max_challenge_retries,
                 challenge_retry_interval=default_challenge_retry_interval,
                 max_jobs_queued=default_job_queue_size,
                 max_n_workers=default_max_n_workers,
                 ):

        # user-facing
        self.password = str(password) if password is not None else default_password

        if notify_interval is None:
            self.notify_interval = 0
        else:
            self.notify_interval = int(notify_interval) if int(notify_interval) >= 0 else default_notify_interval

        if polling_interval is None:
            self.polling_interval = 0
        else:
            self.polling_interval = int(polling_interval) if polling_interval >= 0 else default_poll_interval

        if not remote_ips:
            self._remote_ips = None
        else:
            self._remote_ips = self._parse_remote_ip_spec(remote_ips)

        # semi-user-facing
        #     these have access methods, getters, setters, etc
        self._port = int(port) if port is not None else default_port
        if interface and len([key for key in iflist.keys() if 'lo' not in key]) == 0:
            raise RuntimeError('could not find that interface')
        else:
            self._iface = [key for key in iflist.keys() if interface in key][0] if interface else default_interface
        self._ip = iflist[self.iface]
        self._srv_path = None

        #     these are just a little bit more obscure parameters
        self._max_outstanding_challenges = max_outstanding_challenges if 0 < max_outstanding_challenges < 50 else 2
        self._max_challenge_retries = max_challenge_retries
        self._challenge_retry_interval = challenge_retry_interval
        self._challenge_ttl = int(challenge_ttl)
        self._challenge_tender_interval = 15
        self._max_jobs_queued = max_jobs_queued
        self._max_n_workers = max_n_workers if max_n_workers > 0 else cpu_count()

        # threading
        self._server_thread = None
        self._challenge_tender_thread = None
        self._poll_remote_hosts_thread = None
        self._notify_server_thread = None
        self._worker_threads = []

        self._events = {
            'stop_notify': threading.Event(),
            'stop_polling': threading.Event(),
            'stop_challenge_tender': threading.Event(),
            'shutdown': threading.Event(),
        }

        self._events['stop_notify'].set()
        self._events['stop_polling'].set()
        self._events['stop_challenge_tender'].set()
        self._events['shutdown'].clear()

        self._threadlocks = {
            'server_challenge': threading.Lock(),
            'client_challenge': threading.Lock(),
            'jobqueue': threading.Lock(),
            'put_results': threading.Lock()}

        self._worker_sem = threading.BoundedSemaphore(self._max_n_workers)

        # xmlrpc
        self._server = None
        self._serving = False
        self._srv_functions = []
        self._srv_instances = []
        self._srv_functions_secured = []
        self._srv_instances_secured = []

        # internal services
        self._registered_services = HookedDict(self._update_gui_vars)
        self._host_file = traceback.extract_stack(limit=2)[-2][0]
        self._host_path = os.path.split(self._host_file)
        self._outstanding_challenges = {}
        self._job_queues = {}
        self._pending_jobs = {}
        self._completed_jobs = {}
        self._tkroot = None
        self._rtvars = None

        if path_to_serve is not None:
            self.set_testpath(path_to_serve)

    @staticmethod
    def _parse_remote_ip_spec(remote_ips):
        if isinstance(remote_ips, str):
            if ',' in remote_ips:
                remote_ips = [item.strip() for item in remote_ips.split(',')]
            elif ' ' in remote_ips:
                remote_ips = [item.strip() for item in remote_ips.split(' ')]
            else:
                remote_ips = [remote_ips]
        parsed = []
        for i, user in enumerate(list(remote_ips)):
            if isinstance(user, str):
                user = user.split(':')
            if len(user) == 1:
                user = (user[0].strip('\''), default_port)
            elif len(user) == 2:
                user = (user[0].strip('\''), int(user[1]))
            parsed.append(tuple(user))

        return tuple(parsed) if parsed else None

    @property
    def port(self):
        return self._port

    @property
    def srv_path(self):
        return self._srv_path

    @property
    def ip(self):
        return self._ip

    @property
    def iface(self):
        return self._iface

    @property
    def registered_services(self):
        return self._registered_services

    @property
    def remote_ips(self):
        return self._remote_ips

    @property
    def known_services(self):
        return tuple([item[0] for item in self._srv_functions+self._srv_functions_secured+self._srv_instances \
                      + self._srv_instances_secured])

    @port.setter
    def port(self, value):
        self._set_port(value)

    @srv_path.setter
    def srv_path(self, value):
        self._set_srv_path(value)

    @ip.setter
    def ip(self, value):
        self._set_ip(value)

    @iface.setter
    def iface(self, value):
        self._set_iface(value)

    @remote_ips.setter
    def remote_ips(self, value):
        self._set_remote_ips(value)

    def _set_port(self, value):
        self._port = int(value)
        if self._rtvars is not None:
            self._rtvars['port'].set(str(self._port))

    def _set_srv_path(self, value):
        self._srv_path = str(value)
        if self._rtvars is not None:
            self._rtvars['srv_path'].set(self._srv_path)

    def _set_ip(self, value):
        self._ip = str(value)
        if self._rtvars is not None:
            self._rtvars['ip'].set(str(self._ip))

    def _set_iface(self, value):
        self._iface = str(value)
        if self._rtvars is not None:
            self._rtvars['iface'].set(self._iface)

    def _set_remote_ips(self, value):
        self._remote_ips = self._parse_remote_ip_spec(value)

    def _update_gui_vars(self):
        if self._rtvars is not None:
            for gui_var in self._rtvars.keys():
                self._rtvars[gui_var].set(getattr(self, gui_var))

    @PublicMethod
    def is_secure(self, fn):
        if fn in [name for name, _ in self._srv_functions_secured]:
            return True
        elif fn in [name for name, _ in self._srv_functions]:
            return False
        else:
            print('Server.is_secure(): could not find function named {}'.format(fn))
            return None

    @PublicMethod
    def get_challenge(self):
        with self._threadlocks['server_challenge']:

            if len(self._outstanding_challenges) >= self._max_outstanding_challenges:
                print('ran out of challenges')
                raise OutOfChallengesError

            else:
                client = self._server.client.address[0] if self._server.client.address is not None else 'local'
                challenge = ''.join([format(randint(0, 16), 'x') for i in range(256)])

                if client in self._outstanding_challenges:
                    self._outstanding_challenges[client].append(challenge)
                else:
                    self._outstanding_challenges.update({client: [challenge]})
                print('issued a challenge')
                return challenge

    @PublicMethod
    def notify(self, address, port, bare_fns, bare_insts, sec_fns, sec_insts):

        self.registered_services.update({
            ':'.join([address, str(port)]): [bare_fns, bare_insts, sec_fns, sec_insts],
        })
        print('got a notification from {}:{}'.format(address, port))
        return '10-4'

    def queue_request(self, ext_fn, args=None, host=None, kwargs=None, timeout=None):

        if host is None:
            host = ''

        job = Job(ext_fn, args, kwargs, host=host, timeout=timeout)

        with self._threadlocks['jobqueue']:
            if job.host not in self._job_queues:
                self._job_queues.update({job.host: OrderedDict()})
            self._job_queues[job.host].update({job.id: job})

        print('job queued')
        return job

    @SecureMethod
    def get_job_list(self):
        host, port = self._server.client.address
        joblist = []

        if host in self._job_queues and self._job_queues[host]:
            joblist.extend(list(self._job_queues[host].values()))

        if '' in self._job_queues and self._job_queues['']:
            joblist.extend(list(self._job_queues[''].values()))

        print('sent list of {} potential jobs to {}'.format(len(joblist), host))
        return tuple([(job.id, job.fn) for job in joblist])

    @SecureMethod
    def get_job(self, job_id):

        host, port = self._server.client.address
        job = None

        with self._threadlocks['jobqueue']:

            if host in self._job_queues and job_id in self._job_queues[host]:
                job = self._job_queues[host][job_id]
                self._pending_jobs.update({job.id: job})
                del self._job_queues[host][job_id]

            elif '' in self._job_queues and job_id in self._job_queues['']:
                job = self._job_queues[''][job_id]
                self._pending_jobs.update({job.id: job})
                del self._job_queues[''][job_id]

            if isinstance(job, Job):
                print('giving job {} to {}'.format(job.id, host))
                return str(job.id), job.fn, job.args, job.kwargs, job.timeout
            else:
                raise JobQueueEmpty

    @SecureMethod
    def put_job(self, job_id, result, success):
        job = [job for id, job in self._pending_jobs.items() if str(id) == job_id][0]
        host, port = self._server.client.address

        if not job:
            print('i couldnt find that job in the list of pending jobs...')
            return 'ERROR'

        if job.host != '' and host != job.host:
            raise ConflictingHostError

        print('trying to get threadlock on jobqueue...')

        with self._threadlocks['jobqueue']:

            print('got threadlock on jobqueue...')
            if not success:
                print('job {} failed'.format(job_id))
                print('putting it back on the queue')

                self._job_queues[job.host].update({job.id: job})
                del self._pending_jobs[job.id]
                return 'thanks for being a friend'

            else:
                print('received a completed job')
                job.result = result
                self._completed_jobs.update({job.id: job})
                del self._pending_jobs[job.id]
                return '10-4'

    def get_result(self, job, timeout=None):
        if not isinstance(job, Job):
            #assume it's an id
            id = job
        else:
            id = job.id

        t = 0
        while id not in self._completed_jobs:
            self._events['shutdown'].wait(1)
            t += 1
            if timeout and t > timeout:
                break
        try:
            rjob = self._completed_jobs[id]

        except KeyError:
            pass

        return rjob.result if rjob else None

    def _poll_remote_hosts(self):
        print('polling thread launched')
        while \
            not self._events['stop_polling'].is_set() \
            and not self._events['shutdown'].is_set() \
            and self._remote_ips \
            and self.polling_interval:

            self._events['stop_polling'].wait(timeout=self.polling_interval)

            n_busy_workers = len(self._worker_threads)
            if n_busy_workers >= self._max_n_workers:
                continue

            print('starting a round of polling')

            id = None

            for ip, port in self._remote_ips:
                if ip == self.ip and port == self.port:
                    continue

                n_busy_workers = len(self._worker_threads)
                if n_busy_workers >= self._max_n_workers:
                    break

                while True:
                    n_busy_workers = len(self._worker_threads)
                    if n_busy_workers >= self._max_n_workers:
                        break
                    try:
                        print('about to poll {}:{}'.format(ip, port))
                        l = self.external_request((ip, port), 'get_job_list')
                        if l:
                            j_id = [job[0] for job in l if job[1] in self.known_services][0]
                        else:
                            break
                        if j_id:
                            j = self.external_request((ip, port), 'get_job', j_id)
                        else:
                            break
                        if j:
                            id, fn_name, args, kwargs, timeout = j
                        else:
                            break

                    except NoWaverunnerThereError:
                        break

                    except Fault as err:
                        if 'JobQueueEmpty' in err.faultString:
                            break

                    if id and fn_name:
                        print('got a job from {}'.format(ip))
                        secure = self.is_secure(fn_name)
                        if secure is None:
                            print('i cannot run this job')
                            self.external_request((ip, port), 'put_job', id, 'FAILED', False)

                        if secure is True:
                            c = self.get_challenge()
                            r, s = self._generate_response(c)
                        else:
                            (r, s) = (None, None)

                        int_fn = None
                        for name, fn in self._srv_functions + self._srv_functions_secured + self._srv_instances + self._srv_instances_secured:
                            if name == fn_name:
                                int_fn = fn
                                break

                        if int_fn is not None:
                            self._launch_worker_thread((r, s), int_fn, args, kwargs, ip, port, id)

    def _launch_worker_thread(self, response_tup, int_fn, args, kwargs, ip, port, id):

        def execute(response_tup, int_fn, args, kwargs, ip, port, id):
            self._worker_sem.acquire()
            try:
                result = None

                if response_tup[0] is not None and response_tup[1] is not None:
                    if args is None and kwargs is None:
                        result = int_fn(response_tup)
                    if args is not None and kwargs is None:
                        result = int_fn(response_tup, *args)
                    elif args is None and kwargs is not None:
                        result = int_fn(response_tup, **kwargs)
                    elif args is not None and kwargs is not None:
                        result = int_fn(response_tup, *args, **kwargs)
                else:
                    if args is None and kwargs is None:
                        result = int_fn()
                    if args is not None and kwargs is None:
                        result = int_fn(*args)
                    elif args is None and kwargs is not None:
                        result = int_fn(**kwargs)
                    elif args is not None and kwargs is not None:
                        result = int_fn(*args, **kwargs)

                with self._threadlocks['put_results']:
                    self.external_request((ip, port), 'put_job', id, result, True)

            except Exception as e:
                with self._threadlocks['put_results']:
                    self.external_request((ip, port), 'put_job', id, result, e)

            finally:
                self._worker_sem.release()
                self._worker_threads.remove(threading.current_thread())

        t = threading.Thread(name='worker', target=execute,
                             args=(response_tup, int_fn, args, kwargs, ip, port, id))
        t.daemon = True
        t.start()
        self._worker_threads.append(t)

    def _generate_response(self, challenge, salt=None):
        salt = format(getrandbits(256), 'x').encode() if salt is None else salt
        key = binascii.hexlify(hashlib.pbkdf2_hmac('sha1', self.password.encode(), salt=salt, iterations=1000))
        return hashlib.sha1(key + challenge.encode()).hexdigest(), salt

    def threaded_external_requests(self, hosts, fn_names, args=None, kwargs=None, timeout=5 * 60):

        with ThreadPoolExecutor(max_workers=100) as E_daddy:
            if args is None and kwargs is None:
                futures = E_daddy.map(self.external_request, hosts, fn_names, timeout=timeout)
            elif args is not None and kwargs is None:
                futures = E_daddy.map(self.external_request, hosts, fn_names, args, timeout=timeout)
            elif args is None and kwargs is not None:
                futures = E_daddy.map(self.external_request, hosts, fn_names, kwargs, timeout=timeout)
            else:
                futures = E_daddy.map(self.external_request, hosts, fn_names, args, kwargs, timeout=timeout)

            results = []
            for i in futures:
                results.append(i)
            return results

    def external_request(self, remote_host, remote_fn_name, *args, **kwargs):

        if isinstance(remote_host, str):
            remote_host = remote_host.split(':')
        if len(remote_host) < 2:
            remote_host = [remote_host, default_port]

        host = ServerProxy('http://{}:{}'.format(remote_host[0], remote_host[1]))

        try:
            secure = host.is_secure(remote_fn_name)

        except socketerror:
            raise NoWaverunnerThereError

        if secure is True:
            with self._threadlocks['client_challenge']:
                print('got challenge acquisition lock')
                retry_ct = 0
                response = None

                try:
                    while retry_ct < self._max_challenge_retries:
                        challenge = host.get_challenge()
                        response, salt = self._generate_response(challenge)
                        break

                except socketerror:
                    raise NoWaverunnerThereError

                except OutOfChallengesError:
                    print('server was out of challenges')
                    retry_ct += 1
                    self._events['shutdown'].wait(self._challenge_retry_interval)
                    pass

                if response is None:
                    raise MaxRetriesError("couldn't get a challenge and ran out of retries")

        if secure is True and response is not None:
            print('got a challenge. calling remote fn: {}'.format(remote_fn_name))
            result = host.__getattr__(remote_fn_name)((response, salt), *args, **kwargs)
            print('result= {}'.format(result))

        elif secure is False:
            print('calling public remote fn: {}'.format(remote_fn_name))
            result = host.__getattr__(remote_fn_name)(*args, **kwargs)
            print('result={}'.format(result))

        elif secure is None:
            print('remote host did not recognize that fn: {}'.format(remote_fn_name))
            result = None

        return result

    def _external_security_wrapper(self, fn):

        def wrapped(response_tuple, *args, **kwargs):
            try:
                print('received external request for secure function')
                response, salt = response_tuple
                salt = salt.data if hasattr(salt, 'data') else salt
                client = self._server.client.address[0] if self._server.client.address is not None else 'local'

                if client not in self._outstanding_challenges:
                    print('challenge was not issued by me')
                    return ChallengeNotValidError

                authorized = False

                with self._threadlocks['server_challenge']:
                    for index, item in enumerate(self._outstanding_challenges[client]):
                        test_response = self._generate_response(item, salt)[0]
                        if response == test_response:
                            del self._outstanding_challenges[client][index]
                            authorized = True

                if authorized:
                    print('accepted response for secure function: {}'.format(fn.__name__))
                    print('running secure fn: {}'.format(fn.__name__))
                    result = fn(*args, **kwargs)
                else:
                    print('rejecting response for secure function: {}'.format(fn.__name__))
                    result = ChallengeNotValidError

                return result

            except JobQueueEmpty:
                raise JobQueueEmpty

            except Exception as e:
                print('exception raised before calling secure function: {}'.format(fn.__name__))
                return e

        wrapped.__name__ = fn.__name__
        return wrapped

    def get_completed_jobs(self, flush=False):
        if not flush:
            return self._completed_jobs
        else:
            j = self._completed_jobs
            self._completed_jobs = []
            return j

    def tend_challenges(self):
        ages = {}
        update_interval = self._challenge_tender_interval

        def prune_challenges():
            """
            make sure you have a lock before entering here
            :return:
            """
            hosts = self._outstanding_challenges.keys()
            ids = [[hash(str(host) + str(item)) for item in self._outstanding_challenges[host]] for host in hosts]
            ids_flat = []
            [ids_flat.extend(item) for item in ids]

            newct = 0
            for id in ids_flat:
                if id not in ages:
                    ages.update({id: 0})
                    newct += 1
                else:
                    ages[id] += update_interval
            print('tender found {} new challenges have been issued.'.format(newct))

            purges = []
            for id, age in ages.items():
                if id not in ids_flat:
                    purges.append(id)
                if age > self._challenge_ttl:
                    purges.append(id)

            print('pruning {} challenges'.format(len(purges)))
            for item in purges:
                if item in ages:
                    del ages[item]

                for i, host in enumerate(hosts):
                    for j, item in enumerate(self._outstanding_challenges[host]):
                        if ids[i][j] == item:
                            del self._outstanding_challenges[host][j]

            print('outstanding challenges: {}'.format(ages))
            print('tender going to sleep')

        while not self._events['stop_challenge_tender'] and not self._events['shutdown'].is_set():
            with self._threadlocks['server_challenge']:
                prune_challenges()

            self._events['stop_challenge_tender'].wait(timeout=update_interval)

    def notify_users(self):
        print('user notification thread launched')
        if not self._remote_ips or self.notify_interval == 0:
            return

        while not self._events['stop_notify'].is_set() and not self._events['shutdown'].is_set():
            print('starting a round of notifications')

            for ip, port in self._remote_ips:
                if not (ip == self.ip and port == self.port):
                    try:
                        print('about to notify {}:{}'.format(ip, port))
                        self.external_request(
                            (ip, port),
                            'notify',
                            self.ip, self.port,
                            [name for name, _ in self._srv_functions],
                            [name for name, _ in self._srv_instances],
                            [name for name, _ in self._srv_functions_secured],
                            [name for name, _ in self._srv_instances_secured]
                        )
                        print('notified {}:{}'.format(ip, port))

                    except NoWaverunnerThereError:
                        pass

            self._events['stop_notify'].wait(timeout=self.notify_interval)

    def register_remote(self, ip, port=None):
        if ':' in ip and port is None:
            self._remote_ips.append(tuple(ip.split(':')))
        elif ip and not port:
            self._remote_ips.append((ip, self.default_port))
        elif ip and port:
            self._remote_ips.append((ip, port))

    def make_gui(self, ):

        self._tkroot = Tk()
        self._tkroot.title('WaveRunner')

        self._rtvars = {'srv_path': StringVar(),
                       'ip': StringVar(),
                       'iface': StringVar(),
                       'port': StringVar(),
                       'registered_services': StringVar(), }

        self._update_gui_vars()

        note = Notebook(self._tkroot, padding=0)
        note.grid(sticky=N + S + E + W)

        status_tab = Frame(note)
        status_tab.grid(sticky=N + S + E + W)
        config_tab = Frame(note)
        config_tab.grid(sticky=N + S + E + W)

        note.add(status_tab, text="Status", sticky=N + S + E + W, padding=10)
        note.add(config_tab, text="Configure", sticky=N + S + E + W, padding=10)

        """ Status Tab """
        Label(status_tab, text="Waverunner is running", font="Sans 24 bold").grid(columnspan=2)

        ip_lframe = LabelFrame(status_tab, text="Waverunner http server address")
        ip_lframe.grid(row=1, padx=10, pady=10, sticky=E)
        Label(ip_lframe, textvariable=self._rtvars['ip']).grid(row=0, column=0, sticky=E)
        Label(ip_lframe, text=':').grid(row=0, column=1)
        Label(ip_lframe, textvariable=self._rtvars['port']).grid(row=0, column=2, sticky=W)

        testdir_lframe = LabelFrame(status_tab, text="Waverunner tests path")
        testdir_lframe.grid(row=2, padx=10, pady=10, sticky=E)
        Label(testdir_lframe, textvariable=self._rtvars['srv_path']).grid(row=1, column=1)

        password_lframe = LabelFrame(status_tab, text="Password")
        password_lframe.grid(row=3, padx=10, pady=10, sticky=E)
        Label(password_lframe, text=self.password).grid()

        services_lframe = LabelFrame(status_tab, text="Registered Services")
        services_lframe.grid(row=4, padx=10, pady=10, sticky=E)
        Label(services_lframe, textvariable=self._rtvars['registered_services']).grid()

        Button(status_tab, text="Change\nTest Directory", command=self.gui_update_testpath).grid(row=2, column=1,
                                                                                                 sticky=W)
        Button(status_tab, text="Copy", command=self.gui_address_to_clipboard).grid(row=1, column=1, sticky=W)

        Label(status_tab, text='You can get more details by directing a web browser\nto the ip address above.').grid(
            row=5, sticky=S + W)
        Button(status_tab, text="QUIT", bg='red', fg="black", font="sans 24 bold", command=self.exit_gracefully).grid(
            row=5, column=1, sticky=S + E)

        """ Config Tab """
        conff1 = LabelFrame(config_tab, text="select ethernet interface")
        conff1.grid()
        [Radiobutton(conff1, text=str(iface), variable=self._rtvars['iface'], value=str(iface),
                     command=self.resolve_interface_request).grid(column=0, sticky=W) for iface in iflist.keys()]

    def gui_address_to_clipboard(self):
        address = ':'.join([self.ip, str(self.port)])
        self.copytext(address)

    def gui_update_testpath(self):
        cur_path = self.srv_path
        if cur_path:
            newpath = os.path.abspath(tkFileDialog.askdirectory(initialdir=cur_path))
        else:
            newpath = os.path.abspath(tkFileDialog.askdirectory())
        if newpath and os.path.isdir(newpath):
            self.set_testpath(newpath)

    def set_testpath(self, path):
        testpath = os.path.abspath(path)
        if testpath != self.srv_path and testpath != thispath and testpath and testpath is not None:
            serving = bool(self._server)
            _ = self.stop_service() if serving else None
            self.parse_test_dir(testpath)
            _ = self.start_service() if serving else None

    def parse_test_dir(self, new_path):

        testmodules = _list_modules_at_path(new_path)

        print('found modules: {}'.format([item[0] for item in testmodules]))

        if self.srv_path is not None and self.srv_path in sys.path and self.srv_path != new_path:
            sys.path.remove(self.srv_path)
        self._set_srv_path(new_path)
        if self.srv_path not in sys.path:
            sys.path.append(self.srv_path)

        live_modules = []
        for module_name, module in testmodules:
            try:
                live_modules.append(_get_live_module(module))
            except (ImportError, SyntaxError, TypeError, ValueError) as e:
                print('problem importing {}: {}. moving on...'.format(module, e.message))

        for module in live_modules:
            for itemname, item in [(item, getattr(module, item)) for item in dir(module)]:
                if hasattr(item, '_waverunner_public'):

                    if item._waverunner_public == True:
                        if callable(item):
                            self.register_insecure_method(item, modulename=module.__name__)
                        else:
                            self.register_insecure_instance(item, modulename=module.__name__)

                    elif item._waverunner_public == False:
                        if callable(item):
                            self.register_secure_method(item, modulename=module.__name__)
                        else:
                            self.register_secure_instance(item, modulename=module.__name__)

        if self._srv_functions:
            print('methods available:\n{}'.format('\n'.join(
                ['    {}'.format(name) for name, _ in self._srv_functions]
            )))
        if self._srv_instances:
            print('instances available:\n{}'.format('\n'.join(
                ['    {}'.format(name) for name, _ in self._srv_instances]
            )))
        if self._srv_functions_secured:
            print('methods available:\n{}'.format('\n'.join(
                ['    {}'.format(name) for name, _ in self._srv_functions_secured]
            )))
        if self._srv_instances_secured:
            print('instances available:\n{}'.format('\n'.join(
                ['    {}'.format(name) for name, _ in self._srv_instances_secured]
            )))

    def register_secure_method(self, method, modulename=None):
        serving = self._serving
        self.stop_service()
        name = '.'.join([modulename, method.__name__]) if modulename is not None else method.__name__
        self._srv_functions_secured.append((name, self._external_security_wrapper(method)))
        if serving:
            self.start_service()

    def register_insecure_method(self, method, modulename=None):
        assert hasattr(method, '_waverunner_public') and method._waverunner_public == True
        serving = self._serving
        self.stop_service()
        name = '.'.join([modulename, method.__name__]) if modulename is not None else method.__name__
        self._srv_functions.append((name, method))
        if serving:
            self.start_service()

    def register_secure_instance(self, instance, modulename=None):
        serving = self._serving
        self.stop_service()
        name = '.'.join([modulename, instance.__name__]) if modulename is not None else instance.__name__
        self._srv_functions_secured.append((name, self._external_security_wrapper(instance)))
        if serving:
            self.start_service()

    def register_insecure_instance(self, instance, modulename=None):
        assert hasattr(instance, '_waverunner_public') and instance._waverunner_public == True
        serving = self._serving
        self.stop_service()
        name = '.'.join([modulename, instance.__name__]) if modulename is not None else instance.__name__
        self._srv_functions.append((name, instance))
        if serving:
            self.start_service()

    def set_interface(self, ifname):
        ip = iflist[ifname.get()]
        self._set_ip(ip)

    def resolve_interface_request(self, ):
        if self._server is not None:
            needsrestart = True
            self.stop_service()
        else:
            needsrestart = False

        self.set_interface(self._rtvars['iface'])

        if needsrestart:
            self.start_service()

    def copytext(self, text_to_copy=''):
        clip = Tk()
        clip.withdraw()
        clip.clipboard_clear()
        clip.clipboard_append(text_to_copy)
        clip.destroy()

    def start_xmlrpc_server(self, ):

        if self._server is None and self._server_thread is None:

            server = ThreadingRPCServer(addr=(self.ip, int(self.port)), allow_none=True, bind_and_activate=False)
            # server = RPCServer(addr=(self.ip, int(self.port)))

            server.set_server_title('Waverunner in python')
            server.set_server_documentation('Application provides RPC access to python scripts')
            server.set_server_name('waverunner_' + gethostname())

            # register system functions
            self.register_insecure_method(self.get_challenge)
            self.register_insecure_method(self.notify)
            self.register_insecure_method(self.is_secure)
            self.register_secure_method(self.get_job_list)
            self.register_secure_method(self.get_job)
            self.register_secure_method(self.put_job)

            for name, fn in self._srv_functions + self._srv_functions_secured:
                server.register_function(fn, name=name)

            for name, inst in self._srv_instances + self._srv_instances_secured:
                server.register_instance(inst, name=name)

            server.register_introspection_functions()
            server.register_multicall_functions()

            def serve_and_die(server):
                server.server_bind()
                server.server_activate()
                server.serve_forever()

            server_thread = threading.Thread(name='xmlrpc_server', target=serve_and_die, args=(server,))
            server_thread.daemon = True
            server_thread.start()

            print('server started at {}:{}'.format(self.ip, self.port))
            self._server = server
            self._server_thread = server_thread
            self._outstanding_challenges.clear()

        else:
            print('server already running... restarting')
            self.stop_xmlrpc_server()
            self.start_xmlrpc_server()

    def stop_xmlrpc_server(self):
        self._server.shutdown()
        self._server.server_close()
        self._server_thread.join()
        print('server stopped')

    def start_notify_server(self, ):
        self._events['stop_notify'].clear()
        self._notify_server_thread = threading.Thread(target=self.notify_users, name='notifier')
        self._notify_server_thread.daemon = True
        self._notify_server_thread.start()

    def stop_notify_server(self, ):
        self._events['stop_notify'].set()
        self._notify_server_thread.join()

    def start_polling(self):
        self._events['stop_polling'].clear()
        self._poll_remote_hosts_thread = threading.Thread(target=self._poll_remote_hosts, name='remotes_poller')
        self._poll_remote_hosts_thread.daemon = True
        self._poll_remote_hosts_thread.start()

    def stop_polling(self):
        self._events['stop_polling'].set()
        self._poll_remote_hosts_thread.join()

    def start_challenge_tender(self):
        self._events['stop_challenge_tender'].clear()
        self._challenge_tender_thread = threading.Thread(target=self.tend_challenges, name='challenge_tender')
        self._challenge_tender_thread.daemon = True
        self._challenge_tender_thread.start()

    def stop_challenge_tender(self):
        self._events['stop_challenge_tender'].set()
        self._challenge_tender_thread.join()

    def start_service(self, ):
        if not self._serving:
            self.start_xmlrpc_server()
            self.start_challenge_tender()
            self.start_notify_server()
            self.start_polling()
            self._serving = True

    def stop_service(self, ):
        if self._serving:
            self.stop_xmlrpc_server()
            self.stop_challenge_tender()
            self.stop_notify_server()
            self.stop_polling()
            self._serving = False

    def serve_forever(self):
        self.start_service()
        try:
            while not self._events['shutdown'].is_set():
                self._events['shutdown'].wait(1)
        except:
            pass
        finally:
            self.exit_gracefully()

    def join(self):
        try:
            while not self._events['shutdown'].is_set():
                self._events['shutdown'].wait(1)
        except:
            pass
        finally:
            self.exit_gracefully()

    def exit_gracefully(self, ):
        self._events['shutdown'].set()
        self.stop_service()
        if self._tkroot is not None:
            self._tkroot.quit()
            self._tkroot = None

        for t in self._worker_threads:
            try:
                t.join()
            except:
                pass

    def list_remote_services(self):
        return repr(self.registered_services)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--directory', '-d')
    parser.add_argument('--port', '-p')
    parser.add_argument('--remotes', '-r')
    parser.add_argument('--password', '-s')
    parser.add_argument('--notify', '-n', action='store_true')
    parser.add_argument('--notify-interval', '-i')
    parser.add_argument('--poll', '-P', action='store_true')
    parser.add_argument('--poll-interval', '-I')
    parser.add_argument('--gui', action='store_true')

    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print("invalid directory specified")
        sys.exit(1)
    else:
        directory = os.path.abspath(args.directory)

    if args.port and not 10 < int(args.port) < 65535:
        print('invalid port specified')
        sys.exit(1)
    elif not args.port:
        port = default_port
    else:
        port = int(args.port)

    if args.remotes:
        remotes = args.remotes.split(',')
    else:
        remotes = default_remote_ips

    if args.password:
        password = str(args.password)
    else:
        password = default_password

    if args.notify:
        notify_interval = default_notify_interval
    elif args.notify_interval:
        notify_interval = int(args.notify_interval)
    else:
        notify_interval = default_notify_interval

    if args.poll:
        poll_interval = default_poll_interval
    elif args.poll_interval:
        poll_interval = int(args.poll_interval)
    else:
        poll_interval = default_poll_interval

    server = Waverunner(
        port=port,
        remote_ips=remotes,
        path_to_serve=directory,
        password=password,
        notify_interval=notify_interval,
        polling_interval=poll_interval,
    )

    try:
        server.start_service()
        if args.gui:
            server.make_gui()
            server._tkroot.mainloop()
        server.join()

    except Exception as e:
        raise e

    finally:
        server.exit_gracefully()


def _file2mod(filepath):
    return os.path.split(filepath)[-1].split('.py')[0]


def _list_modules_at_path(pathspec, names=None):
    assert os.path.isdir(pathspec)
    mods = [file.split('.')[0] for file in fnmatch.filter(os.listdir(pathspec), '[!_]*.py')]
    mods.sort()
    mods = list(filter(lambda item: item in names, mods)) if names else mods
    paths = [path.join(pathspec, mod + '.py') for mod in mods]
    return tuple(zip(mods, paths))


def _get_live_module(module_path):
    module_name = _file2mod(module_path)
    if module_name not in sys.modules:
        if PY_SYSVER == 2:
            module = imp.load_source(module_name, module_path)
        else:
            module = importlib.import_module(module_name)
    module = sys.modules[module_name]
    return module


if __name__ == '__main__':
    main()

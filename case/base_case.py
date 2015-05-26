from lib.base_lib import BaseClient
from common import utils
import threading


class BaseCase(object):

    def __init__(self):
        self._udid_list = utils.get_device_udids()
        self._clients = [BaseClient(udid) for udid in self._udid_list]
        self._open_apps()

    def _open_apps(self):
        reenter_thread_list = [threading.Thread(target=client.open_app) for client in self._clients]
        for reenter_thread in reenter_thread_list:
            reenter_thread.start()
        for reenter_thread in reenter_thread_list:
            reenter_thread.join()

    def _set_up(self):
        pass

    def _tear_down(self):
        pass

base_case = BaseCase()
print(123)
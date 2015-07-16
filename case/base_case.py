from lib.base_lib import BaseClient
from common import utils
import threading
import os


class BaseCase(object):

    def __init__(self):
        self._device_id_list = utils.get_device_ids()
        self._clients = [BaseClient(device_id) for device_id in self._device_id_list]
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

    def _stop_logcat(self):
        for device_id in self._device_id_list:
            os.system("ps -e | grep %s | xargs kill" % device_id)

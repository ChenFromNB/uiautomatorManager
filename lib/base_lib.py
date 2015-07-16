from uiautomator import Device
from common import utils
from uiautomator import Adb
import threading
import os


class BaseClient(object):

    def __init__(self, device_id):
        self.device_id = device_id
        self._adb_commander = Adb(self.device_id)
        self._logcat_thread = threading.Thread(target=self._start_logcat)
        self._logcat_thread.start()
        self._device = Device(self.device_id)

    def open_app(self):
        self._device.screen.on()
        for i in range(4):
            self._device.press('back')
        _package_name, _main_activity_name = utils.get_package_and_main_activity_name()
        self._adb_commander.cmd('shell am start -W %s/%s' % (_package_name, _main_activity_name))

    def _start_logcat(self):
        log_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'log'))
        self._adb_commander.cmd('logcat -c' % self.device_id)
        self._adb_commander.cmd('logcat> %s/%s.log' % (log_file_path, self.device_id))

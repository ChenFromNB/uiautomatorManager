from uiautomator import Device
from common import utils
from uiautomator import Adb
import threading
import os
import sys


class BaseClient(object):

    def __init__(self, udid):
        self.udid = udid
        self._adb_commander = Adb(self.udid)
        self._logcat_thread = threading.Thread(target=self._start_logcat)
        self._logcat_thread.start()
        self._device = Device(self.udid)

    def open_app(self):
        self._device.screen.on()
        for i in range(4):
            self._device.press('back')
        _package_name, _main_activity_name = utils.get_package_and_main_activity_name()
        self._adb_commander.cmd('shell am start -W %s/%s' % (_package_name, _main_activity_name))

    def _start_logcat(self):
        log_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'log'))
        self._adb_commander.cmd('-s %s logcat -c' % self.udid)
        self._adb_commander.cmd('-s %s logcat> %s/%s.log' % (self.udid, log_file_path, self.udid))

    def __del__(self):
        sys.stdout = os.devnull
        pid_name = ("adb -s %s logcat" % self.udid)
        os.system('ps -e | grep %s | xargs kill' % pid_name)
        sys.stdout = sys.__stdout__

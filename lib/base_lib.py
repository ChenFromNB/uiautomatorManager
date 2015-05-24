from uiautomator import Device
from common import utils
from uiautomator import Adb
import threading
import os


class BaseClient(object):

    def __init__(self, udid):
        self.udid = udid
        self._adb_commander = Adb(self.udid)
        self._logcat_thread = threading.Thread(target=self._start_logcat)
        self._logcat_thread.start()
        self._device = Device(self.udid)
        # self._logcat = LogcatThread(self.udid)
        # self._logcat.start()

    def open_app(self):
        self._device.screen.on()
        for i in range(4):
            self._device.press('back')
        _package_name, _main_activity_name = utils.get_package_and_main_activity_name()
        self._adb_commander.cmd('shell am start -W %s/%s' % (_package_name, _main_activity_name))

    def _start_logcat(self):
        log_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'log'))
        self._adb_commander.cmd('logcat -s %s -c' % self.udid)
        self._adb_commander.cmd('logcat -s %s > %s/%s.log' % (self.udid, log_file_path, self.udid))

    def __del__(self):
        pid_name = "adb logcat"
        os.system("pkill %s" % pid_name)


class LogcatThread(threading.Thread):
    def __init__(self, udid):
        threading.Thread.__init__(self)
        self.udid = udid
        self.daemon = True

    def run(self):
        _adb_commander = Adb(self.udid)
        log_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'log'))
        _adb_commander.cmd('-s %s logcat -c' % self.udid)
        _adb_commander.cmd('-s %s logcat > %s/%s.log' % (self.udid, log_file_path, self.udid))

    def stop(self):
        self._is_stopped = True
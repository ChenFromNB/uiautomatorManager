import os
import xml.etree.ElementTree
import subprocess


def get_package_and_main_activity_name():
    config_tree = xml.etree.ElementTree.parse(os.path.abspath(os.path.join(os.path.dirname(__file__), 'config.xml')))
    app_info_node = config_tree.getiterator('DeviceInfo')
    node = app_info_node[0]
    return node.getchildren()[0].text, node.getchildren()[1].text


def get_device_udids():
    command_output_string = subprocess.check_output(["adb", "devices"]).decode('UTF8').strip()
    return [udid.split('\t')[0] for udid in command_output_string.splitlines()[1:]]
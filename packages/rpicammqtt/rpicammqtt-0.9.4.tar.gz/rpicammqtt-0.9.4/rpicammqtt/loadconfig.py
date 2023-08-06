import yaml
from os.path import expanduser
import sys

config_file_name = 'rpi-cam-mqtt.yaml'

try:
    config_file = "/etc/rpi-cam-mqtt/{}".format(config_file_name)
except:
    try:
        config_file = "{}/.rpi-cam-mqtt/{}".format(expanduser("~"), config_file_name)
    except:
        try:
            config_file = "./config/rpi-cam-mqtt.yaml/{}".format(config_file_name)
        except IOError:
            print("Configuration file not found")
            sys.exit(-1)


def load_config(config_file):
    '''Open config_file and parse the yaml content'''
    try:
        f = open(config_file, 'r')
        conf = yaml.load(f)

    except IOError:
        print("Error: Configuration file can't be opened.")
        sys.exit(-1)
    return conf

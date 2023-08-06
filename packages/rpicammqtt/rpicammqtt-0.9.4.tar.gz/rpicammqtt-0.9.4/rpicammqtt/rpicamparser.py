import json
from rpicammqtt.loadconfig import load_config, config_file
from pkg_resources import resource_string
import logging


class RpiCamParser:
    """Rpi Camera command validator for RPi-Cam-Web-Interface.
    Given a string, it gets checked according to the command list
    in this table https://elinux.org/RPi-Cam-Web-Interface#Pipe.
    The validator uses a type schema defined in data/rpi-cam-info.json.
    The available types are:
      - string
      - list
      - number
      - set
    Other than confirming the type, where possible, constraints are checked:
    ie: if number, check it is between min/max"""

    rpi_cam_cmds = dict()
    curr_cmd_data = None

    def __init__(self):
        c = load_config(config_file)

        numeric_level = logging.getLevelName(c['logging']['level'])
        logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', filename=c['logging']['file'], filemode='w', level=numeric_level)
        self.logger = logging.getLogger(__name__)

        rpi_cam_data_file = resource_string(__name__, '{}/{}'.format(
                                                                        c['data']['path'],
                                                                        c['data']['rpi_cam_file']
                                                                    )).decode('utf-8')

        self.rpi_cam_cmds = json.loads(rpi_cam_data_file)['rpi_cam_cmds']

    def validate(self, cmdstring):
        valid = False
        self.logger.debug("Validating string command \"{}\"".format(cmdstring))

        if type(cmdstring) == str:
            # Expecting string command like:
            # cc <val> [<val> ...]
            # where cc is a two char command followed by one or more val strings separated by space
            # Check rpi-cam-info.json
            cmd_list = cmdstring.strip().split()
            cmd = cmd_list[0]       # First val is the command
            cmd_values = cmd_list[1:]   # From second val, args of command

            if cmd in self.rpi_cam_cmds and len(cmd_values) > 0:
                # when command recognized and
                # when there is at least one argument

                self.curr_cmd_data = self.rpi_cam_cmds[cmd]
                expected_type = self.curr_cmd_data['type']['name']
                self.logger.debug("Command \"{}\" is of type {}".format(cmd, expected_type))

                if expected_type == 'string':
                    valid = self._cmd_string(cmd_values)
                if expected_type == 'list':
                    valid = self._cmd_list(cmd_values)
                if expected_type == 'number':
                    valid = self._cmd_number(cmd_values)
                if expected_type == 'set':
                    valid = self._cmd_set(cmd_values)
            else:
                self.logger.debug("Command {} not found in command template definitions".format(cmd))
        return valid

    def _cmd_string(self, cmd_values):
        '''Not much to do. Leaving def here for future additional checks'''
        self.logger.debug("Running validation for STRING: {}".format(cmd_values))
        return True

    def _cmd_list(self, cmd_values):
        '''check it is a list and the number of elements is higher than min and less than max'''
        ret = False
        self.logger.debug("Running validation for LIST: {}".format(cmd_values))
        nvals = len(cmd_values)
        (min, max) = self.curr_cmd_data['type']['length']
        if nvals >= min and nvals <= max:
            ret = True
        return ret

    def _cmd_number(self, cmd_values):
        '''check it is a number in the range'''
        ret = False
        first_val = cmd_values[0]  # ignoring any extra value
        self.logger.debug("Running validation for NUMBER: {}".format(first_val))
        try:
            numericval = int(first_val)
            self.logger.debug("The value {} is an integer".format(numericval))
        except ValueError:
            self.logger.debug("Value in {}, \"{}\", is not an integer".format(cmd_values, numericval))
            try:
                numericval = float(first_val)
            except ValueError:
                self.logger.debug("Value in {}, \"{}\", is neither an integer or a float".format(cmd_values, numericval))
                numericval = None

        # If we have a number, check it is in the expected range
        if numericval is not None:
            (min, max) = self.curr_cmd_data['type']['range']
            self.logger.debug("Value {} is a number. Checking if it is between {}-{}".format(numericval, min, max))
            if (min is None or numericval >= min) and (max is None or numericval <= max):
                self.logger.debug("Value {} is a valid number".format(numericval))
                ret = True
        return ret

    def _cmd_set(self, cmd_values):
        '''check the keyword is in the set'''
        ret = False
        self.logger.debug("Running validation for SET: {}".format(cmd_values))
        keyword = cmd_values[0] # Ignoring any keys other than the first
        if keyword in self.curr_cmd_data['type']['keywords']:
            ret = True
        return ret

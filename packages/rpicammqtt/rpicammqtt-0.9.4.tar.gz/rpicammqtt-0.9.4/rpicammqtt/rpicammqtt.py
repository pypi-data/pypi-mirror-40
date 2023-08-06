import paho.mqtt.client as pahomqtt
from rpicammqtt.rpicamparser import RpiCamParser
from rpicammqtt.loadconfig import load_config, config_file
import time
import logging
import json

DEFAULT_RPICAM_STATUS = 'Unknown'

class RpiCamMqtt(pahomqtt.Client):
    rpicam_status = DEFAULT_RPICAM_STATUS
    loopdelay = 0.5 # Delays the main loop to reduce CPU load, for reference:
                    # 0.0 -> 30% CPU, 0.1 -> 6-8% CPU, 0.5 -> 2-3%, 1.0 -> 1-2%
    connected = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        c = load_config(config_file)

        numeric_level = logging.getLevelName(c['logging']['level'])
        logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', filename=c['logging']['file'], filemode='w', level=numeric_level)
        self.logger = logging.getLogger(__name__)

        self.mqtt_server = c['mqtt']['server']
        self.mqtt_port = c['mqtt']['port']
        self.mqtt_user = c['mqtt']['user']
        self.mqtt_pw = c['mqtt']['pw']
        self.mqtt_qos = c['mqtt']['qos']
        self.mqtt_keepalive = c['mqtt']['keepalive']

        self.status_topic = c['mqtt']['topic']['status'].format(c['rpiname'])
        self.cmd_topic = c['mqtt']['topic']['base'].format(c['rpiname'])
        self.pt_topic = c['mqtt']['topic']['pantilt'].format(c['rpiname'])
        self.ptviews_topic = c['mqtt']['topic']['ptviews'].format(c['rpiname'])

        self.rpicam_fifofile = c['rpicam']['fifofile']
        self.rpicam_statusfile = c['rpicam']['statusfile']

        self.pantilt_enabled = c['pantilt']['enabled']
        if self.pantilt_enabled:
            self._init_pantilt(c)

        # Init RpiCamParser to validate commands received from an mqtt topic
        self.rpip = RpiCamParser()

        # Connect to the MQTT server
        self.username_pw_set(self.mqtt_user, password=self.mqtt_pw)
        self.will_set(self.status_topic, payload="Unknown", qos=self.mqtt_qos, retain=True)
        self.connect(self.mqtt_server, self.mqtt_port, self.mqtt_keepalive)

    def _init_pantilt(self, config):
        """Load pantilt module and init pt config"""
        try:
            from rpicammqtt.pantilt import PanTilt
        except ImportError as err:
            self.logger.error("PanTilt library can't be imported: {}".format(err))
        pt_conf = config['pantilt']['config_file']
        pan_ch = config['pantilt']['pan_pwm_ch']
        tilt_ch = config['pantilt']['tilt_pwm_ch']
        self.pantilt = PanTilt(pan_ch, tilt_ch, pt_conf)

        # If configured, load camera views as pan/tilt coordinates
        self.pt_views = dict()
        if 'views' in config['pantilt']:
            self.pt_views = config['pantilt']['views']

    def _get_rpicam_status(self):
        """Read the camera status from /dev/shm/mjpeg/status_mjpeg.txt"""
        try:
            f = open(self.rpicam_statusfile, 'r')
            return f.readline()
        except IOError as err:
            self.logger.error("Error: Status file IO error: {}".format(err))
            return err

    def _set_rpicam_command(self, command):
        """Write a command to the camera FIFO"""
        try:
            self.logger.info("Setting command {} to FIFO file {}".format(command, self.rpicam_fifofile))
            with open(self.rpicam_fifofile, 'w') as fifo:
                fifo.write(command)
                fifo.close()
            return True
        except IOError as err:
            self.logger.error("Error: FIFO file IO error: {}".format(err))
            return err

    def _validate_and_run_rpicam_command(self, mqttcmd):
        """validate a command from mqtt and run it"""
        ret = False
        valid = self.rpip.validate(mqttcmd)
        self.logger.info("New mqtt command received: {}(Valid={})".format(mqttcmd, valid))

        if valid:  # in case of invalid cmd nothing gets executed
            ret = self._set_rpicam_command(mqttcmd)
        else:
            self.logger.warning("Invalid command ({}). Nothing will be executed".format(mqttcmd))
        return ret

    def _get_pt_and_run_servos(self, mqtt_pt_json):
        """Get the message as json and run the pan/tilt servos"""
        ret = False
        if self.pantilt_enabled:
            pan = None
            tilt = None
            view = None
            try:
                pt_cmd = json.loads(mqtt_pt_json)
                if 'pan' in pt_cmd:
                    pan = pt_cmd['pan']
                if 'tilt' in pt_cmd:
                    tilt = pt_cmd['tilt']
                if 'view' in pt_cmd:
                    view = pt_cmd['view']
                    if view in self.pt_views:
                        pan = self.pt_views[view][0]
                        tilt = self.pt_views[view][1]
                self.pantilt.point(pan, tilt)
                self.logger.info("Pan/Tilt command run ({}, {}), view: {}".format(pan, tilt, view))
                ret = True
            except ValueError as err:
                self.logger.error("pantilt payload can't be loaded as json: {}".format(err))
                ret = err
        else:
            self.logger.warning("PanTilt disabled in the configuration")
        return ret

    def on_connect(self, client, userdata, flags, rc):
        """When connected subscribe to receive commands and publish views"""
        self.logger.info("Started. Connected to mqtt server {}".format(self.mqtt_server))
        self.connected = True   # Tracking connection status

        # Publish view list if pantilt enabled and if some views are configured
        if self.pantilt_enabled and len(self.pt_views) > 0:
            view_keys = [*self.pt_views]  # Only the view names get published, not the pan tilt values
            pt_views_dump = json.dumps(view_keys)
            self.publish(
                self.ptviews_topic,
                payload='{}'.format(pt_views_dump),
                qos=self.mqtt_qos,
                retain=True
            )
            self.logger.info("Found pan/tilt views configured: {}".format(pt_views_dump))

        # Subscribe to receive commands
        client.subscribe([(self.cmd_topic, self.mqtt_qos), (self.pt_topic, self.mqtt_qos)])

    def on_disconnect(self, client, userdata, rc=0):
        # The value of rc indicates success or not:
        # 0: Connection successful
        # 1: Connection refused - incorrect protocol version
        # 2: Connection refused - invalid client identifier
        # 3: Connection refused - server unavailable
        # 4: Connection refused - bad username or password
        # 5: Connection refused - not authorised
        # 6 - 255: Currently unused.
        self.connected = False
        self.rpicam_status = DEFAULT_RPICAM_STATUS  # When connection lost (ie: mqtt server down) reset camera status
        self.logger.debug("Disconnected. Code {}".format(rc))

    def on_message(self, client, userdata, msg):
        """When a message is received, parse it and run the command locally"""
        mqttcmd = msg.payload.decode()
        self.logger.debug("Received msg {}. Topic {}".format(msg.payload, msg.topic))
        if msg.topic == self.cmd_topic:
            ret = self._validate_and_run_rpicam_command(mqttcmd)
            if ret is not True:
                self.logger.error("Error: _set_rpicam_command failed to write {} to fifo".format(mqttcmd))
        if msg.topic == self.pt_topic:
            self._get_pt_and_run_servos(mqttcmd)

    def rpicammqtt_loop(self):
        """Start the mqtt loop and check for status changes"""

        # Start threaded interface to the network loop
        self.loop_start()

        # Keep the camera status monitored and re-publish when it changes
        while True:
            if self.connected:
                new_rpicam_status = self._get_rpicam_status()
                if new_rpicam_status != self.rpicam_status:
                    self.logger.info("Status changed {}".format(new_rpicam_status))
                    self.rpicam_status = new_rpicam_status
                    # Check status and publish it
                    self.publish(
                        self.status_topic,
                        payload='{}'.format(self.rpicam_status),
                        qos=self.mqtt_qos,
                        retain=True
                    )

            time.sleep(self.loopdelay)

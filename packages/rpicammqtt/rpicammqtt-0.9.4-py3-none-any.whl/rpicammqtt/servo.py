from __future__ import division
import yaml

# Import the PCA9685 module.
import Adafruit_PCA9685


class Servo:
    freq = None
    p = None

    def __init__(self, config_file, ch=0):
        try:
            f = open(config_file, 'r')
            self.config = yaml.load(f)
        except IOError:
            print("Error: Configuration file can't be opened.")

        self.set_channel(ch)
        self.pos = self.get_neutral_pos()
        self.p = Adafruit_PCA9685.PCA9685()
        self.p.set_pwm_freq(self.config['freq'])

    # Helper function to make setting a servo pulse width simpler.
    def set_servo_pulse(self, channel, pulse):
        pulse_length = 1000000  # 1,000,000 us per second
        pulse_length //= 60  # 60 Hz
        print('{0}us per period'.format(pulse_length))
        pulse_length //= 4096  # 12 bits of resolution
        print('{0}us per bit'.format(pulse_length))
        pulse *= 1000
        pulse //= pulse_length
        self.p.set_pwm(channel, 0, pulse)

    def reset_position(self):
        self.set_position(self.get_neutral_pos())

    # Set a given value (position) for the servo and return the actual updated value
    def set_position(self, position):
        self.pos = position
        if position < self.min_pos:
            self.pos = self.min_pos
        elif position > self.max_pos:
            self.pos = self.max_pos
        # print("New value set {} range({}-{})".format(self.pos, self.min_pos, self.max_pos))
        self.p.set_pwm(self.channel, 0, self.pos)
        return self.pos

    def set_position_smooth(self, position):
        pass

    # Set channel to use and load its settings
    def set_channel(self, ch):
        self.channel = ch
        self.min_pos = self.config['channel'][self.channel]['minp']
        self.max_pos = self.config['channel'][self.channel]['maxp']

    # Increase number of steps the current position
    def step_position(self, steps):
        self.pos += steps
        self.set_position(self.pos)

    # Load servo config
    def get_servo_conf(self):
        return self.config['channel'][self.channel]

    # Get current position
    def get_current_pos(self):
        return self.pos

    # Get neutral position
    def get_neutral_pos(self):
        return int(self.min_pos + ((self.max_pos - self.min_pos) / 2))


from rpicammqtt.servo import Servo


class PanTilt:
    def __init__(self, pan_ch, tilt_ch, config):
        self.pan = Servo(config, ch=pan_ch)
        self.tilt = Servo(config, ch=tilt_ch)
        
    def point(self, p=None, t=None):
        """Set one of pan or tilt or both"""
        if p is not None:
            self.pan.set_position(p)
        if t is not None:
            self.tilt.set_position(t)
        
    def pt_neutral(self):
        self.pan.reset_position()
        self.tilt.reset_position()


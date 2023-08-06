#!/usr/bin/env python3
from rpicammqtt.rpicammqtt import RpiCamMqtt

def main():
    rcm = RpiCamMqtt()
    rcm.rpicammqtt_loop()


if __name__ == "__main__":
    main()
import curses
from rpicammqtt.loadconfig import load_config, config_file
from rpicammqtt.servo import Servo
import sys


def main():
    conf = load_config(config_file)

    if conf['pantilt']['enabled']:
        x_channel = conf['pantilt']['pan_pwm_ch']
        y_channel = conf['pantilt']['tilt_pwm_ch']
        pantilt_config = conf['pantilt']['config_file']
    else:
        sys.exit("ERROR: pantilt not configured. Review {}".format(config_file))


    x = Servo(pantilt_config, x_channel)      # Head Tilt
    y = Servo(pantilt_config, y_channel)      # Head Pan

    xv = x.get_neutral_pos()
    yv = y.get_neutral_pos()

    x.set_position(xv)
    y.set_position(yv)

    stepvalue = 5

    # CURSES INIT
    screen = curses.initscr()
    curses.noecho()
    curses.curs_set(0)
    screen.keypad(1)

    screen.addstr(2, 1, "Pan:")
    screen.addstr(2, 10, str(xv))
    screen.addstr(2, 16, "Tilt:")
    screen.addstr(2, 26, str(yv))

    while True:
        event = screen.getch()
        if event == ord("q"):
            break
        elif event == curses.KEY_LEFT:
            xv += stepvalue
            xv = x.set_position(xv)
            screen.addstr(2, 10, str(xv))
        elif event == curses.KEY_RIGHT:
            xv -= stepvalue
            xv = x.set_position(xv)
            screen.addstr(2, 10, str(xv))
        elif event == curses.KEY_DOWN:
            yv += stepvalue
            yv = y.set_position(yv)
            screen.addstr(2, 26, str(yv))
        elif event == curses.KEY_UP:
            yv -= stepvalue
            yv = y.set_position(yv)
            screen.addstr(2, 26, str(yv))


    curses.endwin()

if __name__ == "__main__":
    main()

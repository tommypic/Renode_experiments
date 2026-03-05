# -*- coding: utf-8 -*-
import os
from Antmicro.Renode.Core import EmulationManager

pipe_path = "/home/tom/Renode_experiments/python_log_scripts/led_status_pipe"

try:
    # Use os.open with O_NONBLOCK to prevent blocking if there is no reader
    fd = os.open(pipe_path, os.O_WRONLY | os.O_NONBLOCK)
    pipe = os.fdopen(fd, "a")
except OSError:
    print("Could not open LED pipe (non-blocking). Is it created and has a reader?")
    pipe = None
except Exception as e:
    print("Could not open LED pipe: {}. Is it created?".format(e))
    pipe = None


def led_logger(sender, value):
    try:
        machine_obj = sender.GetMachine()

        time_str = str(machine_obj.ElapsedVirtualTime)

        status = "ON " if value else "OFF"

        # Write to the pipe
        pipe.write("[{}] LED STATUS: {}\n".format(time_str, status))
        pipe.flush()

    except Exception as e:
        # Using the monitor to print errors helps with debugging
        print("Logging error to pipe: {}".format(e))


led_device = self.Machine["sysbus.gpioPortD.UserLED"]
led_device.StateChanged += led_logger

print("Python Monitor redirected to led_status_pipe.")

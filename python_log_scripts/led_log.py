# -*- coding: utf-8 -*-
import System.IO
import threading
from Antmicro.Renode.Core import EmulationManager

pipe_path = "/home/tom/Renode_experiments/python_log_scripts/led_status_pipe"

pipe = None
def open_pipe_threaded():
    global pipe
    try:
        # Blocks the thread until a reader is ready
        stream = System.IO.File.Open(pipe_path, System.IO.FileMode.Open, System.IO.FileAccess.Write, System.IO.FileShare.ReadWrite)
        pipe = System.IO.StreamWriter(stream)
        pipe.AutoFlush = True
        print("LED pipe connected.")
    except:
        pass

# Initial attempt to connect in background
t = threading.Thread(target=open_pipe_threaded)
t.daemon = True
t.start()

def led_logger(sender, value):
    global pipe
    if not pipe:
        return
        
    try:
        machine_obj = sender.GetMachine()
        time_str = str(machine_obj.ElapsedVirtualTime)
        status = "ON " if value else "OFF"
        
        # Write to the pipe using .NET StreamWriter method
        pipe.WriteLine("[{}] LED STATUS: {}".format(time_str, status))

    except Exception:
        # Broken pipe (reader closed)
        pipe = None
        print("LED pipe disconnected. Waiting for new reader in background...")
        t_reconnect = threading.Thread(target=open_pipe_threaded)
        t_reconnect.daemon = True
        t_reconnect.start()


led_device = self.Machine["sysbus.gpioPortD.UserLED"]
led_device.StateChanged += led_logger

print("Python Monitor redirected to led_status_pipe.")

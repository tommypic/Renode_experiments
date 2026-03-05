using System;
using System.Collections.Generic;
using Antmicro.Renode.Peripherals.I2C;
using Antmicro.Renode.Logging;
using Antmicro.Renode.Core;

namespace Antmicro.Renode.Peripherals.Sensors
{
    public class MyI2CDistanceSensor : II2CPeripheral
    {
        public int Distance { get; set; }

        public void Write(byte[] data)
        {
            this.Log(LogLevel.Noisy, "Received I2C write of length {0}", data.Length);
        }

        public byte[] Read(int count)
        {
            this.Log(LogLevel.Noisy, "I2C read request for {0} bytes. Distance is {1}", count, Distance);
            var result = new byte[count];
            if (count > 0) result[0] = (byte)(Distance & 0xFF);
            if (count > 1) result[1] = (byte)((Distance >> 8) & 0xFF);
            return result;
        }

        public void FinishTransmission()
        {
            // This method is called when an I2C transaction ends
            this.Log(LogLevel.Noisy, "I2C transmission finished");
        }

        public void Reset()
        {
            Distance = 1000;
        }

        public void Dispose()
        {
        }
    }
}

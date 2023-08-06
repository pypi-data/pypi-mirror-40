from mh_z19b.common import SensorMixin
import serial

class Sensor(SensorMixin):
  def __init__(self, **kwargs):
    super(Sensor, self).__init__(serial.Serial(**kwargs))

  def send_request(self, payload, *args):
    data = self._prepare_request(payload, *args)
    return self.serial.write(data)

  def send_receive(self, command, *args):
    self.serial.read(self.serial.in_waiting)  # flush all data in input buffer
    self.send_request(command, *args)
    return self.parse_response(self.serial.read(9))

  def read_metric(self):
    return self.send_receive(self.READ_METRIC)

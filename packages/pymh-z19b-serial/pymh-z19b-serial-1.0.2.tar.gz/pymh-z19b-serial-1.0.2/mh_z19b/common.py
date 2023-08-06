import typing


class SensorMixin(object):
  READ_METRIC = b'\xFF\x01\x86\x00\x00\x00\x00\x00'
  START_CALIBRATION = b'\xFF\x01\x87\x00\x00\x00\x00\x00'
  SET_AUTOCALIBRARTION = b'\xFF\x01\x79%c\x00\x00\x13\x88\x00'
  SET_DETECTION_RANGE = b'\xFF\x01\x99\x00\x00\x00\x13\x88\x00'

  def __init__(self, serial):
    self.serial = serial

  def _prepare_request(self, payload, *args):
    assert len(payload) == 8
    assert isinstance(payload, typing.ByteString)
    payload = payload % tuple(*args)

    csum = self._checksum(payload)
    data = payload + csum
    assert len(data) == 9

    return data

  @staticmethod
  def _checksum(payload):
    checksum = sum(bytearray(payload[0:8]))
    checksum = 0xff - checksum & 0xff

    return bytes([checksum])

  def parse_response(self, payload):
      if payload[0] == 0xff:
          if payload[1] == 0x86:  # Read command
              co2 = (payload[2]<<8)+payload[3]
              return co2

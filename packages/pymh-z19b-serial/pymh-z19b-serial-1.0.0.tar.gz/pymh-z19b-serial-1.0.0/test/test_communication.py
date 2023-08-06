from mh_z19b.async import Sensor

def test_checksum():
    payload = b'\xFF\x01\x86\x00\x00\x00\x00\x00'

    assert Sensor._checksum(payload) == b'\x79'

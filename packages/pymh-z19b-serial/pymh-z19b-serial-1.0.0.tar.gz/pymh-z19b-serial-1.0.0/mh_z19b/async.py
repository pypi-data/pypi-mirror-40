import asyncio
import serial_asyncio

from mh_z19b.common import SensorMixin


class Sensor(SensorMixin):
    def __init__(self, ioloop = None):
        if ioloop is not None:
            self.loop = ioloop
        else:
            self.loop = asyncio.get_event_loop()

    async def open_serial(self, **kwargs):
        (self.reader, self.writer) = await serial_asyncio.open_serial_connection(loop=self.loop, **kwargs)

    def send_request(self, payload, *args):
        data = self._prepare_request(payload, *args)
        return self.writer.write(data)

    async def read_metric(self):
        return await self.send_receive(self.READ_METRIC)

    async def send_receive(self, command, *args):
        self.send_request(command, *args)
        response = await self.reader.readexactly(9)
        return self.parse_response(response)

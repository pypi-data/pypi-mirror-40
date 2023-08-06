===================================================
 MH_Z19B CO2 Sensor Serial interface |build-status|
===================================================

This package is ment to be used to read data from MH_Z19B CO2 Sensor via serial. Sensor can be bought on AliExpress for around 18€ (Jan 2019)

It is recommended to disable Auto calibration and set measuring range to 5000 to get adequate readings after first day of use.

Requirements:
==============

You need a USB to TTL adapter to read data from the sensor. I use Prolific Technology PL2303 adapter plugged into my router.
Router runs a python script with this library that reads metrics periodically and sends it via MQTT.

Python 3.5+

Installation:
==============

.. code-block:: shell

    pip3 install pymh-z19b-serial

Library Usage examples:
========================

It is possible to use sync and async way to read from the sensor

Sync
-----

Uses `pyserial`

.. code-block:: python

    from mh_z19b.sync import Sensor

    sensor = Sensor(port='/dev/cu.usbserial', baudrate=9600)
    print(sensor.read_metric())


Async
------

Uses `asyncio` and `pyserial-asyncio`

.. code-block:: python

    import asyncio

    from mh_z19b.async import Sensor

    async def run(loop):
        sensor = Sensor(loop)
        await sensor.open_serial(url='/dev/cu.usbserial', baudrate=9600)
        data = await sensor.read_metric()
        print(data)

    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    loop.run_until_complete(run(loop))
    loop.close()



.. |build-status| image:: https://travis-ci.org/yozik04/pymh-z19b.svg?branch=master
   :target: https://travis-ci.org/yozik04/pymh-z19b
   :alt: Build status

#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of CSTBox.
#
# CSTBox is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# CSTBox is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with CSTBox.  If not, see <http://www.gnu.org/licenses/>.

""" HAL interface classes for LCJ supported products. """

import logging
import time

from pycstbox.hal.network_nmea import NMEADevice
from pycstbox.lcj.cv7v import CV7VDevice
from pycstbox.hal import hal_device

_logger = logging.getLogger('lcj')

DEFAULT_PRECISION = 3


@hal_device(device_type="lcj.cv7v", coordinator_type="serial-nmea")
class CV7V(NMEADevice):
    """ HAL device modeling the CV7-V Wind Sensor.

    Specific configuration attributes:

        min_speed:
            minimal wind speed (m/s) for considering it is not null

        values_ttl:
            output values time to live (in secs).
            A new value is taken in account only if the previous one is older
            that this delay.
    """
    DEVICE_TYPE = 'lcj.cv7v'

    def __init__(self, coord, cfg):
        super(CV7V, self).__init__(coord, cfg)
        self._hwdev = CV7VDevice()
        self._sentence_ages = {}
        # ensure configuration parameters are of the right types
        for attr in ['min_speed', 'values_ttl']:
            setattr(self._cfg, attr, float(getattr(self._cfg, attr)))

    def process_sentence(self, sentence):
        last_seen = self._sentence_ages.get(sentence.formatter, 0)
        now = time.time()
        if now - last_seen < self._cfg.values_ttl:
            return None

        self._sentence_ages[sentence.formatter] = now

        handled = False
        try:
            handled = self._hwdev.process_sentence(sentence)
        except ValueError as e:
            _logger.error(e)
        except Exception as e:
            _logger.exception(e)

        if handled:
            w_speed, w_dir, w_temp = self._hwdev.get_outputs()
            # filter data when (quasi) no wind
            if w_speed < self._cfg.min_speed:
                w_speed = 0
                w_dir = None
            return CV7VDevice.OutputValues(w_speed, w_dir, w_temp)
        else:
            return None

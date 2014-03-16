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

""" LCJ CV7-V Ultrasonic Wind Sensor.

This modules provides a class modeling the LCJ CV7-V ultrasonic wind sensor
by processing incomming NMEA sentences produced by the equipment and latching
them as a multiple outputs sensor.

It is fully decoupled from the CSTBox architecture.
"""

__author__ = 'Eric PASCUAL - CSTB (eric.pascual@cstb.fr)'
__copyright__ = 'Copyright (c) 2013 CSTB'
__vcs_id__ = '$Id$'
__version__ = '1.0.0'

from collections import namedtuple

# xx to m/s conversion ratios
_speed_conversion_ratio = {
    'N' : 0.5144,           # knots
    'M' : 1,                # m/s
    'K' : 1000.0/3600.0     # km/h
}

class CV7VDevice(object):
    """ Model of the CV7-V wind sensor.

    It presents the device as a multiple outputs sensor, providing :

        - the wind speed (in m/s)
        - the wind temperature (in degC)
        - the wind relative direction (in angular degrees)
    """

    _wind_speed = _wind_temp = _wind_dir = 0

    OutputValues = namedtuple('OutputValues', [
        'wind_speed',    # wind speed
        'wind_dir',      # wind relative direction
        'wind_temp'      # wind temperature
    ])

    def get_outputs(self):
        return self.OutputValues(
            self._wind_speed,
            self._wind_dir,
            self._wind_temp
        )

    def process_sentence(self, sentence):
        """ Process an incomming NMEA sentence.

        Recognized sentences are used to update the latched values, other ones
        are discarded.

        :param str sentence: the NMEA sentence, passed as a pycstbox.nmea.NMEASentence instance

        :returns bool: True if the sentence is supported, False otherwise
        """
        if sentence.formatter == 'IIMWV':
            self._wind_dir = float(sentence.fields[0])

            # gets the wind speed and converts it in m/s, depending on
            # the units used in the sentence
            units = sentence.fields[3]
            try:
                ratio = _speed_conversion_ratio[units]
                self._wind_speed = float(sentence.fields[2]) * ratio
            except KeyError:
                raise ValueError(
                    'invalid speed units (%s) in sentence %s' % (units, sentence)
                )

        elif sentence.formatter == 'WIXDR':
            self._wind_temp = float(sentence.fields[1])

            units = sentence.fields[2]
            if units == 'F':
                self._wind_temp = (self._wind_temp - 32.0) * 5.0 / 9.0
            elif units != 'C':
                raise ValueError(
                    'invalid temperature units (%s) in sentence %s' % (units, sentence)
                )

        else:
            return False

        return True


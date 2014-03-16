#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import cv7v
from pycstbox.nmea import NMEASentence

class TestCV7V(unittest.TestCase):
    def setUp(self):
        self.cv7v = cv7v.CV7V()

    def testValidWindSentence(self):
        sentence = NMEASentence('$IIMWV,225.0,R,1.0,M,A')

        ok = self.cv7v.process_sentence(sentence)

        self.assertTrue(ok, 'valid sentence not recognized')
        self.assertEquals(self.cv7v.wind_dir, 225.0, 'invalid wind direction')
        self.assertEquals(self.cv7v.wind_speed, 1.0, 'invalid wind speed')

    def testValidTempSequence(self):
        sentence = NMEASentence('$WIXDR,C,22.0,C,,')

        ok = self.cv7v.process_sentence(sentence)

        self.assertTrue(ok, 'valid sentence not recognized')
        self.assertEquals(self.cv7v.wind_temp, 22.0, 'invalid wind temperature')

    def testSpeedConversions(self):
        sentence = NMEASentence('$IIMWV,225.0,R,1.0,K,A')
        ok = self.cv7v.process_sentence(sentence)
        self.assertTrue(ok, 'valid sentence not recognized')
        self.assertEquals(self.cv7v.wind_speed, 1000.0/3600, 'invalid km/h conversion')

        sentence = NMEASentence('$IIMWV,225.0,R,1.0,N,A')
        ok = self.cv7v.process_sentence(sentence)
        self.assertTrue(ok, 'valid sentence not recognized')
        self.assertEquals(self.cv7v.wind_speed, 0.5144, 'invalid knots conversion')

    def testTemperatureConversions(self):
        sentence = NMEASentence('$WIXDR,C,59.0,F,,')
        ok = self.cv7v.process_sentence(sentence)
        self.assertTrue(ok, 'valid sentence not recognized')
        self.assertEquals(self.cv7v.wind_temp, 15.0, 'invalid temperature conversion')

    def testUnsupportedSentences(self):
        sentence = NMEASentence('$PLCJ,5801,5F01,AA,4253,3341')
        ok = self.cv7v.process_sentence(sentence)
        self.assertFalse(ok, 'unsupported sentence accepted')

        sentence = NMEASentence('$PLCJEA870,6D98,C500,0056,AC,')
        ok = self.cv7v.process_sentence(sentence)
        self.assertFalse(ok, 'unsupported sentence accepted')


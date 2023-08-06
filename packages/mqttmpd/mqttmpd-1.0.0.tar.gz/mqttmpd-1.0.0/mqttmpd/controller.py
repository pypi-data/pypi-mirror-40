#! /usr/bin/env python
# -*- coding:utf8 -*-
#
# controller.py
#
# Copyright © 2019 Mathieu Gaborit (matael) <mathieu@matael.org>
#
# Licensed under the "THE BEER-WARE LICENSE" (Revision 42):
# Mathieu (matael) Gaborit wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy me a beer or coffee in return
#

import os
import logging
import socket

import paho.mqtt.client as mqtt
from mpd import MPDClient


class MQTTMPDController(object):

    def __init__(self,
                 mqtt_broker, mqtt_client_id, mqtt_topicbase='music', mqtt_port=1883,
                 mpd_server='localhost', mpd_port=6600):
        self._LOG = MQTTMPDController._get_logger()
        self.mqtt_broker = mqtt_broker
        self.mqtt_client_id = mqtt_client_id
        self.mqtt_topicbase = mqtt_topicbase
        self.mqtt_port = mqtt_port
        self.mpd_server = mpd_server
        self.mpd_port = mpd_port

        self.mqtt_client = None
        self.mpd_client = None
        try:
            self.mqtt_client = self.mqtt_connect()
        except ValueError:
            self._LOG.error('Issues with the MQTT connection')

        self._commands = {
            'getstate': self._funcpublish_statuspart('state'),
            'getvol': self._funcpublish_statuspart('volume'),
            'next': lambda *a, **kw: self.mpd_client.next(),
            'previous': lambda *a, **kw: self.mpd_client.previous(),
            'stop': lambda *a, **kw: self.mpd_client.stop(),
            'play': lambda *a, **kw: self.mpd_client.play(),
            'pause': lambda *a, **kw: self.mpd_client.pause(),
            'toggle': self._toggle_play,
            'setvol': lambda *a, **kw: self.mpd_client.setvol(int(a[0]))
        }

    @classmethod
    def _get_logger(cls):
        return logging.getLogger("MPD MQTT Controller")

    def loop_forever(self):
        self.mqtt_client.loop_forever()

    def mqtt_disconnect(self):
        self.mqtt_client.disconnect()

    def mqtt_connect(self):
        """Try and connect to the MQTT borker or raise a ValueError

        Also, subscribe to self.mqtt_topicbase/control topic
        """
        mqtt_client = mqtt.Client(client_id=self.mqtt_client_id)
        mqtt_client.on_message = self._on_message
        mqtt_client.on_connect = self._on_connect
        mqtt_client.will_set(
            os.path.join(self.mqtt_topicbase, 'status'),
            'offline', retain=True)

        try:
            mqtt_client.connect(self.mqtt_broker, self.mqtt_port)
        except socket.gaierror:
            self._LOG.error('Issue w/ MQTT connection')
            raise IOError('Error while connecting to the MQTT broker.')

        return mqtt_client

    def _mqtt_publish(self, payload):
        self.mqtt_client.publish(
            os.path.join(self.mqtt_topicbase, 'status'),
            payload)

    def _on_connect(self, client, userdata, flags, rc):
        self.mqtt_client.publish(
            os.path.join(self.mqtt_topicbase, 'status'),
            'online', retain=True)
        self.mqtt_client.subscribe(os.path.join(self.mqtt_topicbase, 'control/#'))

    def _on_message(self, client, userdata, msg):
        command_handler = self._commands.get(msg.topic.split('/')[-1])
        if command_handler is not None:
            self.mpd_client = self.mpd_connect()
            command_handler(msg.payload)
            self.mpd_disconnect()

    def mpd_connect(self):
        """Try and connect to the MPD borker or raise a ValueError"""
        mpd_client = MPDClient()
        mpd_client.timeout = 10
        try:
            mpd_client.connect(self.mpd_server, self.mpd_port)
        except socket.gaierror:
            self._LOG.error('Issue w/ MPD connection')
            raise IOError('Error while connecting to the MPD server.')

        return mpd_client

    def mpd_disconnect(self):
        self.mpd_client.close()
        self.mpd_client.disconnect()
        self.mpd_client = None

    def _funcpublish_statuspart(self, part):
        def func(*a, **kw):
            part_value = self.mpd_client.status().get(part)
            if part_value is not None:
                self._mqtt_publish('{}: {}'.format(part, part_value))
        return func

    def _toggle_play(self, *a, **kw):
        state = self.mpd_client.status()['state']
        if state == 'play':
            self.mpd_client.pause()
        else:
            self.mpd_client.play()

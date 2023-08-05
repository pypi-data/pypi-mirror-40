"""
Trace object holds events and metadata
"""

from __future__ import absolute_import, print_function
import sys
import os
import time
import traceback
import warnings
import pprint
import simplejson as json

import requests
import requests.exceptions
from epsagon.event import BaseEvent
from epsagon.common import EpsagonWarning
from .constants import SEND_TIMEOUT, MAX_LABEL_SIZE, __version__


class Trace(object):
    """
    Represents runtime trace
    """

    def __init__(self):
        """
        initialize.
        """

        self.app_name = ''
        self.token = ''
        self.events = []
        self.exceptions = []
        self.custom_labels = {}
        self.custom_labels_size = 0
        self.has_custom_error = False
        self.version = __version__
        self.collector_url = ''
        self.metadata_only = True
        self.use_ssl = False
        self.debug = False
        self.platform = 'Python {}.{}'.format(
            sys.version_info.major,
            sys.version_info.minor
        )

    def add_exception(self, exception, stack_trace, additional_data=''):
        """
        add an exception to the trace
        :param exception: the exception to add
        :param stack_trace: the traceback at the moment of the event
        :param additional_data: a json serializable object that contains
            additional data regarding the exception
        :return: None
        """

        try:
            exception_dict = {
                'type': str(type(exception)),
                'message': str(exception),
                'traceback': stack_trace,
                'time': time.time(),
                'additional_data': additional_data
            }

            self.exceptions.append(exception_dict)
        # Making sure that tracing inner exception won't crash
        # pylint: disable=W0703
        except Exception:
            pass

    def prepare(self):
        """
        Prepares new trace.
        Prints error if token is empty, and empty events list.
        :return: None
        """

        if self.token == '':
            warnings.warn(
                'Epsagon Error: Please initialize token, data won\'t be sent.',
                EpsagonWarning
            )

        self.events = []
        self.exceptions = []
        self.custom_labels = {}
        self.custom_labels_size = 0
        self.has_custom_error = False

    def initialize(self, app_name, token, collector_url, metadata_only,
                   use_ssl, debug):
        """
        Initializes trace with user's data.
        User can configure here trace parameters.
        :param app_name: application name
        :param token: user's token
        :param collector_url: the url to send traces to.
        :param metadata_only: whether to send metadata only or not.
        :param use_ssl: whether to use SSL or not.
        :param debug: debug flag
        :return: None
        """

        self.app_name = app_name
        self.token = token
        self.collector_url = collector_url
        self.metadata_only = metadata_only
        self.use_ssl = use_ssl
        self.debug = debug | (os.environ.get('EPSAGON_DEBUG') == 'TRUE')

    @staticmethod
    def load_from_dict(trace_data):
        """
        Load new trace object from dict.
        :param trace_data: dict data of trace
        :return: Trace
        """

        trace = Trace()
        trace.app_name = trace_data['app_name']
        trace.token = trace_data['token']
        trace.version = trace_data['version']
        trace.platform = trace_data['platform']
        trace.exceptions = trace_data.get('exceptions', [])
        for event in trace_data['events']:
            trace.events.append(BaseEvent.load_from_dict(event))
        return trace

    def add_event(self, event):
        """
        Add event to events list.
        :param event: BaseEvent
        :return: None
        """
        event.terminate()
        self.events.append(event)

    def verify_custom_label(self, key, value):
        """
        Verifies custom label is valid, both in size and type.
        :param key: Key for the label data (string)
        :param value: Value for the label data (string)
        :return: True/False
        """
        if not isinstance(key, str) or not isinstance(value, str):
            return False

        if len(key) + len(value) > MAX_LABEL_SIZE:
            return False

        if (
            len(key) +
            len(value) +
            self.custom_labels_size > MAX_LABEL_SIZE
        ):
            return False

        self.custom_labels_size += len(key) + len(value)

        return True

    def add_label(self, key, value):
        """
        Adds a custom label given by the user to the runner
        of the current trace
        :param key: Key for the label data (string)
        :param value: Value for the label data (string)
        """
        if not self.verify_custom_label(key, value):
            return

        self.custom_labels[key] = value

    def update_runner_with_custom_labels(self):
        """
        Adds the custom labels to the runner of the trace
        """
        if not self.custom_labels:
            return

        index, runner = [
            (index, ev) for (index, ev) in enumerate(self.events)
            if ev.origin == 'runner'
        ][0]

        runner.resource['metadata']['labels'] = json.dumps(self.custom_labels)

        self.events[index] = runner

    def to_dict(self):
        """
        Convert trace to dict.
        :return: Trace dict
        """

        try:
            self.update_runner_with_custom_labels()
        # pylint: disable=W0703
        except Exception as exception:
            # Ignore custom logs in case of error.
            tracer.add_exception(
                exception,
                traceback.format_exc()
            )

        return {
            'token': self.token,
            'app_name': self.app_name,
            'events': [event.to_dict() for event in self.events],
            'exceptions': self.exceptions,
            'version': self.version,
            'platform': self.platform,
        }

    # pylint: disable=W0703
    def send_traces(self):
        """
        Send trace to collector.
        :return: None
        """
        if self.token == '':
            return
        try:
            requests.post(
                self.collector_url,
                data=json.dumps(self.to_dict()),
                timeout=SEND_TIMEOUT
            )
            if self.debug:
                print("Sending traces:")
                pprint.pprint(self.to_dict())
        except requests.exceptions.ReadTimeout as exception:
            if self.debug:
                print("Failed to send traces (timeout): ", exception)
        except Exception as exception:
            if self.debug:
                print("Failed to send traces: ", exception)


# pylint: disable=C0103
tracer = Trace()

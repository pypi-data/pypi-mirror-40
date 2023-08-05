# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .base import BaseYarnAPI
from .constants import YarnApplicationState
from .errors import IllegalArgumentError
from .hadoop_conf import get_jobhistory_host_port


class TimelineServer(BaseYarnAPI):
    """
    Timeline server REST API

    :param str address: TimelineServer HTTP address
    :param int port: HistoryServer HTTP port
    :param int timeout: API connection timeout in seconds
    :param boolean kerberos_enabled: Flag identifying is Kerberos Security has been enabled for YARN
    """
    def __init__(self, address=None, port=8188, timeout=30, kerberos_enabled=False):
        self.address, self.port, self.timeout, self.kerberos_enabled = address, port, timeout, kerberos_enabled
        if address is None:
            self.logger.debug('Get information from hadoop conf dir')
            address, port = get_jobhistory_host_port()
            self.address, self.port = address, port


    def apps(self, state=None, user=None, queue=None, limit=None,
             started_time_begin=None, started_time_end=None,
             finished_time_begin=None, finished_time_end=None):
        """
        Application List

        http(s)://<timeline server http(s) address:port>/ws/v1/applicationhistory/apps

        Query Parameters:
        states - applications matching the given application states, specified as a comma-separated list
        finalStatus - the final status of the application - reported by the application itself
        user - user name
        queue - queue name
        limit - total number of app objects to be returned
        startedTimeBegin - applications with start time beginning with this time, specified in ms since epoch
        startedTimeEnd - applications with start time ending with this time, specified in ms since epoch
        finishedTimeBegin - applications with finish time beginning with this time, specified in ms since epoch
        finishedTimeEnd - applications with finish time ending with this time, specified in ms since epoch
        applicationTypes - applications matching the given application types, specified as a comma-separated list

        :param str user: user name
        :param str state: the job state
        :param str queue: queue name
        :param str limit: total number of app objects to be returned
        :param str started_time_begin: jobs with start time beginning with
            this time, specified in ms since epoch
        :param str started_time_end: jobs with start time ending with this
            time, specified in ms since epoch
        :param str finished_time_begin: jobs with finish time beginning with
            this time, specified in ms since epoch
        :param str finished_time_end: jobs with finish time ending with this
            time, specified in ms since epoch
        :returns: API response object with JSON data
        :rtype: :py:class:`yarn_api_client.base.Response`
        :raises yarn_api_client.errors.IllegalArgumentError: if `state`
            incorrect
        """
        path = '/ws/v1/applicationhistory/apps'

        legal_states = set([s for s, _ in YarnApplicationState])
        if state is not None and state not in legal_states:
            msg = 'App Internal State %s is illegal' % (state,)
            raise IllegalArgumentError(msg)

        loc_args = (
            ('state', state),
            ('user', user),
            ('queue', queue),
            ('limit', limit),
            ('startedTimeBegin', started_time_begin),
            ('startedTimeEnd', started_time_end),
            ('finishedTimeBegin', finished_time_begin),
            ('finishedTimeEnd', finished_time_end))

        params = self.construct_parameters(loc_args)

        return self.request(path, **params)
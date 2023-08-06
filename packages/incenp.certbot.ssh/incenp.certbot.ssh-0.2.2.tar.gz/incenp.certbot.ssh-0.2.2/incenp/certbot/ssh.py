# -*- coding: utf-8 -*-
"""SSH plugin."""

import logging
import zope.interface
from acme import challenges
from certbot import errors
from certbot import interfaces
from certbot.plugins import common

from subprocess import Popen, PIPE

logger = logging.getLogger(__name__)


class Authenticator(common.Plugin):
    """SSH Authenticator.

    This plugin sends the token required for HTTP validation
    to a remote program called through SSH. It is then up to
    the remote program to make the tokens available through
    HTTP.

    """
    zope.interface.implements(interfaces.IAuthenticator)
    zope.interface.classProvides(interfaces.IPluginFactory)

    description = "Send authentication tokens through SSH"

    def __init__(self, *args, **kwargs):
        super(Authenticator, self).__init__(*args, **kwargs)

    @classmethod
    def add_parser_arguments(cls, add):
        add("server",
            help="Specify the SSH server to connect to.")
        add("remote-command", default="acme-challenge",
            help="Specify the command to execute on the server.")

    def prepare(self):
        if self.conf("server") is None:
            raise errors.MisconfigurationError("Remote server is not set.")

    def more_info(self):
        return ("This authenticator performs http-01 validation on a "
                "remote machine through a SSH connection.")

    def get_chall_pref(self, domain):
        return [challenges.HTTP01]

    def perform(self, achalls):
        responses = []
        lines = ""
        for achall in achalls:
            response, validation = achall.response_and_validation()
            lines += "%s %s\n" % (achall.domain, validation)
            responses.append(response)

        ssh = Popen(["ssh", self.conf("server"), self.conf("remote-command")],
                    stdin=PIPE)
        ssh.stdin.write(lines)
        ssh.stdin.close()
        ssh.wait()

        return responses

    def cleanup(self, achalls):
        ssh = Popen(["ssh", self.conf("server"),
                     "%s %s" % (self.conf("remote-command"), "clean")])
        ssh.wait()

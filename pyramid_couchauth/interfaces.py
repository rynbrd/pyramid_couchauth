# Copyright (c) 2011-2012 Ryan Bourgeois <bluedragonx@gmail.com>
#
# This project is free software according to the BSD-modified license. Refer to
# the LICENSE file for complete details.
"""
Interfaces for use when implementing portions of pyramid_couchauth in a
project.
"""

from zope.interface import Interface


class IIdentifier(Interface):

    """
    Interface for identifying and saving a currently authenticated principal.
    """

    def identify(self, request):
        """
        Return the username of the currently remembered user or None if no user
        has been remembered.

        :param request: The WSGI request.
        :return: The remembered username or None.
        """

    def remember(self, request, principal, **kw):
        """
        Return a list of headers necessary for remembering the given username.
        These will be passed as part of the WSGI response.

        :param request: The WSGI request.
        :param principal: The principal to save.
        :param kw: Additional identifier parameters.
        :return: A list of headers to add to the response.
        """

    def forget(self, request):
        """
        Return a list of headers necessary for forgetting the remembered
        username.

        :param request: The WSGI request.
        :return: A list of headers to add to the response.
        """


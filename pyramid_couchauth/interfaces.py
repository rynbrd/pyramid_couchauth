# Copyright (c) 2011, Ryan Bourgeois <bluedragonx@gmail.com>
# All rights reserved.
#
# This software is licensed under a modified BSD license as defined in the
# provided license file at the root of this project.  You may modify and/or
# distribute in accordance with those terms.
#
# This software is provided "as is" and any express or implied warranties,
# including, but not limited to, the implied warranties of merchantability and
# fitness for a particular purpose are disclaimed.
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


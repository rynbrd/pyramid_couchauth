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

from zope.interface import Interface

class IIdentifier(Interface):
    """
    Interface for identifying and saving a currently authenticated principal.
    """

    def identify(self, request):
        """
        Return the principle of the currently authenticated user or None if no
        user is authorized.
        :param request: The WSGI request.
        :return: A string with the currently authenticated principle or None.
        """

    def remember(self, request, principle, **kw):
        """
        Return a list of headers necessary for remembering the given principle.
        These will be appended to the response.
        :param request: The WSGI request.
        :param principle: The principle to save.
        :param kw: Additional identifier parameters.
        :return: A list of headers to add to the response.
        """

    def forget(self, request):
        """
        Return a list of headers necessary for forgetting any saved principle.
        :param request: The WSGI request.
        :return: A list of headers to add to the response.
        """


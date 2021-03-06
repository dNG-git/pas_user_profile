# -*- coding: utf-8 -*-

"""
direct PAS
Python Application Services
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?pas;user_profile

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;mpl2
----------------------------------------------------------------------------
#echo(pasUserProfileVersion)#
#echo(__FILEPATH__)#
"""

# pylint: disable=unused-argument

from dNG.database.nothing_matched_exception import NothingMatchedException
from dNG.module.named_loader import NamedLoader
from dNG.plugins.hook import Hook
from dNG.runtime.value_exception import ValueException

def delete(params, last_return = None):
    """
Called for "dNG.pas.user.Profile.delete"

:param params: Parameter specified
:param last_return: The return value from the last hook called.

:return: (mixed) Return value
:since:  v0.2.00
    """

    # pylint: disable=star-args

    if ("username" not in params): raise ValueException("Missing required argument")
    else:
        user_profile_class = NamedLoader.get_class("dNG.data.user.Profile")

        try:
            user_profile = user_profile_class.load_username(params['username'])

            Hook.call("dNG.pas.user.Profile.onDelete", user_profile_id = user_profile.get_id())
            user_profile.delete()
        except NothingMatchedException: pass
    #

    return last_return
#

def register_plugin():
    """
Register plugin hooks.

:since: v0.2.00
    """

    Hook.register("dNG.pas.user.Profile.delete", delete)
#

def unregister_plugin():
    """
Unregister plugin hooks.

:since: v0.2.00
    """

    Hook.unregister("dNG.pas.user.Profile.delete", delete)
#

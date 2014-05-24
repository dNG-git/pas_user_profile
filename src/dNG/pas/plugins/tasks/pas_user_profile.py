# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.plugins.tasks.pas_user_profile
"""
"""n// NOTE
----------------------------------------------------------------------------
direct PAS
Python Application Services
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
http://www.direct-netware.de/redirect.py?pas;user_profile

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
http://www.direct-netware.de/redirect.py?licenses;mpl2
----------------------------------------------------------------------------
#echo(pasUserProfileVersion)#
#echo(__FILEPATH__)#
----------------------------------------------------------------------------
NOTE_END //n"""

# pylint: disable=unused-argument

from dNG.pas.database.nothing_matched_exception import NothingMatchedException
from dNG.pas.module.named_loader import NamedLoader
from dNG.pas.plugins.hook import Hook
from dNG.pas.runtime.value_exception import ValueException

def delete(params, last_return = None):
#
	"""
Called for "dNG.pas.user.Profile.delete"

:param params: Parameter specified
:param last_return: The return value from the last hook called.

:return: (mixed) Return value
:since:  v0.1.00
	"""

	# pylint: disable=star-args

	if ("username" not in params): raise ValueException("Missing required arguments")
	else:
	#
		user_profile_class = NamedLoader.get_class("dNG.pas.data.user.Profile")

		try:
		#
			user_profile = user_profile_class.load_username(params['username'])
			user_profile.delete()
		#
		except NothingMatchedException: pass
	#

	return last_return
#

def unregister_plugin():
#
	"""
Unregister plugin hooks.

:since: v0.1.00
	"""

	Hook.unregister("dNG.pas.user.Profile.delete", delete)
#

def register_plugin():
#
	"""
Register plugin hooks.

:since: v0.1.00
	"""

	Hook.register("dNG.pas.user.Profile.delete", delete)
#

##j## EOF
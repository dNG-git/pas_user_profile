# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.plugins.database.pas_user_profile
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

from dNG.pas.module.named_loader import NamedLoader
from dNG.pas.plugins.hooks import Hooks

def plugin_db_load_all(params = None, last_return = None):
#
	"""
Load and register all SQLAlchemy objects to generate database tables.

:param params: Parameter specified
:param last_return: The return value from the last hook called.

:since: v0.1.00
	"""

	NamedLoader.get_instance("dNG.pas.database.instances.UserProfile")
#

def plugin_deregistration():
#
	"""
Unregister plugin hooks.

:since: v0.1.00
	"""

	Hooks.unregister("dNG.pas.Database.loadAll", plugin_db_load_all)
#

def plugin_registration():
#
	"""
Register plugin hooks.

:since: v0.1.00
	"""

	Hooks.register("dNG.pas.Database.loadAll", plugin_db_load_all)
#

##j## EOF
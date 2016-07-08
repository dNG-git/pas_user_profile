# -*- coding: utf-8 -*-
##j## BOF

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

from dNG.data.binary import Binary
from dNG.database.instance import Instance
from dNG.database.instances.permission import Permission as _DbPermission

class Permission(Instance):
#
	"""
The "Permission" class provides a relationship to a list of owners for the
given entry ID.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: user_profile
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	_DB_INSTANCE_CLASS = _DbPermission
	"""
SQLAlchemy database instance class to initialize for new instances.
	"""

	def set_data_attributes(self, **kwargs):
	#
		"""
Sets values given as keyword arguments to this method.

:since: v0.2.00
		"""

		with self:
		#
			if ("name" in kwargs): self.local.db_instance.name = Binary.utf8(kwargs['name'])
			if ("permitted" in kwargs): self.local.db_instance.permitted = kwargs['permitted']
		#
	#
#

##j## EOF
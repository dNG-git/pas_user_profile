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

from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import BOOLEAN, VARCHAR
from uuid import uuid4 as uuid

from .abstract import Abstract

class Permission(Abstract):
#
	"""
"TextEntry" contains the database representation for a text entry.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: user_profile
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	# pylint: disable=invalid-name

	__tablename__ = "{0}_permission".format(Abstract.get_table_prefix())
	"""
SQLAlchemy table name
	"""
	db_instance_class = "dNG.data.acl.Permission"
	"""
Encapsulating SQLAlchemy database instance class name
	"""
	db_schema_version = 1
	"""
Database schema version
	"""

	id = Column(VARCHAR(32), primary_key = True)
	"""
permission.id
	"""
	id_acl_entry = Column(VARCHAR(32), ForeignKey("{0}_acl.id".format(Abstract.get_table_prefix())), index = True, nullable = False)
	"""
permission.id_acl_entry
	"""
	name = Column(VARCHAR(255))
	"""
permission.name
	"""
	permitted = Column(BOOLEAN)
	"""
permission.permitted
	"""

	def __init__(self, *args, **kwargs):
	#
		"""
Constructor __init__(Permission)

:since: v0.2.00
		"""

		Abstract.__init__(self, *args, **kwargs)
		if (self.id is None): self.id = uuid().hex
	#
#

##j## EOF
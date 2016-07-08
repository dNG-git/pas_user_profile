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

from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column
from sqlalchemy.types import CHAR, VARCHAR
from uuid import uuid4 as uuid

from .abstract import Abstract
from .permission import Permission

class AclEntry(Abstract):
#
	"""
An "AclEntry" provides the database representation of an access control list
(ACL) entry.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: user_profile
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	# pylint: disable=invalid-name

	__tablename__ = "{0}_acl".format(Abstract.get_table_prefix())
	"""
SQLAlchemy table name
	"""
	db_instance_class = "dNG.data.acl.Entry"
	"""
Encapsulating SQLAlchemy database instance class name
	"""
	db_schema_version = 1
	"""
Database schema version
	"""

	id = Column(VARCHAR(32), primary_key = True)
	"""
acl.id
	"""
	owned_id = Column(VARCHAR(32), index = True, nullable = False)
	"""
acl.owned_id
	"""
	owner_id = Column(VARCHAR(32), index = True, nullable = False)
	"""
acl.owner_id
	"""
	owner_type = Column(CHAR(1), server_default = "u", nullable = False)
	"""
acl.owner_type
	"""

	rel_permissions = relationship(Permission)
	"""
Relation to Permission
	"""

	def __init__(self, *args, **kwargs):
	#
		"""
Constructor __init__(AclEntry)

:since: v0.2.00
		"""

		Abstract.__init__(self, *args, **kwargs)
		if (self.id is None): self.id = uuid().hex
	#
#

##j## EOF
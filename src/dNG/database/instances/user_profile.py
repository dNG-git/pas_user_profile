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

from sqlalchemy.orm import foreign, relationship, remote
from sqlalchemy.schema import Column
from sqlalchemy.types import BOOLEAN, CHAR, INT, FLOAT, TEXT, SMALLINT, VARCHAR
from time import time
from uuid import uuid4 as uuid

from dNG.database.types.date_time import DateTime

from .abstract import Abstract
from .acl_entry import AclEntry

class UserProfile(Abstract):
#
	"""
SQLAlchemy database instance for Profile.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas
:subpackage: user_profile
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	# pylint: disable=invalid-name

	__tablename__ = "{0}_user_profile".format(Abstract.get_table_prefix())
	"""
SQLAlchemy table name
	"""
	db_instance_class = "dNG.data.user.Profile"
	"""
Encapsulating SQLAlchemy database instance class name
	"""
	db_schema_version = 3
	"""
Database schema version
	"""

	id = Column(VARCHAR(32), primary_key = True)
	"""
user_profile.id
	"""
	type = Column(INT, server_default = "2", nullable = False)
	"""
user_profile.type
	"""
	type_ex = Column(VARCHAR(50), server_default = "", nullable = False)
	"""
user_profile.type_ex
	"""
	banned = Column(BOOLEAN, server_default = "0", nullable = False)
	"""
user_profile.banned
	"""
	deleted = Column(BOOLEAN, server_default = "0", nullable = False)
	"""
user_profile.deleted
	"""
	locked = Column(BOOLEAN, server_default = "1", nullable = False)
	"""
user_profile.locked
	"""
	name = Column(VARCHAR(100), nullable = False)
	"""
user_profile.name
	"""
	password = Column(CHAR(96))
	"""
user_profile.password
	"""
	password_missed = Column(SMALLINT, server_default = "0", nullable = False)
	"""
user_profile.password_missed
	"""
	lang = Column(VARCHAR(20), server_default = "", nullable = False)
	"""
user_profile.lang
	"""
	theme = Column(VARCHAR(100), server_default = "", nullable = False)
	"""
user_profile.theme
	"""
	email = Column(VARCHAR(255), nullable = False)
	"""
user_profile.email
	"""
	email_public = Column(BOOLEAN, server_default = "0", nullable = False)
	"""
user_profile.email_public
	"""
	credits = Column(INT, server_default = "0", nullable = False)
	"""
user_profile.credits
	"""
	title = Column(VARCHAR(255), server_default = "", nullable = False)
	"""
user_profile.title
	"""
	avatar = Column(VARCHAR(32))
	"""
user_profile.avatar
	"""
	signature = Column(TEXT, server_default = "", nullable = False)
	"""
user_profile.signature
	"""
	registration_ip = Column(VARCHAR(100), server_default = "", nullable = False)
	"""
user_profile.registration_ip
	"""
	registration_time = Column(DateTime, default = 0, nullable = False)
	"""
user_profile.registration_time
	"""
	secid = Column(CHAR(96), server_default = "", nullable = False)
	"""
user_profile.secid
	"""
	lastvisit_ip = Column(VARCHAR(100), server_default = "", nullable = False)
	"""
user_profile.lastvisit_ip
	"""
	lastvisit_time = Column(DateTime, default = 0, nullable = False)
	"""
user_profile.lastvisit_time
	"""
	rating = Column(FLOAT, server_default = "0", nullable = False)
	"""
user_profile.rating
	"""
	timezone = Column(FLOAT, server_default = "0", nullable = False)
	"""
user_profile.timezone
	"""

	rel_acl_entry = relationship(AclEntry, primaryjoin = (foreign(id) == remote(AclEntry.owned_id)), uselist = False)
	"""
Relation to AclEntry
	"""
	"""
@TODO: rel_user_groups = relationship(UserGroup, primaryjoin = (foreign(id) == remote(UserGroup.id_user)))
Relation to AclGroup
	"""

	def __init__(self, *args, **kwargs):
	#
		"""
Constructor __init__(UserProfile)

:since: v0.2.00
		"""

		Abstract.__init__(self, *args, **kwargs)
		if (self.id is None): self.id = uuid().hex
		if (self.registration_time is None): self.registration_time = int(time())
	#
#

##j## EOF
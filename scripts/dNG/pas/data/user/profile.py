# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.user.Profile
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

from sqlalchemy import BIGINT, CHAR, Column, INT, REAL, SMALLINT, TEXT, VARCHAR
#from sqlalchemy.orm import relationship
from time import time
from uuid import uuid4 as uuid

from dNG.pas.database.connection import Connection
from dNG.pas.database.instance import Instance

class Profile(Instance):
#
	TYPE_ADMINISTRATOR = 4
	"""
Profile identifies an administrator
	"""
	TYPE_EXTERNAL_VERIFIED_MEMBER = 1
	"""
Profile identifies an external verified member
	"""
	TYPE_MEMBER = 2
	"""
Profile identifies a member
	"""
	TYPE_MODERATOR = 3
	"""
Profile identifies a member with moderation rights
	"""

	__tablename__ = "{0}_user_profile".format(Instance.get_table_prefix())
	"""
SQLAlchemy table name
	"""

	db_id = Column("id", VARCHAR(32), primary_key = True)
	"""
user_profile.id
	"""
	db_type = Column("type", INT, server_default = "2", nullable = False)
	"""
user_profile.type
	"""
	db_type_ex = Column("type_ex", VARCHAR(50), server_default = "", nullable = False)
	"""
user_profile.type_ex
	"""
	db_banned = Column("banned", SMALLINT, server_default = "0", nullable = False)
	"""
user_profile.banned
	"""
	db_deleted = Column("deleted", SMALLINT, server_default = "0", nullable = False)
	"""
user_profile.deleted
	"""
	db_locked = Column("locked", SMALLINT, server_default = "1", nullable = False)
	"""
user_profile.locked
	"""
	db_name = Column("name", VARCHAR(100), nullable = False)
	"""
user_profile.name
	"""
	db_password = Column("password", CHAR(96), nullable = False)
	"""
user_profile.password
	"""
	db_lang = Column("lang", VARCHAR(20), server_default = "", nullable = False)
	"""
user_profile.lang
	"""
	db_theme = Column("theme", VARCHAR(100), server_default = "", nullable = False)
	"""
user_profile.theme
	"""
	db_email = Column("email", VARCHAR(255), nullable = False)
	"""
user_profile.email
	"""
	db_email_public = Column("email_public", SMALLINT, server_default = "0", nullable = False)
	"""
user_profile.email_public
	"""
	db_credits = Column("credits", INT, server_default = "0", nullable = False)
	"""
user_profile.credits
	"""
	db_title = Column("title", VARCHAR(255), server_default = "", nullable = False)
	"""
user_profile.title
	"""
	db_avatar = Column("avatar", VARCHAR(32))
	"""
user_profile.avatar
	"""
	db_signature = Column("signature", TEXT, server_default = "", nullable = False)
	"""
user_profile.signature
	"""
	db_registration_ip = Column("registration_ip", VARCHAR(100), server_default = "", nullable = False)
	"""
user_profile.registration_ip
	"""
	db_registration_time = Column("registration_time", BIGINT, server_default = "0", nullable = False)
	"""
user_profile.registration_time
	"""
	db_secid = Column("secid", CHAR(96), server_default = "", nullable = False)
	"""
user_profile.secid
	"""
	db_lastvisit_ip = Column("lastvisit_ip", VARCHAR(100), server_default = "", nullable = False)
	"""
user_profile.lastvisit_ip
	"""
	db_lastvisit_time = Column("lastvisit_time", BIGINT, server_default = "0", nullable = False)
	"""
user_profile.lastvisit_time
	"""
	db_rating = Column("rating", INT, server_default = "0", nullable = False)
	"""
user_profile.rating
	"""
	db_timezone = Column("timezone", REAL, server_default = "0", nullable = False)
	"""
user_profile.timezone
	"""

	#permissions = relationship("PermissionGroup", primaryjoin = "and_(Profile.db_id == PermissionGroup.db_id_source, PermissionGroup.db_type == 'u')", secondary = PermissionGroup)

	def __init__(self):
	#
		"""
Constructor __init__(Profile)

:since: v0.1.00
		"""

		Instance.__init__(self)

		if (self.db_id == None): self.db_id = uuid().hex
		if (self.db_registration_time == None): self.db_registration_time = int(time())
	#

	def db_get(self, *args):
	#
		"""
Return the requested attributes.

:return: (dict) Values for the requested attributes
:since:  v0.1.00
		"""

		_return = { }

		for attribute in args:
		#
			key = "db_{0}".format(attribute)
			_return[attribute] = (getattr(self, key) if (hasattr(self, key)) else None)
		#

		return _return
	#

	def db_set(self, **kwargs):
	#
		"""
Sets values given as keyword arguments to this method.

:since: v0.1.00
		"""

		if ("type" in kwargs):
		#
			_type = (kwargs['type'] if (type(kwargs['type']) == int) else self._get_type(kwargs['type']))
			self.db_type = _type
		#

		if ("type_ex" in kwargs): self.db_type_ex = kwargs['type_ex']
		if ("banned" in kwargs): self.db_banned = kwargs['banned']
		if ("deleted" in kwargs): self.db_deleted = kwargs['deleted']
		if ("locked" in kwargs): self.db_locked = kwargs['locked']
		if ("name" in kwargs): self.db_name = kwargs['name']
		if ("password" in kwargs): self.db_password = kwargs['password']
		if ("lang" in kwargs): self.db_lang = kwargs['lang']
		if ("theme" in kwargs): self.db_theme = kwargs['theme']
		if ("email" in kwargs): self.db_email = kwargs['email']
		if ("email_public" in kwargs): self.db_email_public = kwargs['email_public']
		if ("credits" in kwargs): self.db_credits = kwargs['credits']
		if ("title" in kwargs): self.db_title = kwargs['title']
		if ("avatar" in kwargs): self.db_avatar = kwargs['avatar']
		if ("signature" in kwargs): self.db_signature = kwargs['signature']
		if ("registration_ip" in kwargs): self.db_registration_ip = kwargs['registration_ip']
		if ("registration_time" in kwargs): self.db_registration_time = kwargs['registration_time']
		if ("secid" in kwargs): self.db_secid = kwargs['secid']
		if ("lastvisit_ip" in kwargs): self.db_lastvisit_ip = kwargs['lastvisit_ip']
		if ("lastvisit_time" in kwargs): self.db_lastvisit_time = kwargs['lastvisit_time']
		if ("rating" in kwargs): self.db_rating = kwargs['rating']
		if ("timezone" in kwargs): self.db_timezone = kwargs['timezone']
	#

	def is_type(self, _type):
	#
		"""
Checks if the user type is the given one.

:param _type: User type to be checked

:return: (bool) True if the user type is the given one
:since:  v0.1.00
		"""

		if (type(_type) != int): _type = self._get_type(_type)
		return (self.db_type == _type)
	#

	def _get_type(self, _type):
	#
		"""
Parses the given type parameter given as a string value.

:param _type: String type

:return: (int) Internal type
:since:  v0.1.00
		"""

		if (_type == "ad"): _return = Profile.TYPE_ADMINISTRATOR
		elif (_type == "me"): _return = Profile.TYPE_MEMBER
		elif (_type == "mo"): _return = Profile.TYPE_MODERATOR
		else: _return = 0

		return _return
	#

	@staticmethod
	def db_get_id(_id):
	#
		database = Connection.get_instance()
		return database.query(Profile).filter(Profile.db_id == _id).first()
	#

	@staticmethod
	def db_get_username(username):
	#
		database = Connection.get_instance()
		return database.query(Profile).filter(Profile.db_name == username).first()
	#
#

##j## EOF
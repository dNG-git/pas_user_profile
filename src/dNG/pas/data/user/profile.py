# -*- coding: utf-8 -*-
##j## BOF

"""
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
"""

from dNG.pas.data.binary import Binary
from dNG.pas.data.settings import Settings
from dNG.pas.data.text.tmd5 import Tmd5
from dNG.pas.database.connection import Connection
from dNG.pas.database.instance import Instance
from dNG.pas.database.lockable_mixin import LockableMixin
from dNG.pas.database.nothing_matched_exception import NothingMatchedException
from dNG.pas.database.instances.user_profile import UserProfile as _DbUserProfile
from dNG.pas.runtime.value_exception import ValueException
from .abstract_profile import AbstractProfile

class Profile(Instance, LockableMixin, AbstractProfile):
#
	"""
"Profile" contains user specific data used for the Python Application
Services. Logging in and additional details may come from external sources.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: user_profile
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def __init__(self, db_instance = None):
	#
		"""
Constructor __init__(Profile)

:since: v0.1.00
		"""

		if (db_instance == None): db_instance = _DbUserProfile()

		Instance.__init__(self, db_instance)
		LockableMixin.__init__(self)
		AbstractProfile.__init__(self)

		self.db_id = (None if (db_instance == None) else db_instance.id)
		"""
Database ID used for reloading
		"""

		self.supported_features['password_missed'] = True
	#

	def is_banned(self):
	#
		"""
Checks if the user has been banned.

:return: (bool) True if the user has been banned
:since:  v0.1.00
		"""

		profile_data = self.get_data_attributes("banned")
		return profile_data['banned']
	#

	def is_deleted(self):
	#
		"""
Checks if the user has been deleted.

:return: (bool) True if the user has been deleted
:since:  v0.1.00
		"""

		profile_data = self.get_data_attributes("deleted")
		return profile_data['deleted']
	#

	def is_password_valid(self, password):
	#
		"""
Checks if the password is correct.

:param password: User profile password

:return: (bool) True if valid
:since:  v0.1.00
		"""

		salt = Settings.get("pas_user_profile_password_salt")
		if (salt == None): raise ValueException("User profile password salt is not defined")

		with self:
		#
			hashed_password = Tmd5.password_hash(password, Settings.get("pas_user_profile_password_salt"), self.local.db_instance.name)

			return (hashed_password == self.local.db_instance.password
			        and self.local.db_instance.type_ex == ""
			       )
		#
	#

	def is_reloadable(self):
	#
		"""
Returns true if the instance can be reloaded automatically in another
thread.

:return: (bool) True if reloadable
:since:  v0.1.00
		"""

		_return = True

		if (self.db_id == None):
		# Thread safety
			with self._lock: _return = (self.db_id != None)
		#

		return _return
	#

	def is_type(self, _type):
	#
		"""
Checks if the user type is the given one.

:param _type: User type to be checked

:return: (bool) True if the user type is the given one
:since:  v0.1.00
		"""

		with self:
		#
			if (type(_type) != int): _type = self.__class__.get_type(_type)
			return (self.local.db_instance.type == _type)
		#
	#

	def is_valid(self):
	#
		"""
Checks if the user is valid (not banned, deleted or locked).

:param _type: User type to be checked

:return: (bool) True if the user type is the given one
:since:  v0.1.00
		"""

		profile_data = self.get_data_attributes("banned", "deleted", "locked")
		return (False if (profile_data['banned'] or profile_data['deleted'] or profile_data['locked']) else True)
	#

	def lock(self):
	#
		"""
Locks a user profile.

:since: v0.1.00
		"""

		self.set_data_attributes(locked = True)
	#

	def set_data_attributes(self, **kwargs):
	#
		"""
Sets values given as keyword arguments to this method.

:since: v0.1.00
		"""

		with self:
		#
			if ("type" in kwargs):
			#
				_type = (kwargs['type'] if (type(kwargs['type']) == int) else self.__class__.get_type(kwargs['type']))
				self.local.db_instance.type = _type
			#

			if ("type_ex" in kwargs): self.local.db_instance.type_ex = kwargs['type_ex']
			if ("banned" in kwargs): self.local.db_instance.banned = kwargs['banned']
			if ("deleted" in kwargs): self.local.db_instance.deleted = kwargs['deleted']
			if ("locked" in kwargs): self.local.db_instance.locked = kwargs['locked']
			if ("name" in kwargs): self.local.db_instance.name = Binary.utf8(kwargs['name'])
			if ("password" in kwargs): self.local.db_instance.password = kwargs['password']
			if ("lang" in kwargs): self.local.db_instance.lang = kwargs['lang']
			if ("theme" in kwargs): self.local.db_instance.theme = kwargs['theme']
			if ("email" in kwargs): self.local.db_instance.email = Binary.utf8(kwargs['email'])
			if ("email_public" in kwargs): self.local.db_instance.email_public = kwargs['email_public']
			if ("credits" in kwargs): self.local.db_instance.credits = kwargs['credits']
			if ("title" in kwargs): self.local.db_instance.title = Binary.utf8(kwargs['title'])
			if ("avatar" in kwargs): self.local.db_instance.avatar = kwargs['avatar']
			if ("signature" in kwargs): self.local.db_instance.signature = Binary.utf8(kwargs['signature'])
			if ("registration_ip" in kwargs): self.local.db_instance.registration_ip = kwargs['registration_ip']
			if ("registration_time" in kwargs): self.local.db_instance.registration_time = int(kwargs['registration_time'])
			if ("secid" in kwargs): self.local.db_instance.secid = kwargs['secid']
			if ("lastvisit_ip" in kwargs): self.local.db_instance.lastvisit_ip = kwargs['lastvisit_ip']
			if ("lastvisit_time" in kwargs): self.local.db_instance.lastvisit_time = int(kwargs['lastvisit_time'])
			if ("rating" in kwargs): self.local.db_instance.rating = kwargs['rating']
			if ("timezone" in kwargs): self.local.db_instance.timezone = kwargs['timezone']
		#
	#

	def set_password(self, password):
	#
		"""
Sets the profile password.

:param password: User profile password

:since: v0.1.00
		"""

		salt = Settings.get("pas_user_profile_password_salt")
		if (salt == None): raise ValueException("User profile password salt is not defined")

		with self:
		#
			hashed_password = Tmd5.password_hash(password, Settings.get("pas_user_profile_password_salt"), self.local.db_instance.name)
			self.local.db_instance.password = hashed_password
		#
	#

	def unlock(self):
	#
		"""
Unlocks a user profile.

:since: v0.1.00
		"""

		self.set_data_attributes(locked = False)
	#

	@staticmethod
	def load_email(email, insensitive = False):
	#
		"""
Load Profile instance by an e-mail address.

:param email: Profile's e-mail address
:param insensitive: Search case-insensitive for the given value

:return: (object) Profile instance on success
:since:  v0.1.00
		"""

		if (email == None): raise NothingMatchedException("Profile e-mail is invalid")

		with Connection.get_instance() as connection:
		#
			db_instance = (connection.query(_DbUserProfile).filter(_DbUserProfile.email.ilike(email)).first()
			               if (insensitive) else
			               connection.query(_DbUserProfile).filter(_DbUserProfile.email == email).first()
			              )
		#

		if (db_instance == None): raise NothingMatchedException("Profile e-mail '{0}' is invalid".format(email))
		return Profile(db_instance)
	#

	@staticmethod
	def load_id(_id):
	#
		"""
Load Profile instance by ID.

:param _id: Profile ID

:return: (object) Profile instance on success
:since:  v0.1.00
		"""

		if (_id == None): raise NothingMatchedException("Profile ID is invalid")

		with Connection.get_instance() as connection: db_instance = connection.query(_DbUserProfile).get(_id)
		if (db_instance == None): raise NothingMatchedException("Profile ID '{0}' is invalid".format(_id))
		return Profile(db_instance)
	#

	@staticmethod
	def load_list(offset = 0, limit = -1, _type = None):
	#
		"""
Load a list of valid user profiles sorted by registration time.

:param offset: SQLAlchemy query offset
:param limit: SQLAlchemy query limit
:param _type: User type to be checked

:return: (list) List of profile instances on success
:since:  v0.1.00
		"""

		with Connection.get_instance() as connection:
		#
			db_query = connection.query(_DbUserProfile).filter(_DbUserProfile.deleted != True)

			if (_type != None):
			#
				if (type(_type) != int): _type = Profile.get_type(_type)
				db_query = db_query.filter(_DbUserProfile.type == _type)
			#

			if (offset > 0): db_query = db_query.offset(offset)
			if (limit > 0): db_query = db_query.limit(limit)

			return Profile.buffered_iterator(_DbUserProfile, connection.execute(db_query), Profile)
		#
	#

	@staticmethod
	def load_username(username, insensitive = False):
	#
		"""
Load Profile instance by user name.

:param username: Profile's user name
:param insensitive: Search case-insensitive for the given value

:return: (object) Profile instance on success
:since:  v0.1.00
		"""

		if (username == None): raise NothingMatchedException("Profile user name is invalid")

		with Connection.get_instance() as connection:
		#
			db_instance = (connection.query(_DbUserProfile).filter(_DbUserProfile.name.ilike(username)).first()
			               if (insensitive) else
			               connection.query(_DbUserProfile).filter(_DbUserProfile.name == username).first()
			              )
		#

		if (db_instance == None): raise NothingMatchedException("Profile user name '{0}' is invalid".format(username))
		return Profile(db_instance)
	#
#

##j## EOF
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

from dNG.pas.data.binary import Binary
from dNG.pas.database.connection import Connection
from dNG.pas.database.instance import Instance
from dNG.pas.database.instances.user_profile import UserProfile as _DbUserProfile
from dNG.pas.runtime.value_exception import ValueException

class Profile(Instance):
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

	def __init__(self, db_instance = None):
	#
		"""
Constructor __init__(Profile)

:since: v0.1.00
		"""

		if (db_instance == None): db_instance = _DbUserProfile()
		Instance.__init__(self, db_instance)

		self.db_id = (None if (db_instance == None) else db_instance.id)
		"""
Database ID used for reloading
		"""
	#

	def data_set(self, **kwargs):
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

	get_id = Instance._wrap_getter("id")
	"""
Returns the ID for this profile.

:return: (str) Profile ID; None if undefined
:since:  v0.1.00
	"""

	get_lang = Instance._wrap_getter("lang")
	"""
Returns the language for this profile.

:return: (str) Profile language; None if undefined
:since:  v0.1.00
	"""

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
		#
			# Value could be set in another thread so check again
			with self.lock: _return = (self.db_id != None)
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

		profile_data = self.data_get("banned", "deleted", "locked")
		return (False if (profile_data['banned'] or profile_data['deleted'] or profile_data['locked']) else True)
	#

	@staticmethod
	def get_type(_type):
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

	load = Instance._wrap_loader(_DbUserProfile)
	"""
Load Profile instance by the given criteria (AND condition is used).

:return: (object) Profile instance on success
:since:  v0.1.00
	"""

	@staticmethod
	def load_email(email):
	#
		"""
Load Profile instance by user name.

:param _id: Profile user name

:return: (object) Profile instance on success
:since:  v0.1.00
		"""

		with Connection.get_instance() as database: db_instance = database.query(_DbUserProfile).filter(_DbUserProfile.email == email).first()
		if (db_instance == None): raise ValueException("Profile e-mail '{0}' is invalid".format(email))
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

		with Connection.get_instance() as database: db_instance = database.query(_DbUserProfile).filter(_DbUserProfile.id == _id).first()
		if (db_instance == None): raise ValueException("Profile ID '{0}' is invalid".format(_id))
		return Profile(db_instance)
	#

	@staticmethod
	def load_username(username):
	#
		"""
Load Profile instance by user name.

:param _id: Profile user name

:return: (object) Profile instance on success
:since:  v0.1.00
		"""

		with Connection.get_instance() as database: db_instance = database.query(_DbUserProfile).filter(_DbUserProfile.name == username).first()
		if (db_instance == None): raise ValueException("Profile user name '{0}' is invalid".format(username))
		return Profile(db_instance)
	#
#

##j## EOF
# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.user.AbstractProfile
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

from dNG.pas.runtime.not_implemented_exception import NotImplementedException

class AbstractProfile(object):
#
	"""
"AbstractProfile" contains abstract user specific data used for the Python
Application Services.

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
	TYPE_GUEST = 0
	"""
Profile identifies a unknown guest
	"""
	TYPE_MEMBER = 2
	"""
Profile identifies a member
	"""
	TYPE_MODERATOR = 3
	"""
Profile identifies a member with moderation rights
	"""

	def data_get(self, *args):
	#
		"""
Sets values given as keyword arguments to this method.

:since: v0.1.00
		"""

		raise NotImplementedException()
	#

	def data_set(self, **kwargs):
	#
		"""
Sets values given as keyword arguments to this method.

:since: v0.1.00
		"""

		raise NotImplementedException()
	#

	def get_id(self):
	#
		"""
Returns the ID for this profile.

:return: (str) Profile ID; None if undefined
:since:  v0.1.00
		"""

		return self.data_get("id")['id']
	#

	def get_lang(self):
	#
		"""
Returns the language for this profile.

:return: (str) Profile language; None if undefined
:since:  v0.1.00
		"""

		return self.data_get("lang")['lang']
	#

	def is_type(self, _type):
	#
		"""
Checks if the user type is the given one.

:param _type: User type to be checked

:return: (bool) True if the user type is the given one
:since:  v0.1.00
		"""

		raise NotImplementedException()
	#

	def is_valid(self):
	#
		"""
Checks if the user is valid.

:return: (bool) True if the user is known and valid
:since:  v0.1.00
		"""

		return False
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

		if (_type == "ad"): _return = AbstractProfile.TYPE_ADMINISTRATOR
		elif (_type == "me"): _return = AbstractProfile.TYPE_MEMBER
		elif (_type == "mo"): _return = AbstractProfile.TYPE_MODERATOR
		else: _return = AbstractProfile.TYPE_GUEST

		return _return
	#

	@staticmethod
	def load_email(email):
	#
		"""
Load Profile instance by user name.

:param _id: Profile user name

:return: (object) Profile instance on success
:since:  v0.1.00
		"""

		raise NotImplementedException()
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

		raise NotImplementedException()
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

		raise NotImplementedException()
	#
#

##j## EOF
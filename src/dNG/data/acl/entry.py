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

from sqlalchemy.sql.expression import and_

from dNG.data.binary import Binary
from dNG.database.connection import Connection
from dNG.database.instance import Instance
from dNG.database.instances.acl_entry import AclEntry as _DbAclEntry
from dNG.database.nothing_matched_exception import NothingMatchedException

from .permission import Permission

class Entry(Instance):
#
	"""
An access control list (ACL) entry links an owned entry with granted
permissions.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: user_profile
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	_DB_INSTANCE_CLASS = _DbAclEntry
	"""
SQLAlchemy database instance class to initialize for new instances.
	"""

	def add_permission(self, permission):
	#
		"""
Add the given permission instance.

:param permission: Permission instance

:since: v0.2.00
		"""

		# pylint: disable=protected-access

		if (self.log_handler is not None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.add_entry()- (#echo(__LINE__)#)", self, context = "pas_database")

		if (isinstance(permission, Permission)):
		#
			with self:
			#
				self.local.db_instance.rel_permissions.append(permission._get_db_instance())

				if (self.local.permission_cache is not None):
				#
					permission_data = permission.get_data_attributes("name", "permitted")
					self.local.permission_cache[permission_data['name']] = { "permitted": permission_data['permitted'], "db_instance": permission }
				#
			#
		#
	#

	def _ensure_thread_local_permission_cache(self):
	#
		"""
Checks the thread-local permission cache dictionary.

:since: v0.2.00
		"""

		if (not hasattr(self.local, "permission_cache")): self.local.permission_cache = None
	#

	def get_acl_id(self):
	#
		"""
Returns the ACL ID of this instance.

:return: (str) Entry ACL ID; None if undefined
:since:  v0.2.00
		"""

		entry_data = self.get_data_attributes("owner_id", "owner_type")
		return "{0}_{1}".format(entry_data['owner_type'], entry_data['owner_id'])
	#

	get_owned_id = Instance._wrap_getter("owned_id")
	"""
Returns the owned entry ID of this instance.

:return: (str) Owned entry ID; None if undefined
:since:  v0.2.00
	"""

	get_owner_id = Instance._wrap_getter("owner_id")
	"""
Returns the owner ID of this instance.

:return: (str) ACL owner ID; None if undefined
:since:  v0.2.00
	"""

	get_owner_type = Instance._wrap_getter("owner_type")
	"""
Returns the owner type of this instance.

:return: (str) ACL owner type; None if undefined
:since:  v0.2.00
	"""

	def get_permissions(self):
	#
		"""
Returns the underlying database relation to the permission instances.

:return: (object) Permission instances database relation
:since:  v0.2.00
		"""

		with self: return self.local.db_instance.rel_permissions
	#

	def get_permissions_dict(self):
	#
		"""
Returns a dictionary with permissions.

:return: (dict) Dictionary of permissions
:since:  v0.2.00
		"""

		# pylint: disable=protected-access

		_return = { }

		self._ensure_thread_local_permission_cache()
		if (self.local.permission_cache is None): self._init_permission_cache()

		for permission_name in self.local.permission_cache: _return[permission_name] = self.local.permission_cache[permission_name]['permitted']

		return _return
	#

	def _init_permission_cache(self):
	#
		"""
Initializes the permission cache.

:since: v0.2.00
		"""

		if (self.local.permission_cache is None):
		#
			with self:
			#
				acl_id = "{0}_{1}".format(self.local.db_instance.owner_type, self.local.db_instance.owner_id)
				self.local.permission_cache = { }

				for permission in self.local.db_instance.rel_permissions:
				#
					if (self.log_handler is not None): self.log_handler.debug("{0!r} with ID '{1}' cached permission '{2}'", self, acl_id, permission.name, context = "pas_database")
					self.local.permission_cache[permission.name] = { "permitted": permission.permitted, "db_instance": permission }
				#
			#
		#
	#

	def remove_permission(self, permission):
	#
		"""
Removes the given permission instance.

:param permission: Permission instance

:since: v0.2.00
		"""

		# pylint: disable=protected-access

		if (self.log_handler is not None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.remove_entry()- (#echo(__LINE__)#)", self, context = "pas_database")

		if (isinstance(permission, Permission)):
		#
			with self:
			#
				self.local.db_instance.rel_permissions.remove(permission._get_db_instance())

				if (self.local.permission_cache is not None):
				#
					permission_data = permission.get_data_attributes("name", "permitted")
					if (permission_data['name'] in self.local.permission_cache): del(self.local.permission_cache[permission_data['name']])
				#
			#
		#
	#

	def set_data_attributes(self, **kwargs):
	#
		"""
Sets values given as keyword arguments to this method.

:since: v0.2.00
		"""

		with self:
		#
			if ("owned_id" in kwargs): self.local.db_instance.owned_id = kwargs['owned_id']
			if ("owner_id" in kwargs): self.local.db_instance.owner_id = kwargs['owner_id']
			if ("owner_type" in kwargs): self.local.db_instance.owner_type = kwargs['owner_type']
		#
	#

	def set_permission(self, name, permitted = True):
	#
		"""
Sets the permission with the specified name.

:since: v0.2.00
		"""

		name = Binary.str(name)
		if (self.log_handler is not None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.set_permission({1})- (#echo(__LINE__)#)", self, name, context = "pas_database")

		self._ensure_thread_local_permission_cache()

		with self:
		#
			if (self.local.permission_cache is None): self._init_permission_cache()

			if (name not in self.local.permission_cache):
			#
				permission = Permission()
				permission.set_data_attributes(name = name, permitted = permitted)

				self.add_permission(permission)
				self.local.permission_cache[name] = { "permitted": permitted, "db_instance": permission }
			#
		#
	#

	def unset_permission(self, name):
	#
		"""
Unsets the permission with the specified name.

:since: v0.2.00
		"""

		name = Binary.str(name)
		if (self.log_handler is not None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.set_permission({1})- (#echo(__LINE__)#)", self, name, context = "pas_database")

		self._ensure_thread_local_permission_cache()

		with self:
		#
			if (self.local.permission_cache is not None
			    and name in self.local.permission_cache
			   ):
			#
				self.remove_permission(Permission(self.local.permission_cache[name]['db_instance']))
				del(self.local.permission_cache[name])
			#
		#
	#

	@classmethod
	def load_acl_id(cls, owned_id, acl_id):
	#
		"""
Load Entry instance by its ACL ID.

:param cls: Expected encapsulating database instance class
:param _id: ACL ID

:return: (object) Entry instance on success
:since:  v0.2.00
		"""

		if (owned_id is None): raise NothingMatchedException("Owned ID is invalid")

		if (acl_id is None): raise NothingMatchedException("ACL ID is invalid")
		elif ("_" not in acl_id): raise NothingMatchedException("ACL ID '{0}' is invalid".format(acl_id))

		with Connection.get_instance():
		#
			( owner_type, owner_id ) = acl_id.split("_", 1)

			db_instance = (Instance.get_db_class_query(cls)
			               .filter(and_(_DbAclEntry.owned_id == owned_id,
			                            _DbAclEntry.owner_id == owner_id,
			                            _DbAclEntry.owner_type == owner_type
			                           )
			                      )
			               .first()
			              )

			if (db_instance is None): raise NothingMatchedException("ACL ID '{0}' for owned ID '{1}' is invalid".format(acl_id, owned_id))
			Instance._ensure_db_class(cls, db_instance)

			return Entry(db_instance)
		#
	#
#

##j## EOF
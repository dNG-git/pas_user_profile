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

# pylint: disable=unused-argument

from random import choice
import string

from dNG.pas.data.settings import Settings
from dNG.pas.data.text.tmd5 import Tmd5
from dNG.pas.data.user.profile import Profile
from dNG.pas.database.schema import Schema
from dNG.pas.loader.interactive_cli import InteractiveCli
from dNG.pas.module.named_loader import NamedLoader
from dNG.pas.plugins.hook import Hook

def after_apply_schema(params, last_return = None):
#
	"""
Called for "dNG.pas.Database.applySchema.after"

:param params: Parameter specified
:param last_return: The return value from the last hook called.

:return: (mixed) Return value
:since:  v0.1.00
	"""

	user_profile_class = NamedLoader.get_class("dNG.pas.data.user.Profile")

	if (issubclass(user_profile_class, Profile)):
	#
		db_user_profile_class = NamedLoader.get_class("dNG.pas.database.instances.UserProfile")
		Schema.apply_version(db_user_profile_class)

		cli = InteractiveCli.get_instance()

		if (isinstance(cli, InteractiveCli)
		    and hasattr(cli, "is_cli_setup")
		    and cli.is_cli_setup()
		   ): _ensure_administrative_user_account()
	#

	return last_return
#

def _ensure_administrative_user_account():
#
	"""
Checks if at least one active administrative user profile exists. Creates
one if this is not the case.

:since: v0.1.00
	"""

	cli = InteractiveCli.get_instance()
	cli.output_info("Validating administrative account ...")

	user_profile_class = NamedLoader.get_class("dNG.pas.data.user.Profile")

	if (next(user_profile_class.load_list(limit = 1, _type = "ad"), None) is not None): cli.output_info("Administrative account is available")
	else:
	#
		cli.output_info("No valid administrative account found")

		Settings.read_file("{0}/settings/pas_user_profile.json".format(Settings.get("path_data")))
		password = "".join(choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(20))
		password_encrypted = Tmd5.password_hash(password, Settings.get("pas_user_profile_password_salt"), "root")

		cli.output("")
		cli.output("A new default account will be generated.")
		cli.output("")
		cli.output("---------------------------------")
		cli.output("User name: root")
		cli.output("   e-mail: invalid@domain.invalid")
		cli.output(" Password: {0}", password)
		cli.output("---------------------------------")
		cli.output("")
		cli.output("Please change this account as soon as possible.")
		cli.output("")

		user_profile = user_profile_class()

		user_profile.set_data_attributes(type = user_profile_class.get_type("ad"),
		                                 name = "root",
		                                 password = password_encrypted,
		                                 locked = False,
		                                 email = "invalid@domain.invalid"
		                                )

		user_profile.save()
	#
#

def load_all(params, last_return = None):
#
	"""
Load and register all SQLAlchemy objects to generate database tables.

:param params: Parameter specified
:param last_return: The return value from the last hook called.

:return: (mixed) Return value
:since:  v0.1.00
	"""

	user_profile_class = NamedLoader.get_class("dNG.pas.data.user.Profile")
	if (issubclass(user_profile_class, Profile)): NamedLoader.get_class("dNG.pas.database.instances.UserProfile")

	return last_return
#

def register_plugin():
#
	"""
Register plugin hooks.

:since: v0.1.00
	"""

	Hook.register("dNG.pas.Database.applySchema.after", after_apply_schema)
	Hook.register("dNG.pas.Database.loadAll", load_all)
#

def unregister_plugin():
#
	"""
Unregister plugin hooks.

:since: v0.1.00
	"""

	Hook.unregister("dNG.pas.Database.applySchema.after", after_apply_schema)
	Hook.unregister("dNG.pas.Database.loadAll", load_all)
#

##j## EOF
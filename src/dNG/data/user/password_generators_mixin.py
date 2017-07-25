# -*- coding: utf-8 -*-

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

try: from hashlib import blake2s
except ImportError: blake2s = None

try: from hashlib import blake2b
except ImportError: blake2b = None

from dNG.data.binary import Binary
from dNG.data.settings import Settings
from dNG.data.text.tmd5 import Tmd5
from dNG.runtime.not_implemented_exception import NotImplementedException
from dNG.runtime.value_exception import ValueException

try:
    from passlib.exc import MissingBackendError
    from passlib.hash import argon2
except ImportError: argon2 = None

from .abstract_profile import AbstractProfile

class PasswordGeneratorsMixin(object):
    """
"PasswordGeneratorsMixin" is used by implementations to select and generate
password hashes.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: user_profile
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    PASSWORD_TYPE_TMD5 = 1
    """
TMD5 password type
    """
    PASSWORD_TYPE_MCF = 4
    """
Modular Crypt Format encoded password type
    """
    PASSWORD_TYPE_BLAKE2B = 3
    """
BLAKE2b password type
    """
    PASSWORD_TYPE_BLAKE2S = 2
    """
BLAKE2s password type
    """

    def __init__(self):
        """
Constructor __init__(Profile)

:since: v0.2.00
        """

        self.password_generators_available = [ ]
        """
List of password generators sorted by recommendation
        """

        if (argon2 is not None):
            try:
                argon2.get_backend()
                self.password_generators_available.append(PasswordGeneratorsMixin.PASSWORD_TYPE_MCF)
            except MissingBackendError: pass
        #

        if (blake2b is not None
            and blake2b.SALT_SIZE == 16
            and blake2b.PERSON_SIZE == 16
            ): self.password_generators_available.append(PasswordGeneratorsMixin.PASSWORD_TYPE_BLAKE2B)

        if (blake2s is not None
            and blake2s.SALT_SIZE == 8
            and blake2s.PERSON_SIZE == 8
           ): self.password_generators_available.append(PasswordGeneratorsMixin.PASSWORD_TYPE_BLAKE2S)

        self.password_generators_available.append(PasswordGeneratorsMixin.PASSWORD_TYPE_TMD5)
    #

    def _get_blake2_password(self, variant, password, username = None):
        """
Returns the BLAKE2 generated password hash.

:param password: User profile password
:param username: User name used while generating BLAKE2 hash

:return: (str) Hash on success; None if not supported
:since:  v0.2.00
        """

        blake2 = None
        blake2_person = None
        blake2_salt = None

        salt = Settings.get("pas_user_profile_password_salt")
        if (salt is None): raise ValueException("User profile password salt is not defined")

        if (variant == PasswordGeneratorsMixin.PASSWORD_TYPE_BLAKE2B):
            blake2 = blake2b
            blake2_salt = Binary.bytes(salt[:blake2b.SALT_SIZE])
            blake2_person = Binary.utf8_bytes(username[:blake2b.PERSON_SIZE])
        #

        if (variant == PasswordGeneratorsMixin.PASSWORD_TYPE_BLAKE2S):
            blake2 = blake2s
            blake2_salt = Binary.bytes(salt[:blake2s.SALT_SIZE])
            blake2_person = Binary.utf8_bytes(username[:blake2s.PERSON_SIZE])
        #

        if (blake2 is None): raise ValueException("BLAKE2 variant given is invalid")

        return blake2(Binary.utf8_bytes(password), salt = blake2_salt, person = blake2_person).hexdigest()
    #

    def _get_blake2b_password(self, password, username):
        """
Returns the BLAKE2b generated password hash.

:param password: User profile password
:param username: User name used while generating BLAKE2 hash

:return: (str) BLAKE2b hashed password
:since:  v0.2.00
        """

        return self._get_blake2_password(PasswordGeneratorsMixin.PASSWORD_TYPE_BLAKE2B, password, username)
    #

    def _get_blake2s_password(self, password, username):
        """
Returns the BLAKE2s generated password hash.

:param password: User profile password
:param username: User name used while generating BLAKE2 hash

:return: (str) BLAKE2s hashed password
:since:  v0.2.00
        """

        return self._get_blake2_password(PasswordGeneratorsMixin.PASSWORD_TYPE_BLAKE2S, password, username)
    #

    def _get_tmd5_password(self, password, username = None):
        """
Returns the triple MD5 generated password hash.

:param password: User profile password
:param username: User name used while generating the triple MD5 hash

:return: (str) Hash on success; None if not supported
:since:  v0.2.00
        """

        salt = Settings.get("pas_user_profile_password_salt")
        if (salt is None): raise ValueException("User profile password salt is not defined")

        return Tmd5.password_hash(password, salt, username)
    #

    def is_password_valid(self, password):
        """
Checks if the password is correct.

:param password: User profile password

:return: (bool) True if valid
:since:  v0.2.00
        """

        _return = False

        with self:
            if (self.local.db_instance.type != AbstractProfile.TYPE_EXTERNAL_VERIFIED_MEMBER):
                password_type = self.local.db_instance.password_type

                if (password_type == PasswordGeneratorsMixin.PASSWORD_TYPE_MCF
                    and PasswordGeneratorsMixin.PASSWORD_TYPE_MCF in self.password_generators_available
                   ): _return = argon2.verify(password, self.local.db_instance.password)

                if (password_type == PasswordGeneratorsMixin.PASSWORD_TYPE_BLAKE2B
                    and PasswordGeneratorsMixin.PASSWORD_TYPE_BLAKE2B in self.password_generators_available
                   ):
                    hashed_password = self._get_blake2b_password(password, self.local.db_instance.name)
                    _return = (hashed_password == self.local.db_instance.password)
                #

                if (password_type == PasswordGeneratorsMixin.PASSWORD_TYPE_BLAKE2S
                    and PasswordGeneratorsMixin.PASSWORD_TYPE_BLAKE2S in self.password_generators_available
                   ):
                    hashed_password = self._get_blake2s_password(password, self.local.db_instance.name)
                    _return = (hashed_password == self.local.db_instance.password)
                #

                if (password_type == PasswordGeneratorsMixin.PASSWORD_TYPE_TMD5
                    and PasswordGeneratorsMixin.PASSWORD_TYPE_TMD5 in self.password_generators_available
                   ):
                    hashed_password = self._get_tmd5_password(password, self.local.db_instance.name)
                    _return = (hashed_password == self.local.db_instance.password)
                #
            #
        #

        return _return
    #

    def set_password(self, password):
        """
Sets the profile password.

:param password: User profile password

:since: v0.2.00
        """

        with self:
            _type = None
            hashed_password = None

            if (PasswordGeneratorsMixin.PASSWORD_TYPE_MCF in self.password_generators_available):
                hashed_password = argon2.hash(password)
                _type = PasswordGeneratorsMixin.PASSWORD_TYPE_MCF
            elif (PasswordGeneratorsMixin.PASSWORD_TYPE_BLAKE2B in self.password_generators_available):
                hashed_password = self._get_blake2b_password(password, self.local.db_instance.name)
                _type = PasswordGeneratorsMixin.PASSWORD_TYPE_BLAKE2B
            elif (PasswordGeneratorsMixin.PASSWORD_TYPE_BLAKE2S in self.password_generators_available):
                hashed_password = self._get_blake2s_password(password, self.local.db_instance.name)
                _type = PasswordGeneratorsMixin.PASSWORD_TYPE_BLAKE2S
            elif (PasswordGeneratorsMixin.PASSWORD_TYPE_TMD5 in self.password_generators_available):
                hashed_password = self._get_tmd5_password(password, self.local.db_instance.name)
                _type = PasswordGeneratorsMixin.PASSWORD_TYPE_TMD5
            #

            if (hashed_password is None): raise NotImplementedException("No hash algorithm is supported")

            self.local.db_instance.password_type = _type
            self.local.db_instance.password = hashed_password
        #
    #
#

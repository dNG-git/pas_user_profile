-- direct PAS
-- Python Application Services
--
-- (C) direct Netware Group - All rights reserved
-- https://www.direct-netware.de/redirect?pas;user_profile
--
-- This Source Code Form is subject to the terms of the Mozilla Public License,
-- v. 2.0. If a copy of the MPL was not distributed with this file, You can
-- obtain one at http://mozilla.org/MPL/2.0/.
--
-- https://www.direct-netware.de/redirect?licenses;mpl2

-- Set rating and timezone as FLOAT

ALTER TABLE __db_prefix___user_profile RENAME TO __db_prefix__tmp_user_profile;

CREATE TABLE __db_prefix___user_profile (
 id VARCHAR(32) NOT NULL,
 type INTEGER DEFAULT 2 NOT NULL,
 type_ex VARCHAR(50) DEFAULT '' NOT NULL,
 banned BOOLEAN DEFAULT '0' NOT NULL,
 deleted BOOLEAN DEFAULT '0' NOT NULL,
 locked BOOLEAN DEFAULT '1' NOT NULL,
 name VARCHAR(100) NOT NULL,
 password CHAR(96),
 password_missed SMALLINT DEFAULT 0 NOT NULL,
 lang VARCHAR(20) DEFAULT '' NOT NULL,
 theme VARCHAR(100) DEFAULT '' NOT NULL,
 email VARCHAR(255) NOT NULL,
 email_public BOOLEAN DEFAULT '0' NOT NULL,
 credits INTEGER DEFAULT 0 NOT NULL,
 title VARCHAR(255) DEFAULT '' NOT NULL,
 avatar VARCHAR(32),
 signature TEXT DEFAULT '' NOT NULL,
 registration_ip VARCHAR(100) DEFAULT '' NOT NULL,
 registration_time DATETIME NOT NULL,
 secid CHAR(96) DEFAULT '' NOT NULL,
 lastvisit_ip VARCHAR(100) DEFAULT '' NOT NULL,
 lastvisit_time DATETIME NOT NULL,
 rating FLOAT DEFAULT 0 NOT NULL,
 timezone FLOAT DEFAULT 0 NOT NULL,
 PRIMARY KEY (id),
 CHECK (banned IN (0,1)),
 CHECK (deleted IN (0,1)),
 CHECK (locked IN (0,1)),
 CHECK (email_public IN (0,1))
);

INSERT INTO __db_prefix___user_profile SELECT * FROM __db_prefix__tmp_user_profile;

DROP TABLE __db_prefix__tmp_user_profile;
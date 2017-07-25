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

-- Add type value for password and avatar

ALTER TABLE __db_prefix___user_profile RENAME TO __db_prefix__tmp_user_profile;

CREATE TABLE __db_prefix___user_profile (
 id character varying(32)  NOT NULL,
 type smallint DEFAULT 2 NOT NULL,
 type_ex character varying(50) DEFAULT '' NOT NULL,
 banned boolean DEFAULT false NOT NULL,
 deleted boolean DEFAULT false NOT NULL,
 locked boolean DEFAULT true NOT NULL,
 name character varying(100) NOT NULL,
 password_type smallint DEFAULT 2 NOT NULL,
 password character varying(255),
 password_missed smallint DEFAULT 0 NOT NULL,
 lang character varying(20) DEFAULT '' NOT NULL,
 theme character varying(100) DEFAULT '' NOT NULL,
 email character varying(255) NOT NULL,
 email_public boolean DEFAULT false NOT NULL,
 credits integer DEFAULT 0 NOT NULL,
 title character varying(255) DEFAULT '' NOT NULL,
 avatar character varying(100),
 signature text DEFAULT '' NOT NULL,
 registration_ip character varying(100) DEFAULT '' NOT NULL,
 registration_time timestamp without time zone NOT NULL,
 secid CHAR(96) DEFAULT '' NOT NULL,
 lastvisit_ip character varying(100) DEFAULT '' NOT NULL,
 lastvisit_time timestamp without time zone NOT NULL,
 rating double precision DEFAULT 0 NOT NULL,
 timezone double precision DEFAULT 0 NOT NULL,
 PRIMARY KEY (id),
 CHECK (banned IN (0,1)),
 CHECK (deleted IN (0,1)),
 CHECK (locked IN (0,1)),
 CHECK (email_public IN (0,1))
);

ALTER TABLE __db_prefix___user_profile ADD CONSTRAINT __db_prefix___user_profile_pkey PRIMARY KEY (id);

INSERT INTO __db_prefix___user_profile SELECT id, type, type_ex, banned, deleted, locked, name, 1, password,
 password_missed, lang, theme, email, email_public, credits, title, avatar, signature, registration_ip,
 registration_time, secid, lastvisit_ip, lastvisit_time, rating, timezone
 FROM __db_prefix__tmp_user_profile;

DROP TABLE __db_prefix__tmp_user_profile;
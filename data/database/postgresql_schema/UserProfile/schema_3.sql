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

ALTER TABLE __db_prefix___user_profile ALTER COLUMN rating TYPE double precision;
ALTER TABLE __db_prefix___user_profile ALTER COLUMN timezone TYPE double precision;
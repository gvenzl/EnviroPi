--
-- Since: December, 2019
-- Author: gvenzl
-- Name: DBSetup.sql
-- Description: Database schema setup
--
-- Copyright 2019 Gerald Venzl
--
-- Licensed under the Apache License, Version 2.0 (the "License");
-- you may not use this file except in compliance with the License.
-- You may obtain a copy of the License at
--
--     http://www.apache.org/licenses/LICENSE-2.0
--
-- Unless required by applicable law or agreed to in writing, software
-- distributed under the License is distributed on an "AS IS" BASIS,
-- WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
-- See the License for the specific language governing permissions and
-- limitations under the License.
--

CREATE TABLE ENVIRONMENT
(
  id             VARCHAR2(50)               AS (     JSON_VALUE(data, '$.id'           RETURNING VARCHAR2(50))) VIRTUAL,
  tms_utc        TIMESTAMP WITH TIME ZONE   AS (     JSON_VALUE(data, '$.tms_utc'      RETURNING TIMESTAMP WITH TIME ZONE)) VIRTUAL,
  date_utc       DATE                       AS (CAST(JSON_VALUE(data, '$.tms_utc'      RETURNING TIMESTAMP WITH TIME ZONE) AS DATE)) VIRTUAL,
  air_poll_pct   NUMBER                     AS (     JSON_VALUE(data, '$.air_poll_pct' RETURNING NUMBER)) VIRTUAL,
  humi_pct       NUMBER                     AS (     JSON_VALUE(data, '$.humi_pct'     RETURNING NUMBER)) VIRTUAL,
  temp_celsius   NUMBER                     AS (     JSON_VALUE(data, '$.temp_celsius' RETURNING NUMBER)) VIRTUAL,
  data           VARCHAR2(255) CONSTRAINT valid_json CHECK (data IS JSON)
);
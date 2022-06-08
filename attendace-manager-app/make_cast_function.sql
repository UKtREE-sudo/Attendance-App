-- 数値 <-> 文字列変換
CREATE CAST (int4 AS text) WITH INOUT AS IMPLICIT;
CREATE CAST (text as numeric) WITH INOUT AS IMPLICIT;

-- || 演算子の定義
CREATE FUNCTION textint4cat(text, int4) RETURNS text
   AS 'SELECT $1 || $2::pg_catalog.text' LANGUAGE sql IMMUTABLE STRICT;

CREATE OPERATOR || (PROCEDURE = textint4cat,LEFTARG = text, RIGHTARG = int4);
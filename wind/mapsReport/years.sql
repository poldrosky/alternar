SELECT * FROM (

(SELECT latitude, longitude, value FROM maps WHERE tag_time LIKE '2000' AND tag_type = 1) AS a1

JOIN

(SELECT latitude, longitude, value FROM maps WHERE tag_time LIKE '2001' AND tag_type = 1) AS a2

USING(latitude, longitude)

JOIN

(SELECT latitude, longitude, value FROM maps WHERE tag_time LIKE '2002' AND tag_type = 1) AS a3

USING(latitude, longitude)

JOIN

(SELECT latitude, longitude, value FROM maps WHERE tag_time LIKE '2003' AND tag_type = 1) AS a4

USING(latitude, longitude)

JOIN

(SELECT latitude, longitude, value FROM maps WHERE tag_time LIKE '2004' AND tag_type = 1) AS a5

USING(latitude, longitude)

JOIN

(SELECT latitude, longitude, value FROM maps WHERE tag_time LIKE '2005' AND tag_type = 1) AS a6

USING(latitude, longitude)

JOIN

(SELECT latitude, longitude, value FROM maps WHERE tag_time LIKE '2006' AND tag_type = 1) AS a7

USING(latitude, longitude)

JOIN

(SELECT latitude, longitude, value FROM maps WHERE tag_time LIKE '2007' AND tag_type = 1) AS a8

USING(latitude, longitude)

JOIN

(SELECT latitude, longitude, value FROM maps WHERE tag_time LIKE '2008' AND tag_type = 1) AS a9

USING(latitude, longitude)

JOIN

(SELECT latitude, longitude, value FROM maps WHERE tag_time LIKE '2009' AND tag_type = 1) AS a10

USING(latitude, longitude)

JOIN

(SELECT latitude, longitude, value FROM maps WHERE tag_time LIKE '2010' AND tag_type = 1) AS a11

USING(latitude, longitude)

JOIN

(SELECT latitude, longitude, value FROM maps WHERE tag_time LIKE '2011' AND tag_type = 1) AS a12

USING(latitude, longitude)

JOIN

(SELECT latitude, longitude, value FROM maps WHERE tag_time LIKE '2012' AND tag_type = 1) AS a13

USING(latitude, longitude)

JOIN

(SELECT latitude, longitude, value FROM maps WHERE tag_time LIKE '2013' AND tag_type = 1) AS a14

USING(latitude, longitude)

JOIN

(SELECT latitude, longitude, value FROM maps WHERE tag_time LIKE '2014' AND tag_type = 1) AS a15

USING(latitude, longitude)
)

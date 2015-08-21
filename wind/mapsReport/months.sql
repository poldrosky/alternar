SELECT * FROM (

(SELECT latitude, longitude, VALUE AS january FROM maps WHERE tag_time LIKE 'January' AND tag_type = 1) AS a1

JOIN

(SELECT latitude, longitude, VALUE AS february FROM maps WHERE tag_time LIKE 'February' AND tag_type = 1) AS a2

USING(latitude, longitude)

JOIN

(SELECT latitude, longitude, VALUE AS march FROM maps WHERE tag_time LIKE 'March' AND tag_type = 1) AS a3

USING(latitude, longitude)

JOIN

(SELECT latitude, longitude, VALUE AS april FROM maps WHERE tag_time LIKE 'April' AND tag_type = 1) AS a4

USING(latitude, longitude)

JOIN

(SELECT latitude, longitude, VALUE AS may FROM maps WHERE tag_time LIKE 'May' AND tag_type = 1) AS a5

USING(latitude, longitude)

JOIN

(SELECT latitude, longitude, VALUE AS june FROM maps WHERE tag_time LIKE 'June' AND tag_type = 1) AS a6

USING(latitude, longitude)

JOIN

(SELECT latitude, longitude, VALUE AS july FROM maps WHERE tag_time LIKE 'July' AND tag_type = 1) AS a7

USING(latitude, longitude)

JOIN

(SELECT latitude, longitude, VALUE AS august FROM maps WHERE tag_time LIKE 'August' AND tag_type = 1) AS a8

USING(latitude, longitude)

JOIN

(SELECT latitude, longitude, VALUE AS september FROM maps WHERE tag_time LIKE 'September' AND tag_type = 1) AS a9

USING(latitude, longitude)

JOIN

(SELECT latitude, longitude, VALUE AS october FROM maps WHERE tag_time LIKE 'October' AND tag_type = 1) AS a10

USING(latitude, longitude)

JOIN

(SELECT latitude, longitude, VALUE AS november FROM maps WHERE tag_time LIKE 'November' AND tag_type = 1) AS a11

USING(latitude, longitude)

JOIN

(SELECT latitude, longitude, VALUE AS december FROM maps WHERE tag_time LIKE 'December' AND tag_type = 1) AS a12

USING(latitude, longitude)
)

library('DBI')
library('RPostgreSQL')
library('stringr')
library('kknn')
library('rminer')

drv <- dbDriver("PostgreSQL")
con <- dbConnect(drv, dbname="db",host="localhost",port=port,
                 user="user",password="pass")

setForSolar <- function(month){
query <- paste("SELECT
  latitude, longitude, avg(band1) as band1, avg(band2) as band2,
   avg(band3) as band3, avg(band4) as band4, avg(band5) as band5,
   avg(band6) as band6, avg(band7) as band7
FROM 
  reflectance
JOIN
	date_landsat
USING
	(id_landsat)
GROUP BY
	extract(month from date), latitude, longitude
having
	count(*) >= 3 and extract(month from date) =", month)

table <- dbGetQuery(con, query)
return (table)
}

M=loadmining("mlpe")
for (i in 1:12){ 
solar <- setForSolar(i)
Value=predict(M,solar[,c(3:9)])
solar <- cbind(solar,Value)
solar <- solar[sample(sample(seq(1:length(solar[,1])),5000)),]
nameFile <- paste0(i,".csv")
write.table(solar, file = nameFile, append = FALSE, quote = F, sep = ";", row.names = FALSE)
}


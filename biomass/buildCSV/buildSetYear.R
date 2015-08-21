library('DBI')
library('RPostgreSQL')
library('stringr')
library('kknn')
library('rminer')

drv <- dbDriver("PostgreSQL")
con <- dbConnect(drv, dbname="db",host="localhost",port=port,
                 user="user",password="pass")

models=c("ctree", "rpart", "kknn", "mlp", "mlpe","ksvm", "randomForest", "mr",
         "mars", "cubist", "pcr", "plsr", "cppls")


setForBiomass <- function(year){
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
	extract(year from date), latitude, longitude
having
	count(*) >= 3 and extract(year from date) =", year)

table <- dbGetQuery(con, query)
return (table)
}

M=loadmining("ksvm")
for (i in 2000:2014){ 
biomass <- setForBiomass(i)
Value=predict(M,biomass[,c(3:9)])
biomass <- cbind(biomass,Value)
biomass <- biomass[sample(sample(seq(1:length(biomass[,1])),5000)),]
nameFile <- paste0(i,".csv")
write.table(biomass, file = nameFile, append = FALSE, quote = F, sep = ";", row.names = FALSE)
}


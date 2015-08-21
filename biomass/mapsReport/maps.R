library(lattice)
library(rgdal)

rw.colors <- colorRampPalette(c('#FFFF00', '#FFE500', '#FFCB00',
                                '#FFB100','#FF9700','#FF7D00',
                                '#AA8F02', '#7FA503', '#55BA04',
                                '#2AD005', '#00E606'))

months <- read.table('biomassMonths.csv', header = TRUE, sep = ",")

max <- max(months[c(3:14)])
min <- min(months[c(3:14)])
at <- seq(min,max,0.1)

coordinates(months) = ~latitude+longitude

months <- as(months, 'SpatialPixelsDataFrame')

pdf(file='mapMonthsBiomass.pdf')

spplot(months, c('September','October','November','December',
                 'May', 'June', 'July', 'August',
                 'January', 'February', 'March', 'April'), 
       col.regions=rw.colors(length(at)), at=at)

dev.off()

years <- read.table('biomassYears.csv', header = TRUE, sep = ",")

max <- max(years[c(3:17)])
min <- min(years[c(3:17)])
at <- seq(min,max,0.1)

coordinates(years) = ~latitude+longitude

years <- as(years, 'SpatialPixelsDataFrame')

pdf(file='mapYearsBiomass.pdf')

spplot(years, c('X2010','X2011','X2012','X2013','X2014',
                'X2005','X2006','X2007','X2008','X2009',
                'X2000','X2001','X2002','X2003','X2004'),
       names.attr = c('2010','2011','2012','2013','2014',
                      '2005','2006','2007','2008','2009',
                      '2000','2001','2002','2003','2004'),
       col.regions=rw.colors(length(at)), at=at)

dev.off()

total <- readGDAL('Biomass.tif')

max <- summary(total)$data[6]
min <- summary(total)$data[1]
at <- seq(min,max,0.1)

pdf(file='mapGeneralBiomass.pdf')

spplot(total, col.regions=rw.colors(length(at)), at=at)

dev.off()

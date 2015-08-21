library(lattice)
library(rgdal)

rw.colors <- colorRampPalette(c('#0000FF', '#AAAA55', '#C6C638',
                                '#E2E21C', '#FFFF00', '#FFE200', '#FFC600',
                                '#FFAA00', '#FF8D00', '#FF7100', '#FF5500', 
                                '#FF3800', '#FF1C00', '#FF0000'))

months <- read.table('windMonths.csv', header = TRUE, sep = ",")

max <- max(months[c(3:14)])
min <- min(months[c(3:14)])
at <- seq(min,max,0.1)

coordinates(months) = ~latitude+longitude

months <- as(months, 'SpatialPixelsDataFrame')

pdf(file='mapMonthsWind.pdf')

spplot(months, c('September','October','November','December',
                'May', 'June', 'July', 'August',
                'January', 'February', 'March', 'April'), 
                col.regions=rw.colors(length(at)), at=at)

dev.off()

years <- read.table('windYears.csv', header = TRUE, sep = ",")

max <- max(years[c(3:17)])
min <- min(years[c(3:17)])
at <- seq(min,max,0.1)

coordinates(years) = ~latitude+longitude

years <- as(years, 'SpatialPixelsDataFrame')

pdf(file='mapYearsWind.pdf')

spplot(years, c('X2010','X2011','X2012','X2013','X2014',
                'X2005','X2006','X2007','X2008','X2009',
                'X2000','X2001','X2002','X2003','X2004'),
       names.attr = c('2010','2011','2012','2013','2014',
                      '2005','2006','2007','2008','2009',
                      '2000','2001','2002','2003','2004'),
       col.regions=rw.colors(length(at)), at=at)

dev.off()

total <- readGDAL('Wind.tif')

max <- summary(total)$data[6]
min <- summary(total)$data[1]
at <- seq(min,max,0.1)

pdf(file='mapGeneralWind.pdf')

spplot(total, col.regions=rw.colors(length(at)), at=at)

dev.off()

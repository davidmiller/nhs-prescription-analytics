
geoCode <- function(df){
  require(plyr)

  return(ddply(df, c("Postcode"), function(df) getGeoCode(df$Postcode)))
}

getGeoCode <- function(gcStr)  {
  require(RJSONIO)

  gcStr <- gsub(' ','%20',gcStr) #Encode URL Parameters
  #Open Connection
  connectStr <- paste('http://maps.google.com/maps/api/geocode/json?sensor=false&address=',gcStr, sep="")
  con <- tryCatch({
    url(connectStr)
  }, error = function(err){
    return(NULL)
  })
  if (is.null(con)){
    gcodes <- c(NA, NA)

  }else{
    data.json <- fromJSON(paste(readLines(con), collapse=""))
    close(con)
                                        #Flatten the received JSON
    data.json <- unlist(data.json)
    if(data.json["status"]=="OK")   {
      lat <- data.json["results.geometry.location.lat"]
      lng <- data.json["results.geometry.location.lng"]
      gcodes <- c(lat, lng)
    }
    names(gcodes) <- c("Lat", "Lng")
    return (gcodes)
  }
}


# JSON format for time series charts
toJSONarray <- function(dtf){
  clnms <- colnames(dtf)
  name.value <- function(i){
    quote <- '';
    if(class(dtf[, i])!='numeric'){
      quote <- '"';
    }
    paste('"', i, '" : ', quote, dtf[,i], quote, sep='')
  }
  objs <- apply(sapply(clnms, name.value), 1, function(x){paste(x, collapse=', ')})
  objs <- paste('{', objs, '}')
  res <- paste('[', paste(objs, collapse=', '), ']')
  return(res)
}

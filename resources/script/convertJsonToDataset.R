file <- read_json("bengaluru_india_places.geojson")
geojson_file <- toJSON(file)

##############################Install and load libraries####################################

list.of.packages <- c("ggplot2", "tidyjson", "dplyr", "jsonlite","rjson")
new.packages <- list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
if(length(new.packages)) install.packages(new.packages)


library(ggplot2)
library(tidyjson)
library(dplyr)
library(jsonlite)
library(rjson)
library(data.table)

#load working space
path_read <- ""

setwd(path_read)

filenames <- as.list(list.files(pattern = "\\.geojson"))


parse_JSON_to_CSV <- function(geojson_file) {

  # 1  
  data_properties <- geojson_file %>%
    enter_object("features") %>%
    gather_array %>% 
    spread_values(
      Record_type = jstring("type") 
      ) %>%  enter_object("properties") %>% 
    spread_values(
      id = jstring("id"),
      osm_id = jstring("osm_id"),
      name = jstring("name"),
      type = jnumber("type"),
      z_order = jstring("z_order"),
      population = jstring("population")
      )%>% 
    select(Record_type,id,osm_id,name,type,z_order,population) 


  #2
  data_geometry <- geojson_file %>%
    enter_object("features") %>%
    gather_array %>% 
    spread_values(
      Record_type = jstring("type") 
    ) %>%  enter_object("geometry") %>% 
    spread_values(
      geo_type = jstring("type"),
      coordinates = jstring("coordinates")
    ) %>% 
    select(Record_type,geo_type,coordinates) 
  
  data <- cbind(data_properties,data_geometry[,c(2:3)])
  
  data <- data[which(data$Record_type=="Feature" & data$geo_type=="Point" & !is.na(data$coordinates)),]
  return(data)
}

#create list of parsed datasets
list_parsed_df <- lapply(filenames,parse_JSON_to_CSV)


  
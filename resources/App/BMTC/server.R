#
# This is the server logic of a Shiny web application. You can run the 
# application by clicking 'Run App' above.
#
# Find out more about building applications with Shiny here:
# 
#    http://shiny.rstudio.com/
#

library(shiny)
library(plyr)
library(dplyr)
library(stringr)
library(ggplot2)

# Define server logic required to draw a histogram
shinyServer(function(input, output) {
  
  routesData <- read.csv(file="routes.csv", header=TRUE, sep=",")
  busRoutesData <- read.csv(file="bus_route.csv", header=TRUE, sep=",")
  timingsData <- read.csv(file="timings.csv", header=TRUE, sep=",")
  
  # Remove the distance unit from the data and retain only distance value
  routesData$distance <- as.character(routesData$distance)
  routesData$distance <- sapply(routesData$distance,str_trim)
  routesData$distance <- sapply(strsplit(routesData$distance, " "), head, 1)
  routesData$distance <- sapply(routesData$distance,function(x) as.numeric(x))
  
  # Converting string into duration in minutes
  routesData$time <- as.character(routesData$time)
  routesData$time <- sapply(routesData$time,str_trim)
  routesData$time <- sapply(strsplit(routesData$time, " "), head, 1)
  routesData$duration_min <- (as.numeric(sapply(strsplit(routesData$time, ":"), head, 1)) * 60) + as.numeric(sapply(strsplit(routesData$time, ":"), tail, 1))
  
  # Create a new column that labels each route a Round trip or Single trip
  routesData$tripType <- ifelse(as.character(routesData$origin) == as.character(routesData$destination), "Round", "Single")

  # Subsetting Data according to distance filter from slider Input
  distance_filter <- reactive({
    distance_filter <- subset(routesData,(routesData$distance >= input$slider_RouteDistance[1]) & (routesData$distance <= input$slider_RouteDistance[2]))
  })
  
  output$dimensions <- renderPrint({
    busRouteStats <- paste("There are", nrow(routesData), "rows and", ncol(routesData), "columns for routes.")
    print(busRouteStats)
  })
  
  # UI definition for Duration slider since it requires dynamic updated slider range based on distance slider.
  output$slider_duration <- renderUI({
    sliderInput("durationSlider",
                label = h4("Route Duration"), 
                min = min(distance_filter()$duration_min), 
                max = max(distance_filter()$duration_min), 
                value = c(0, 1500)
    )
  })
  
  # Removing unwanted columns from data inorder to provide only relevant data summary.
  cleanColumnData <- reactive ({

    removeColumns <- c("X", "tripType", "duration_min")
    cleanColumnData <- routesData[!(colnames(routesData) %in% removeColumns )]
  })
  
  # UI definition to select the required column
  output$columnSelection <- renderUI({
    selectInput("column", "Column:", 
                choices=colnames(cleanColumnData()))
  })
  
  # Filter to select only the required column
  columnFilter <- reactive({
    columnFilter <- cleanColumnData()[input$column]
  })
  
  # Ouput text that displays details of chosen column
  output$ChosenColumn <- renderText({
    
    paste("Column Class is ", sapply(cleanColumnData(), class)[input$column])
    
  })
  
  # Filter Data according duration slider based on the data filtered from distance slider
  distance_duration_filter <- reactive({
    distance_duration_filter<- subset(distance_filter(),(distance_filter()$duration_min >= input$durationSlider[1]) & (distance_filter()$duration_min <= input$durationSlider[2]))
  })
  
  # Creating a temporary storage for summarising round trip and single trips
  distanceRangeWiseRoutesdf <- reactive({
    distanceRangeWiseRoutesdf <- distance_duration_filter() %>% group_by(tripType) %>% dplyr::summarise(n = n())
  })
  
  # Plotting bar plot to display frequencies of round trip and single trips
  output$roundTripFreq <- renderPlot({
    
    ggplot(distanceRangeWiseRoutesdf(), aes(tripType, n, label = n))+
      geom_bar(stat = "identity", fill = "steelblue", width = 0.5) +
      geom_text(vjust = -0.5, color = "black") +
      theme_bw() +
      labs(title = "Trip Type Frequency", x = "Trip Type", y = "Frequency")+
      ylim(c(0,nrow(routesData)))+
      theme(title = element_text(face = "bold", color = "black"), 
            axis.title = element_text(face = "bold", color = "black"),
            axis.text.x = element_text(face = "bold", size = 8, angle = 90, vjust = 0.5),
            axis.text.y = element_text(face = "bold", size = 8),
            plot.title = element_text(hjust = 0.5))
  })
  
  # Plotting scatter plot to display distance vs duration
  output$distanceDurationScatter <- renderPlot({
    
    ggplot(distance_duration_filter(), aes(duration_min, distance, color = duration_min)) +
      geom_point(shape = 16, size = 2, show.legend = FALSE) +
      labs(title = "Distance Vs Duration", x = "Duration (min)", y = "Distance (km)") +
      theme(title = element_text(face = "bold", color = "black"), 
            axis.title = element_text(face = "bold", color = "black"),
            axis.text.x = element_text(face = "bold", size = 8, angle = 90, vjust = 0.5),
            plot.title = element_text(hjust = 0.5)) +
    scale_color_gradient(low = "#0091ff", high = "#f0650e")
  })
  
  # Plotting the data table with the data as per both distance and duration filters
  output$tripFreqDatatable <- renderDataTable({
    distance_duration_filter()[c("route_no","distance","origin", "destination", "duration_min")]
  })
})

# TODO
# Dataset summary
# Missing value count
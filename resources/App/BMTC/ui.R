#
# This is the user-interface definition of a Shiny web application. You can
# run the application by clicking 'Run App' above.
#
# Find out more about building applications with Shiny here:
# 
#    http://shiny.rstudio.com/
#

library(shiny)

# Define UI for application that draws a histogram
shinyUI(fluidPage(navbarPage("BMTC Exploratory Data Analysis",
                             tabPanel("Home",
                                      fluidRow(
                                        HTML("<center><h2>Schema Analysis</h2></center>")
                                        ),
                                      fluidRow(
                                        sidebarLayout(
                                          sidebarPanel(
                                            uiOutput("columnSelection")
                                          ),
                                          mainPanel(
                                            textOutput("ChosenColumn")
                                          )
                                        )
                                      )
                                      ),
                             tabPanel("Bus Routes",
                                      fluidRow(
                                        sidebarLayout(
                                          sidebarPanel(
                                            sliderInput("slider_RouteDistance",
                                                        label = h4("Route Distance"), 
                                                        min = 0, 
                                                        max = 100, 
                                                        value = c(0,30)
                                            ),
                                            uiOutput("slider_duration")
                                            ),
                                          mainPanel(
                                            tabsetPanel(
                                              tabPanel("Trip Type Frequency", 
                                                       plotOutput("roundTripFreq")
                                                       ),
                                              tabPanel("Distance Vs Duration", plotOutput("distanceDurationScatter"))
                                              )
                                            )
                                          )
                                        ),
                                      fluidRow(
                                        dataTableOutput("tripFreqDatatable")
                                      )
                                      ))
))

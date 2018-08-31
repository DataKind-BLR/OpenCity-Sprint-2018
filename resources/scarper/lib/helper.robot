*** Settings ***
Documentation                       Helper Keywords for Robot Framework
Library                             Selenium2Library
Library                             String
Library                             PSLECIScraper.py


*** Keywords ***
open
    [Arguments]                     ${element}
    Go To                           ${element}

select
    [Arguments]                     ${element}  ${value}
    Select From List                ${element}  ${value}

click
    [Arguments]                     ${element}
    Click Element                   ${element}

Scrape Data
    [Arguments]                     @{states}
    : FOR   ${state}                IN                      @{states}
    \   log to console              Scrapping State : ${state}
    \   select                      id=ddlState             ${state}
    \   @{districts}=               Get All Districts
    \   Get Districts               @{districts}

Get Districts
    [Arguments]                     @{districts}
    : FOR   ${district}             IN                      @{districts}
    \   log to console              Scrapping district : ${district}
    \   select                      id=ddlDistrict          ${district}
    \   @{acs}=                     Get All AC
    \   Get ACs                     @{acs}

Get ACs
    [Arguments]                     @{acs}
    : FOR   ${ac}                   IN                      @{acs}
    \   log to console              Scrapping constituency : ${ac}
    \   select                      id=ddlAC                ${ac}
    \   click                       id=imgbtnFind
    \   ${session}                  Get Cookie value        ASP.NET_SessionId
    \   Get Polling Station Data    ${session}

Scrape Data From PSL-ECI
    open                            http://psleci.nic.in/Default.aspx
    @{states}=                      Get All States
    Scrape Data                     @{states}

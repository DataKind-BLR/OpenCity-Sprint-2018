*** Settings ***
Resource            lib/helper.robot
Suite Setup         Open Browser    http://dhi.madhbhavikar.online    firefox
Suite Teardown      Close Browser


*** Test Cases ***
Scrape data for Polling Booths
    log to console  Initializing
    Scrape Data From PSL-ECI
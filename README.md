# covid-tracking
Tracking state test counts

## urls.yaml
This is a config file for [urlwatch](https://github.com/thp/urlwatch) to detect changes to health department pages (see [list here](https://docs.google.com/spreadsheets/d/18oVRrHj3c183mHmq3m89_163yuYltLNlOmPerQ18E8w/edit#gid=207813168)) and report them to a Slack channel for further analysis. 

`urlwatch` is running [this fork](https://github.com/COVID19Tracking/urlwatch) with patches to allow in-browser execution for the pages that need it and webhook reporting of changed pages for IFTTT integration.

todo:
- fine tune filters to narrow in on the correct data
- for those states that have structured data, automatically parse out data fields and detect changes

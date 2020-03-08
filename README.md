# covid-tracking
Tracking state test counts

## urls.yaml
This is a config file for [urlwatch](https://github.com/thp/urlwatch) to detect changes to health department pages (see [list here](https://docs.google.com/spreadsheets/d/18oVRrHj3c183mHmq3m89_163yuYltLNlOmPerQ18E8w/edit#gid=207813168)) and report them to a Slack channel for further analysis. 

urlwatch is running with [this patch](https://github.com/cfbao/urlwatch/commit/b965954ea608f60512de42d81bfc3e0bd686b7d0) applied to allow in-browser execution for the pages that need it (such as Arizona). 

todo:
- add all available state pages
- fine tune filters to narrow in on the correct data
- for those states that have structured data, automatically parse out data fields and detect changes

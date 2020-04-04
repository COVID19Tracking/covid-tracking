# covid-tracking
Tracking state test counts. Posting diff changes every ~30mins to #urlwatch in COVID-Tracking.

## Installation

- To install the fork of urlwatch: `pip install git+https://github.com/COVID19Tracking/urlwatch.git`
  - You also need the tesseract-ocr package, for which you can find the installation instructions [here](https://tesseract-ocr.github.io/tessdoc/Home.html)
- For development, you can also check out the `COVID19Tracking/urlwatch` repository and deploy from your local copy with `pip3 install .`

## urls.yaml
This is a config file for [urlwatch](https://github.com/thp/urlwatch) to detect changes to health department pages (see [list here](https://docs.google.com/spreadsheets/d/18oVRrHj3c183mHmq3m89_163yuYltLNlOmPerQ18E8w/edit#gid=207813168)) and report them to a Slack channel for further analysis.

`urlwatch` is running [this fork](https://github.com/COVID19Tracking/urlwatch) with patches to allow in-browser execution for the pages that need it and webhook reporting of changed pages for IFTTT integration.

## Getting started with modifying `urls.yaml` filters

_Note, this does not cover environment setup, but please ask in #coding if you have any issues/questions around getting dependencies setup and running. Lots of Python folks to help out!_

Jump into the repo root directory: `cd PATH/covid-tracking`

Output the current list of watchers: `urlwatch --urls urls.yaml --list`

Test the filter you're interested in, using the number from the `--list` command: `urlwatch --urls urls.yaml --test-filter FILTER_NUM`

And now the fun part:

- Open existing or new URL (sometimes takes manual searching/research around state health websites, Slack channels, etc.)

- Open Developer Tools (cmd+opt+i in Mac/Chrome)

- Investigate where test and/or case data is being outputted, check for higher-level CSS classes and/or elements/data structures to target

- Update filter using `css:CSS_RULES`, `xpath:XPATH_RULES`, or other available filters defined here: [urlwatch/filters](https://github.com/COVID19Tracking/urlwatch/blob/master/lib/urlwatch/filters.py). The parent repo is also a great resource: [github.com/thp/urlwatch](https://github.com/thp/urlwatch)

- Make sure to add `,html2text` on the end of your filter to clean up the output if using a `css` or `xpath` filter to keep things readable in the #urlwatch channel :)

- Re-run `urlwatch --urls urls.yaml --test-filter FILTER_NUM` to test/confirm your new rules are working.

- Ask questions!

- When ready, `git push` to `master` and let Josh Ellington and/or Zach Lipton know new rules are ready to be deployed.

Most important, keep an eye on #urlwatch! These pages are changing/going down/implementing new rules daily at this point. Responding quickly will keep everyone informed and updated on these data changes.

## TODO
- fine tune filters to narrow in on the correct data
- for those states that have structured data, automatically parse out data fields and detect changes

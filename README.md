[![Build Status](https://travis-ci.com/aalquist/cli-lds.svg?branch=master)](https://travis-ci.com/aalquist/cli-lds)

[![Vulnerability Scan](https://snyk.io/test/github/aalquist/cli-lds/badge.svg?targetFile=requirements.txt)](https://snyk.io/test/github/aalquist/cli-lds?targetFile=requirements.txt)

# cli-lds
Quick and dirty Log Delivery Service (LDS) command line tool to view and audit settings

## Example Commands Report Commands

Basic command with default output and filters

```bash
akamai lds cpcodelist

```

Basic command that only shows active lds configurations

```bash
akamai lds template --get active.json | akamai lds cpcodelist --use-stdin

```

Basic command that only shows active lds configurations with GPG encryption 

```bash
akamai lds template --get active-gpg.json | akamai lds cpcodelist --use-stdin


```

Convert output to CSV with JQ

```bash
akamai lds cpcodelist | jq -r '. | @csv'

```


View RAW LDS Json used  

```bash
akamai lds cpcodelist --show-json


```

## Customize Report Filters Commands

```bash
akamai lds template --get active-gpg.json > custom-query.json

```

modify custom-query.json based on RAW json from --show-json. Each json key pair value is using JSONPath which can extract value and/or filter to specific values

```bash
vi custom-query.json

```


```json
{
 "CPCODE": "$.logSource.id",
 "Aggregation_Frequency": "$.aggregationDetails.deliveryFrequency.value",
 "Status": "$[?(@.status=\"active\")].status",
 "Encoding": "$.encodingDetails.encoding.value",
 "Format": "$.logFormatDetails.logFormat.value"
}

```

Pipe in custom filter

```bash
cat custom-query.json | akamai lds cpcodelist --use-stdin

```

## Install
use Akamai CLI and install command:

```bash
akamai install https://github.com/aalquist/cli-lds

```

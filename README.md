[![Build Status](https://travis-ci.com/aalquist/cli-lds.svg?branch=master)](https://travis-ci.com/aalquist/cli-lds)

[![Vulnerability Scan](https://snyk.io/test/github/aalquist/cli-lds/badge.svg?targetFile=requirements.txt)](https://snyk.io/test/github/aalquist/cli-lds?targetFile=requirements.txt)

# cli-lds
Quick and dirty Log Delivery Service (LDS) command line tool to view and audit settings

## Example Commands Report Commands

Basic command that uses the default settings

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


View RAW LDS Json   

```bash
akamai lds cpcodelist --show-json


```

## Customize Report Filters Commands

```bash
akamai lds template --get active-gpg.json > custom-query.json

```

Using an existing template as a guide, modify the saved custom-query.json to filter for specific values you want. Tip: use the --show-json flag to see what other values are available. For simplicty, JSONPath is re-executed against each entity and not the entire json response from --show-json. JSONPath can be used to extract values or filter output to match your needs. 

```bash
vi custom-query.json

```

Example Template saved to local file:

```json
{
 "CPCODE": "$.logSource.id",
 "Aggregation_Frequency": "$.aggregationDetails.deliveryFrequency.value",
 "Status": "$[?(@.status=\"active\")].status",
 "Encoding": "$.encodingDetails.encoding.value",
 "Format": "$.logFormatDetails.logFormat.value"
}

```

Just like the other commands, pipe your custom filter into the tool 

```bash
cat custom-query.json | akamai lds cpcodelist --use-stdin

```

## Install
use Akamai CLI and install command:

```bash
akamai install https://github.com/aalquist/cli-lds

```

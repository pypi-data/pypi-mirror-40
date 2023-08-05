# opisense_client

## Intro
Python package providing some functions to interact with the Opisense API. 
More info about Opisense at www.opisense.com

## Warning
This is a first version to be tested by the users

## Changelog
### 0.3 :
#### force_path 
Added force_path optional parameter to http.POST and http.PUT. 
Overwrites the default OpisenseObject.api_path in the http call.

#### json_output
Added json_output optional parameter to http.GET
If True, Returns the JSON object from the http response if available.
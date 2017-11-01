* Connector Module Tasks:
[ ] Create module UI
	[ ] Provide and generate an api key
	[ ] Output the URL to .mvc file
	[ ] Provide instructions on how to configure sublime settings to pull data
	[ ] Allow user to limit which endpoints are accessible (radio interface)
	[ ] Create a popup interface which allows the administrator to view connection logs 
[ ] Create a Settings database table
[ ] Create a Logging database table
[ ] Hook into the User Access module feature
[ ] Create a JSON API
	[ ] Handle authentication
	[ ] Endpoints
		[ ] Customfield codes
		[ ] ReadyTheme codes
		[ ] 

* Miva IDE Tasks:
[ ] Create settings
	[ ] "mivaide_connector_enabled" -- boolean setting to disable fetching (default to false)
	[ ] "mivaide_connector_url" -- a url to the hosted .mvc endpoint
	[ ] "mivaide_connector_api_key" -- the api key provided within the connector module
	[ ] Allow configuration at the project level
[ ] Create Python script
	[ ] Determine optimal time to fetch data from the endpoints
	[ ] Process responses and generate completion caches
	[ ] Create "Test Endpoint" function
[ ] Expose the "Test Endpoint" function to the Command Palette
[appdynamics_single_api://<name>]
host_port = Enter the host and port for your AppDynamics Collector
auth_token = For a single tenant controller use the output of.: echo -n '<user>@customer1:<password>' | base64'for multi-tenant controller use the output of:echo -n '<user>@<accountname>:<password>' | base64'
duration = The time period (in minutes) that you wish to retrieve data for.  e.g.:  5 = retrieve data for the past 5 minutes.
app_name = The name (or ID) of your Application in AppDynamics
url_path = e.g.:  /metric-data    --or-- /events   --or--  /problems/healthrule-violations
params = e.g.: /metric-data  REQUIRES  metric-path=Overall Application Performance|* (hint: use 'Copy Full Path' in the AppDynamics Metric Browser)

[appdynamics_summary://<name>]
host_port = Enter the URL and Port for your AppDynamics Collector
appd_userid = The userid you use to login to AppDynamics
appd_password = The password you use to login to AppDynamics
account_name = For most on-premise deployments this will be the default value of 'customer1'.   For SaaS deployments this will be your account name.
duration = The time period (in minutes) that you wish to retrieve data for.  e.g.:  5 = retrieve data for the past 5 minutes.
app_name = Leave this blank to retrieve data for ALL applications in AppDynamics.  If you only want a single application, enter that application's name here.
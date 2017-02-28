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
metrics_to_collect = In large environments, metrics collected from Infrastructure Performance and Business Transactions can result in large amounts of data. Use with caution based on the size of  your environment.
app_name = Blank retrieves ALL applications.  Each application is 1 API call per metric set (4 sets * 50 apps = 200 calls). DO NOT LEAVE THIS BLANK IF YOU HAVE 50+ APPS as the controller could be overwhelmed.
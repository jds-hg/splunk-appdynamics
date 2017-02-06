# splunk-appdynamics
Splunk Add-on &amp; App for AppDynamics


## What's Needed?
- Downloads
    - Splunk Add-on for AppDynamics
    - Splunk App for AppDynamics


- AppDynamics Information
    - AppDynamics Collector URL (host & port)
    - AppDynamics Authorization Token
    
**Note:** Your AppDynamics Authorization Token is created by endocding your userid, password and account secret in a base64 hash.
To Create this token issue the following command from a *nix command line: 
```
echo -n 'user@customer1:secret' | base64
```
Save the resulting output. This will be your Authorization token.

More details can be found on the AppDynamics website here:
https://docs.appdynamics.com/display/PRO42/Using+the+Controller+APIs#UsingtheControllerAPIs-Authentication


## Installation
The installation consists of installing both the *Splunk Add-on for AppDynamics* and the *Splunk App for AppDynamics*.   The Add-on is responsible for executing the rest calls and collecting the data from AppDynamics.  The App provides the dashboards and saved searches.  To install, navigate to Apps --> Manage Apps and select the “Install app from File” button.  Specify the location of the file you downloaded and install.   

## Configuration
The Splunk Add-on for AppDynamics contains two separate input types:
- AppDynamics Summary
- Single API Call

In most cases you will only need to use the AppDynamics Summary input.  


## Start Searching
Once the Splunk Add-on for AppDynamics is installed and configured you can execute searches using: 
```
sourcetype="appdynamcis_summary"
```

----  

# Additional OPTIONAL Configurations
----
### Additional Inputs

#### Single AppDynamics API Call
In some cases you may not want all of the Summary data or you may only need a very specifc metric for a single application.  For these cases, use the AppDynamics Single API Call input type. In this case, you will also need to specify an application name, the url path and the specific metric path found in the AppDynamics Metric Browser.  While in the AppDynamics Metric Browser, identify the metric you would like to capture and right-click to copy the "Full Path".  This is the value you will use for an AppDynamics Single API Call data input. 

- Click the **Configure New Input** button and select **New Relic Single API Call**
- Enter your API call parameters and save

Now start searching using 
```
sourcetype="appdynamics_single_api_call”
```

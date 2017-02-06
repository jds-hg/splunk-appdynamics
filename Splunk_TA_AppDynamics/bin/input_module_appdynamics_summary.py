
# encoding = utf-8

import os
import sys
import time
import datetime

'''
    IMPORTANT
    Edit only the validate_input and collect_events functions.
    Do not edit any other part in this file.
    This file is generated only once when creating the modular input.
'''
'''
# For advanced users, if you want to create single instance mod input, uncomment this method.
def use_single_instance_mode():
    return True
'''

def validate_input(helper, definition):
    """Implement your own validation logic to validate the input stanza configurations"""
    # This example accesses the modular input variable
    # host_port = definition.parameters.get('host_port', None)
    # auth_token = definition.parameters.get('auth_token', None)
    # duration = definition.parameters.get('duration', None)
    # app_name = definition.parameters.get('app_name', None)
    pass

def collect_events(helper, ew):
    #Implement your data collection logic here


    import HTMLParser
    import json
    import urllib
    import requests


    '''
    Variable declarations and initializations
    '''

    #  Process each account input in inputs.conf separately
    #  Get the properties for each input (stanzas in inputs.conf)
    stanzas = helper.input_stanzas
    for stanza_name in stanzas:
        opt_host_port   = helper.get_arg('host_port')
        opt_auth_token  = helper.get_arg('auth_token')
        opt_duration    = helper.get_arg('duration')
        opt_app_name    = helper.get_arg('app_name')
        #helper.log_info(' = '.join(['opt_app_name', str(opt_app_name)]))
        idx = helper.get_output_index()
        st = helper.get_sourcetype()

        # If there are more than 1 input of this type, the arguments will be in a dictionary so grab them out
        if type(opt_auth_token) == dict:
            opt_host_port   = opt_host_port[stanza_name]
        if type(opt_auth_token) == dict:
            opt_auth_token  = opt_auth_token[stanza_name]
        if type(opt_duration) == dict:
            opt_duration    = opt_duration[stanza_name]
        if type(idx) == dict:
            idx = idx[stanza_name]
        if type(st) == dict:
            st = st[stanza_name]

        #  app_name is optional so we need to account for the fact that it may not exist
        if type(opt_app_name) == dict:
            opt_app_name = opt_app_name[stanza_name]

        #headers = {'Authorization':'Basic YmFzaWNAY3VzdG9tZXIxOnczbGNvbWU='}
        headers =  {'Authorization': 'Basic {}'.format(opt_auth_token)}
        parameters = "output=JSON&time-range-type=BEFORE_NOW&duration-in-mins=" + opt_duration
        api_url = opt_host_port + "/controller/rest/applications"

    '''
    End of Variable declarations and initializations
    '''

    
    # Remove any metric elements that have a metricName of 'METRIC DATA NOT FOUND'
    def del_empty_items(d):
        for key, val in d.items():
            if isinstance(val, list):
                for i in reversed(range(len(val))):
                    if val[i].get('metricName') == "METRIC DATA NOT FOUND":
                        val.pop(i)
        return


    def parse_piped_naming(d):
        for key, val in d.items():  
            #  let's parse out the metricPath from into component parts.  This will make our lives a little easier in Splunk ;-).
            if isinstance(val, list):
                for metrics in val:
                    for key2, val2 in metrics.items():
                        if key2 == "metricPath":
                            parts = val2.split("|")
                            for i in range(len(parts)):
                                partName = "path-part-" + str(i+1)
                                metrics[partName] = "{}".format(parts[i])
        return



    
    #  get the list of all applications so that we can add app_id and app_name to the event.
    #  This enables us to build a url back into AppDynamics.
    def get_application_list():
        response = helper.send_http_request(api_url, "GET", headers=headers,  parameters=parameters, payload=None, cookies=None, verify=None, cert=None, timeout=None, use_proxy=True)

        # check the response status, if the status is not sucessful, raise requests.HTTPError
        r_status = response.status_code
        response.raise_for_status()
        application_list = response.json()
        return application_list;


    # Given an application name, let's find it's ID
    def get_app_id(app_name):
        for app in application_list:
            if app["name"] == app_name:
                return app['id'];
        return -1;


    # Execute a REST API Call to get data for a single application
    # Example url = "https://host:port/controller/rest/applications/<app_name>/metric-data?metric-path=Business Transaction Performance|*|*|*|*"
    def get_api_data(app_id, app_name, url, params, key_name):
        response = helper.send_http_request(url, "GET", headers=headers,  parameters=params, payload=None, cookies=None, verify=None, cert=None, timeout=None, use_proxy=True)

        # check the response status, if the status is not sucessful, raise requests.HTTPError
        r_status = response.status_code
        response.raise_for_status()

        # get the response data
        r_json = response.json()
        
        # if there's no data, let's just stop right here and move to the next one.
        if not r_json:
            return;


        #  add the application ID & Name to the event so we can link back to AppDynamics in the UI
        app_dict =  {'application_name': '{}'.format(app_name), 'application_id' : app_id }
        app_dict[key_name] = r_json
        data = json.loads(json.dumps(app_dict))
 
        #  if there are empty elements, let's get rid of those.
        del_empty_items(data)
        #parse_piped_naming(data)

        
        #   Now write the event to Splunk
        event = helper.new_event(source=key_name, index=idx, sourcetype=st, data=json.dumps(data,sort_keys=True))
        try:
            ew.write_event(event)
        except Exception as e:
            raise e
        return;


    # This is where we define what data we would like ot pull back from Appdynamics
    def get_app_metrics(app_id, app_name):
        helper.log_info("processing app_id:" + app_id + "    app_name:" + app_name)

        # Application Infrastructure Performance Metrics
        api_url = opt_host_port + "/controller/rest/applications/" + app_name + "/metric-data"
        params  = parameters + "&metric-path=Application Infrastructure Performance|*|*|*|*"
        get_api_data( app_id, app_name, api_url, params, "infrastructure_performance" )

        # Overall Application Performance Metrics
        api_url = opt_host_port + "/controller/rest/applications/" + app_name + "/metric-data"
        params  = parameters + "&metric-path=Overall Application Performance|*"
        get_api_data( app_id, app_name, api_url, params, "application_performance" )

        # Busienss Transaction Metrics
        api_url = opt_host_port + "/controller/rest/applications/" + app_name + "/metric-data"
        params  = parameters + "&metric-path=Business Transaction Performance|*|*|*|*"
        get_api_data( app_id, app_name, api_url, params, "business_transactions" )

        # Healthrule Violations
        api_url = opt_host_port + "/controller/rest/applications/" + app_name + "/problems/healthrule-violations"
        params  = parameters
        get_api_data( app_id, app_name, api_url, params, "healthrule_violations" )

        # Application Event 
        api_url = opt_host_port + "/controller/rest/applications/" + app_name + "/events"
        params  = parameters + "&event-types=APPLICATION_ERROR,DIAGNOSTIC_SESSION&severities=INFO,WARN,ERROR"
        get_api_data( app_id, app_name, api_url, params, "application_events" )

        return;


    '''
    Begin processing logic
    '''
    # Get a list of all applications in AppDynamics
    application_list = get_application_list()

    # Are we getting data for ALL applications or one specific app?      (does the input specify an app name?)
    if (opt_app_name is None ):
        # We want to grab all data for all applications in AppDynamics
        for app in application_list:
            get_app_metrics(str(app['id']),str(app['name']))
    else:
        #  We want 1 specific application from AppDynamics
        app_id = str(get_app_id(opt_app_name))
        get_app_metrics(app_id, opt_app_name)



















    """
    # The following examples get the arguments of this input.
    # Note, for single instance mod input, args will be returned as a dict.
    # For multi instance mod input, args will be returned as a single value.
    opt_host_port = helper.get_arg('host_port')
    opt_auth_token = helper.get_arg('auth_token')
    opt_duration = helper.get_arg('duration')
    opt_app_name = helper.get_arg('app_name')
    # In single instance mode, to get arguments of a particular input, use
    opt_host_port = helper.get_arg('host_port', stanza_name)
    opt_auth_token = helper.get_arg('auth_token', stanza_name)
    opt_duration = helper.get_arg('duration', stanza_name)
    opt_app_name = helper.get_arg('app_name', stanza_name)

    # get input type
    helper.get_input_type()

    # The following examples get input stanzas.
    # get all detailed input stanzas
    helper.get_input_stanza()
    # get specific input stanza with stanza name
    helper.get_input_stanza(stanza_name)
    # get all stanza names
    helper.get_input_stanza_names()

    # The following examples get options from setup page configuration.
    # get the loglevel from the setup page
    loglevel = helper.get_log_level()
    # get proxy setting configuration
    proxy_settings = helper.get_proxy()
    # get user credentials
    account = helper.get_user_credential_by_username("username")
    account = helper.get_user_credential_by_id("account id")
    # get global variable configuration
    global_userdefined_global_var = helper.get_global_setting("userdefined_global_var")

    # The following examples show usage of logging related helper functions.
    # write to the log for this modular input using configured global log level or INFO as default
    helper.log("log message")
    # write to the log using specified log level
    helper.log_debug("log message")
    helper.log_info("log message")
    helper.log_warning("log message")
    helper.log_error("log message")
    helper.log_critical("log message")
    # set the log level for this modular input
    # (log_level can be "debug", "info", "warning", "error" or "critical", case insensitive)
    helper.set_log_level(log_level)

    # The following examples send rest requests to some endpoint.
    response = helper.send_http_request(url, method, parameters=None, payload=None,
                                        headers=None, cookies=None, verify=True, cert=None,
                                        timeout=None, use_proxy=True)
    # get the response headers
    r_headers = response.headers
    # get the response body as text
    r_text = response.text
    # get response body as json. If the body text is not a json string, raise a ValueError
    r_json = response.json()
    # get response cookies
    r_cookies = response.cookies
    # get redirect history
    historical_responses = response.history
    # get response status code
    r_status = response.status_code
    # check the response status, if the status is not sucessful, raise requests.HTTPError
    response.raise_for_status()

    # The following examples show usage of check pointing related helper functions.
    # save checkpoint
    helper.save_check_point(key, state)
    # delete checkpoint
    helper.delete_check_point(key)
    # get checkpoint
    state = helper.get_check_point(key)

    # To create a splunk event
    helper.new_event(data, time=None, host=None, index=None, source=None, sourcetype=None, done=True, unbroken=True)
    """

    '''
    # The following example writes a random number as an event. (Multi Instance Mode)
    # Use this code template by default.
    import random
    data = str(random.randint(0,100))
    event = helper.new_event(source=helper.get_input_type(), index=helper.get_output_index(), sourcetype=helper.get_sourcetype(), data=data)
    ew.write_event(event)
    '''

    '''
    # The following example writes a random number as an event for each input config. (Single Instance Mode)
    # For advanced users, if you want to create single instance mod input, please use this code template.
    # Also, you need to uncomment use_single_instance_mode() above.
    import random
    input_type = helper.get_input_type()
    for stanza_name in helper.get_input_stanza_names():
        data = str(random.randint(0,100))
        event = helper.new_event(source=input_type, index=helper.get_output_index(stanza_name), sourcetype=helper.get_sourcetype(stanza_name), data=data)
        ew.write_event(event)
    '''

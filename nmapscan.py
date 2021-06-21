from pprint import pprint
import json 
from kubernetes.stream import stream
from kubernetes import client, config
import json
import sys
import yaml
import datetime

def append_value(dict_obj, key, value):
    # Check if key exist in dict or not
    if key in dict_obj:
        # Key exist in dict.
        # Check if type of value of key is list or not
        if not isinstance(dict_obj[key], list):
            # If type is not list then make it list
            dict_obj[key] = [dict_obj[key]]
        # Append the value in list
        dict_obj[key].append(value)
    else:
        # As key is not in dict,
        # so, add key-value pair
        dict_obj[key] = value
def nmapScanner(data):

    apply=client.CustomObjectsApi()
     # apply nmap scan
    apply.create_namespaced_custom_object(
        group="execution.securecodebox.io",
        version="v1",
        namespace="default",
        plural="scans",
        body=data,
    )

def nmapIp(podList):
    data={
        'apiVersion': 'execution.securecodebox.io/v1',
        'kind': 'Scan',
        'metadata':
        {
            'name': 'nmap-scan' 
        },
        'spec':
        {
            'scanType': 'nmap',
            'parameters':[
            ]
        }
    }
    for i in podList.items:
        if i.status.pod_ip :
            append_value(data['spec'],'parameters',i.status.pod_ip)

    x = datetime.datetime.now().strftime("%d-%m-%Y-%I-%M")
    data['metadata'].update({'name': 'nmap-scan-'+x})
    
    nmapScanner(data)

    


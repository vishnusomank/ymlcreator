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

def zapScanner(data):

    apply=client.CustomObjectsApi()
    # apply zap scan
    apply.create_namespaced_custom_object(
        group="execution.securecodebox.io",
        version="v1",
        namespace="default",
        plural="scans",
        body=data,
    )
    
    pprint(data)

def zapIp(svcList):
    data={}
    for i in svcList.items:
        if i.status.load_balancer.ingress:
            for j in range(0,len(i.spec.ports)):
                data={
                'apiVersion': 'execution.securecodebox.io/v1',
                'kind': 'Scan',
                'metadata':
                {
                    'name': 'zap-scan' 
                },
                'spec':
                {
                    'scanType': 'zap-full-scan',
                    'parameters':[
                        '-t'
                    ]
                }
                }
                append_value(data['spec'],'parameters',"http://"+i.status.load_balancer.ingress[0].ip+":"+str(i.spec.ports[j].port))
                data['metadata'].update({'name': 'zap-scan-'+i.status.load_balancer.ingress[0].ip+"-"+str(i.spec.ports[j].port)})
                zapScanner(data)

    


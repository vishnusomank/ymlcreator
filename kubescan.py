from pprint import pprint
import json 
from kubernetes.stream import stream
from kubernetes import client, config
import json
import sys
import yaml
import datetime

def kubeScanner():

  data={
    'apiVersion': 'execution.securecodebox.io/v1',
    'kind': 'Scan',
    'metadata':
    {
        'name': 'kube-hunter-incluster' 
    },
    'spec':
    {
      'scanType': 'kube-hunter',
      'parameters':[
        '--pod'
      ]
    }
  }
  apply=client.CustomObjectsApi()
  # apply kubehunter scan
  apply.create_namespaced_custom_object(
        group="execution.securecodebox.io",
        version="v1",
        namespace="default",
        plural="scans",
        body=data,
  )
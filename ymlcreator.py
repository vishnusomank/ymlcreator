from pprint import pprint
import json 
from kubernetes.stream import stream
from kubernetes import client, config, utils
import json
import sys
import yaml
import nmapscan
import zapscan
import kubescan



def main():
    config.load_kube_config()

    v1 = client.CoreV1Api()
    print("SecureCodeBox Scan Started ")
    podList = v1.list_pod_for_all_namespaces(watch=False)   
    svcList = v1.list_service_for_all_namespaces(watch=False)
    nmapscan.nmapIp(podList)
    zapscan.zapIp(svcList)
    kubescan.kubeScanner()
if  __name__ == "__main__":
    main()
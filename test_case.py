from pprint import pprint
import json 
from kubernetes.stream import stream
from kubernetes import client, config
import json
import sys
import yaml
import time
import policy_check_v1
import policy_check

def testFramework():
    pass

def pingTestFramework(pod1,pod2,policyName,nameSpace,labels):
    s_count=1
    p1_success= p2_success = False
    config.load_kube_config()
    api=client.CoreV1Api()
    
    print()
    print("Case #"+policyName)
    print()
    nameSpace=nameSpace.strip()
    labels=labels.strip()
    pod_1 = api.list_namespaced_pod(nameSpace,label_selector=labels)
    pod_2 = api.read_namespaced_pod_status(pod1.metadata.name,pod1.metadata.namespace)
    pod_3 = api.read_namespaced_pod_status(pod2.metadata.name,pod2.metadata.namespace)
    '''
    #pod_3 = api.read_namespaced_pod_status(pod3.metadata.name,pod3.metadata.namespace)
    while pod_1.status.pod_ip == None or pod_2.status.pod_ip == None :
        pod_1 = api.read_namespaced_pod_status(pod1.metadata.name,pod1.metadata.namespace)
        pod_2 = api.read_namespaced_pod_status(pod2.metadata.name,pod2.metadata.namespace)
        #pod_3 = api.read_namespaced_pod_status(pod3.metadata.name,pod3.metadata.namespace)
    '''
    for i in pod_1.items:
        pod_cmd = [ '/bin/sh','-c', 'ping -c 4 '+i.status.pod_ip ]
        try:
            print("\t#"+str(s_count)+" ==> Establishing connection from ",pod1.metadata.name," to ",i.metadata.name,end=" ")
            print("in namespace ",i.metadata.namespace)
            api_response = stream(api.connect_get_namespaced_pod_exec,pod_2.metadata.name, pod_2.metadata.namespace, command=pod_cmd,stderr=True, stdin=False, stdout=True, tty=False)
            if api_response.find('4 packets transmitted, 4 packets received, 0% packet loss') != -1:
                print('\tStatus : OK\n\tConnection Established\n')
                p1_success=True
            else:
                print('\tStatus : FAILED\n\tConnection Failed\n')
                p1_success=False
            s_count+=1
            print("\t#"+str(s_count)+" ==> Establishing connection from  ",pod2.metadata.name," to ",i.metadata.name,end=" ")
            print("in namespace ",i.metadata.namespace)
            s_count+=1
            api_response = stream(api.connect_get_namespaced_pod_exec,pod_3.metadata.name, pod_3.metadata.namespace, command=pod_cmd,stderr=True, stdin=False, stdout=True, tty=False)
            if api_response.find('4 packets transmitted, 0 packets received, 100% packet loss') != -1:
                print('\tStatus : FAILED\n\tConnection Dropped\n')
                p2_success=True
            else:
                print('\tStatus : OK\n\tConnection Established\n')
                p2_success=False
        except Exception as e:
            p1_success = p2_success=False
            print(e)
    if p1_success== True and p2_success == True:
        print("\n\tFinal Verdict: "+policyName+"\n\tPOLICY VALIDATION : SUCCESS\n")
    else:
        print("\n\tFinal Verdict: "+policyName+"\n\tPOLICY VALIDATION : FAILURE\n")



def curlTestFramework(pod1,pod2,policyName,port, protocol,ruleType, method, path, headers,nameSpace,labels):
    s_count=1
    p1_success= p2_success = False
    api=client.CoreV1Api()
    print()
    print("POLICY #"+policyName)
    print()
    pod_1 = api.list_namespaced_pod(nameSpace,label_selector=labels)
    pod_2 = api.read_namespaced_pod_status(pod1.metadata.name,pod1.metadata.namespace)
    pod_3 = api.read_namespaced_pod_status(pod2.metadata.name,pod2.metadata.namespace)
    
    for i in pod_1.items:
        if method == "GET" and path != "":
            pod_cmd = [ '/bin/sh','-c', 'curl -s --header '+headers+ruleType+"://"+i.status.pod_ip+port+":"+path ]
        elif method == "POST" and path != "" :
            pod_cmd = [ '/bin/sh','-c', 'curl -s -XPOST --header '+headers+ruleType+"://"+i.status.pod_ip+port+":"+path ]
        else:
            pod_cmd = [ '/bin/sh','-c', 'curl -s '+ruleType+"://"+i.status.pod_ip+":"+port ]
    
        try:
            print("\t#"+str(s_count)+" ==> Establishing connection from ",pod1.metadata.name," to ",i.metadata.name,end=" ")
            print("in namespace ",i.metadata.namespace)
            api_response = stream(api.connect_get_namespaced_pod_exec,pod_2.metadata.name, pod_2.metadata.namespace, command=pod_cmd,stderr=True, stdin=False, stdout=True, tty=False)
            print(api_response)
            if api_response.find('command terminated') != -1:
                print('\tStatus : FAILED\n\tConnection Failed\n')
                p1_success=False
            else:
                print('\tStatus : OK\n\tConnection Established\n')
                p1_success=True
            s_count+=1
            print("\t#"+str(s_count)+" ==> Establishing connection from  ",pod2.metadata.name," to ",i.metadata.name,end=" ")
            print("in namespace ",i.metadata.namespace)
            s_count+=1
            api_response = stream(api.connect_get_namespaced_pod_exec,pod_3.metadata.name, pod_3.metadata.namespace, command=pod_cmd,stderr=True, stdin=False, stdout=True, tty=False)
            print(api_response)
            if api_response.find('command terminated') != -1:
                print('\tStatus : FAILED\n\tConnection Failed\n')
                p2_success=False
            else:
                print('\tStatus : OK\n\tConnection Established\n')
                p2_success=True
        except Exception as e:
            p1_success = p2_success=False
            print(e)
    if p1_success== True and p2_success == True:
        print("\n\tFinal Verdict: "+policyName+"\n\tPOLICY VALIDATION : SUCCESS\n")
    else:
        print("\n\tFinal Verdict: "+policyName+"\n\tPOLICY VALIDATION : FAILURE\n")
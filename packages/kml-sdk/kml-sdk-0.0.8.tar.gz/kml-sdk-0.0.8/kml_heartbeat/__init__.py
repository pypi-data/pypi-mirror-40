import os
import time
import etcd3

etcd_hosts = ['10.48.55.169','10.48.55.179','10.48.56.149','10.48.56.159','10.48.56.169']

client=etcd3.client(host=etcd_hosts[0],ca_cert='/etcd/ca.pem',cert_key='/etcd/etcd-key.pem',cert_cert='/etcd/etcd.pem')

def heartbeat(timeout, operation="alert"):
    global client
    retry_time = 0
    while True:
        try:
            client.put('/kml/production/heartbeat/job/'+os.environ['KML_ID'], "%d %d %s" % (time.time(), timeout, operation))
            return True
        except etcd3.exceptions.ConnectionFailedError as e:
            if retry_time == len(etcd_hosts):
                raise e
            client=etcd3.client(host=etcd_hosts[retry_time],ca_cert='/etcd/ca.pem',cert_key='/etcd/etcd-key.pem',cert_cert='/etcd/etcd.pem')
            retry_time = retry_time+1

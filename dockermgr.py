import docker

client = docker.Client(base_url='unix://var/run/docker.sock', version="1.4", timeout=60)

def create_container():
	return client.create_container('spltopic', command="/root/node-v0.10.22-linux-x64/bin/node /root/ipshow/app.js")

def onspect_container(container):
	return client.inspect_container(container)

def get_container_ip(container):
	info = client.inspect_container(container)
	return info['NetworkSettings']['IPAddress']

def get_container_id(container):
	info = client.inspect_container(container)
	return info['Config']['Hostname']
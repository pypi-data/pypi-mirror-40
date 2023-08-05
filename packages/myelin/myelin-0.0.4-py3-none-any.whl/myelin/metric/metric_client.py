from __future__ import absolute_import
import os
from kubernetes import client, config
import requests

class MetricClientKubernetes(object):
	group = 'monitoring.coreos.com'
	version = 'v1'
	plural = 'prometheusrules'
	metric_prefix = "metric/"

	def __init__(self, config_file, port=9091):

		self.port = port

		config.load_kube_config(config_file=config_file)
		configuration = client.Configuration()
		configuration.verify_ssl = False
		configuration.debug = True

		client.Configuration.set_default(configuration)

		self.api_instance = client.CustomObjectsApi(client.ApiClient(configuration))
		self.v1 = client.CoreV1Api()

		self.namespace = os.environ["NAMESPACE"]
		self.task_id = os.environ["TASK_ID"]
		self.axon_id = os.environ["AXON_ID"]
		self.metrics = self.get_metrics(self.axon_id, self.namespace)
		self.url = "http://prometheus-pushgateway.{}:{}/metrics/job/{}/pod/".format(self.namespace, self.port, self.task_id)

	def get_metrics(self, name, namespace):
		ret = self.api_instance.get_namespaced_custom_object(group=MetricClientKubernetes.group,
															 version=MetricClientKubernetes.version,
															 plural=MetricClientKubernetes.plural,
															 namespace=namespace,
															 name=name)

		m = {k.split(self.metric_prefix)[1]: v for k, v in ret["metadata"]["labels"].items()
			 if k.startswith(self.metric_prefix)}

		return m

	def post_update(self, metric, value):
		internal_metric_name = self.metrics[metric]
		payload = "{} {}".format(internal_metric_name, value)
		res = requests.post(self.url, payload, headers={'Content-Type': 'application/octet-stream'})
		return res


class MetricClient(object):

	def __init__(self, port=9091):
		self.port = port
		self.namespace = os.environ["NAMESPACE"]
		self.task_id = os.environ["TASK_ID"]
		self.axon_id = os.environ["AXON_ID"]
		self.url = "http://prometheus-pushgateway.{}:{}/metrics/job/{}/pod/".format(self.namespace, self.port, self.task_id)

	def get_metric(self, name):
		metric = "{}_{}".format(name, self.axon_id)
		return metric.replace("-", "__")

	def post_update(self, metric, value):
		internal_metric = self.get_metric(metric)
		payload = "{} {}\n".format(internal_metric, value)
		res = requests.post(url=self.url, data=payload,
							headers={'Content-Type': 'application/x-www-form-urlencoded'})
		print(res.text)
		return res
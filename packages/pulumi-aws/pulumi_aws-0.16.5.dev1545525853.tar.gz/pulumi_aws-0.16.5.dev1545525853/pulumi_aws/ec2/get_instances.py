# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime
from .. import utilities, tables

class GetInstancesResult(object):
    """
    A collection of values returned by getInstances.
    """
    def __init__(__self__, ids=None, instance_tags=None, private_ips=None, public_ips=None, id=None):
        if ids and not isinstance(ids, list):
            raise TypeError('Expected argument ids to be a list')
        __self__.ids = ids
        """
        IDs of instances found through the filter
        """
        if instance_tags and not isinstance(instance_tags, dict):
            raise TypeError('Expected argument instance_tags to be a dict')
        __self__.instance_tags = instance_tags
        if private_ips and not isinstance(private_ips, list):
            raise TypeError('Expected argument private_ips to be a list')
        __self__.private_ips = private_ips
        """
        Private IP addresses of instances found through the filter
        """
        if public_ips and not isinstance(public_ips, list):
            raise TypeError('Expected argument public_ips to be a list')
        __self__.public_ips = public_ips
        """
        Public IP addresses of instances found through the filter
        """
        if id and not isinstance(id, str):
            raise TypeError('Expected argument id to be a str')
        __self__.id = id
        """
        id is the provider-assigned unique ID for this managed resource.
        """

async def get_instances(filters=None, instance_state_names=None, instance_tags=None):
    """
    Use this data source to get IDs or IPs of Amazon EC2 instances to be referenced elsewhere,
    e.g. to allow easier migration from another management solution
    or to make it easier for an operator to connect through bastion host(s).
    
    -> **Note:** It's a best practice to expose instance details via [outputs](https://www.terraform.io/docs/configuration/outputs.html)
    and [remote state](https://www.terraform.io/docs/state/remote.html) and
    **use [`terraform_remote_state`](https://www.terraform.io/docs/providers/terraform/d/remote_state.html)
    data source instead** if you manage referenced instances via Terraform.
    
    > **Note:** It's strongly discouraged to use this data source for querying ephemeral
    instances (e.g. managed via autoscaling group), as the output may change at any time
    and you'd need to re-run `apply` every time an instance comes up or dies.
    """
    __args__ = dict()

    __args__['filters'] = filters
    __args__['instanceStateNames'] = instance_state_names
    __args__['instanceTags'] = instance_tags
    __ret__ = await pulumi.runtime.invoke('aws:ec2/getInstances:getInstances', __args__)

    return GetInstancesResult(
        ids=__ret__.get('ids'),
        instance_tags=__ret__.get('instanceTags'),
        private_ips=__ret__.get('privateIps'),
        public_ips=__ret__.get('publicIps'),
        id=__ret__.get('id'))

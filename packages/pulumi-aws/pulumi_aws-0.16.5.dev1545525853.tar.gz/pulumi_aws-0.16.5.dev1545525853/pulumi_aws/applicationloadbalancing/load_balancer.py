# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime
from .. import utilities, tables

class LoadBalancer(pulumi.CustomResource):
    """
    Provides a Load Balancer resource.
    
    > **Note:** `aws_alb` is known as `aws_lb`. The functionality is identical.
    """
    def __init__(__self__, __name__, __opts__=None, access_logs=None, enable_cross_zone_load_balancing=None, enable_deletion_protection=None, enable_http2=None, idle_timeout=None, internal=None, ip_address_type=None, load_balancer_type=None, name=None, name_prefix=None, security_groups=None, subnet_mappings=None, subnets=None, tags=None):
        """Create a LoadBalancer resource with the given unique name, props, and options."""
        if not __name__:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(__name__, str):
            raise TypeError('Expected resource name to be a string')
        if __opts__ and not isinstance(__opts__, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        __props__['access_logs'] = access_logs

        __props__['enable_cross_zone_load_balancing'] = enable_cross_zone_load_balancing

        __props__['enable_deletion_protection'] = enable_deletion_protection

        __props__['enable_http2'] = enable_http2

        __props__['idle_timeout'] = idle_timeout

        __props__['internal'] = internal

        __props__['ip_address_type'] = ip_address_type

        __props__['load_balancer_type'] = load_balancer_type

        __props__['name'] = name

        __props__['name_prefix'] = name_prefix

        __props__['security_groups'] = security_groups

        __props__['subnet_mappings'] = subnet_mappings

        __props__['subnets'] = subnets

        __props__['tags'] = tags

        __props__['arn'] = None
        __props__['arn_suffix'] = None
        __props__['dns_name'] = None
        __props__['vpc_id'] = None
        __props__['zone_id'] = None

        super(LoadBalancer, __self__).__init__(
            'aws:applicationloadbalancing/loadBalancer:LoadBalancer',
            __name__,
            __props__,
            __opts__)


    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop


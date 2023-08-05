# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime
from .. import utilities, tables

class NatGateway(pulumi.CustomResource):
    """
    Provides a resource to create a VPC NAT Gateway.
    """
    def __init__(__self__, __name__, __opts__=None, allocation_id=None, subnet_id=None, tags=None):
        """Create a NatGateway resource with the given unique name, props, and options."""
        if not __name__:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(__name__, str):
            raise TypeError('Expected resource name to be a string')
        if __opts__ and not isinstance(__opts__, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        if not allocation_id:
            raise TypeError('Missing required property allocation_id')
        __props__['allocation_id'] = allocation_id

        if not subnet_id:
            raise TypeError('Missing required property subnet_id')
        __props__['subnet_id'] = subnet_id

        __props__['tags'] = tags

        __props__['network_interface_id'] = None
        __props__['private_ip'] = None
        __props__['public_ip'] = None

        super(NatGateway, __self__).__init__(
            'aws:ec2/natGateway:NatGateway',
            __name__,
            __props__,
            __opts__)


    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop


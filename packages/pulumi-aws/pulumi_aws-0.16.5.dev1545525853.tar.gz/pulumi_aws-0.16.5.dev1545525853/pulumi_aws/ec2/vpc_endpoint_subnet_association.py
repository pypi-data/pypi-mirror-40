# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime
from .. import utilities, tables

class VpcEndpointSubnetAssociation(pulumi.CustomResource):
    """
    Provides a resource to create an association between a VPC endpoint and a subnet.
    
    > **NOTE on VPC Endpoints and VPC Endpoint Subnet Associations:** Terraform provides
    both a standalone VPC Endpoint Subnet Association (an association between a VPC endpoint
    and a single `subnet_id`) and a VPC Endpoint resource with a `subnet_ids`
    attribute. Do not use the same subnet ID in both a VPC Endpoint resource and a VPC Endpoint Subnet
    Association resource. Doing so will cause a conflict of associations and will overwrite the association.
    """
    def __init__(__self__, __name__, __opts__=None, subnet_id=None, vpc_endpoint_id=None):
        """Create a VpcEndpointSubnetAssociation resource with the given unique name, props, and options."""
        if not __name__:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(__name__, str):
            raise TypeError('Expected resource name to be a string')
        if __opts__ and not isinstance(__opts__, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        if not subnet_id:
            raise TypeError('Missing required property subnet_id')
        __props__['subnet_id'] = subnet_id

        if not vpc_endpoint_id:
            raise TypeError('Missing required property vpc_endpoint_id')
        __props__['vpc_endpoint_id'] = vpc_endpoint_id

        super(VpcEndpointSubnetAssociation, __self__).__init__(
            'aws:ec2/vpcEndpointSubnetAssociation:VpcEndpointSubnetAssociation',
            __name__,
            __props__,
            __opts__)


    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop


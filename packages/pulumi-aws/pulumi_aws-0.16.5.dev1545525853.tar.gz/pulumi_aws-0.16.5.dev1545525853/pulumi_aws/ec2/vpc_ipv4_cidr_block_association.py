# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime
from .. import utilities, tables

class VpcIpv4CidrBlockAssociation(pulumi.CustomResource):
    """
    Provides a resource to associate additional IPv4 CIDR blocks with a VPC.
    
    When a VPC is created, a primary IPv4 CIDR block for the VPC must be specified.
    The `aws_vpc_ipv4_cidr_block_association` resource allows further IPv4 CIDR blocks to be added to the VPC.
    """
    def __init__(__self__, __name__, __opts__=None, cidr_block=None, vpc_id=None):
        """Create a VpcIpv4CidrBlockAssociation resource with the given unique name, props, and options."""
        if not __name__:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(__name__, str):
            raise TypeError('Expected resource name to be a string')
        if __opts__ and not isinstance(__opts__, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        if not cidr_block:
            raise TypeError('Missing required property cidr_block')
        __props__['cidr_block'] = cidr_block

        if not vpc_id:
            raise TypeError('Missing required property vpc_id')
        __props__['vpc_id'] = vpc_id

        super(VpcIpv4CidrBlockAssociation, __self__).__init__(
            'aws:ec2/vpcIpv4CidrBlockAssociation:VpcIpv4CidrBlockAssociation',
            __name__,
            __props__,
            __opts__)


    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop


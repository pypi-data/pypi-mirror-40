# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime
from .. import utilities, tables

class NetworkAcl(pulumi.CustomResource):
    """
    Provides an network ACL resource. You might set up network ACLs with rules similar
    to your security groups in order to add an additional layer of security to your VPC.
    
    ~> **NOTE on Network ACLs and Network ACL Rules:** Terraform currently
    provides both a standalone Network ACL Rule resource and a Network ACL resource with rules
    defined in-line. At this time you cannot use a Network ACL with in-line rules
    in conjunction with any Network ACL Rule resources. Doing so will cause
    a conflict of rule settings and will overwrite rules.
    """
    def __init__(__self__, __name__, __opts__=None, egress=None, ingress=None, subnet_id=None, subnet_ids=None, tags=None, vpc_id=None):
        """Create a NetworkAcl resource with the given unique name, props, and options."""
        if not __name__:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(__name__, str):
            raise TypeError('Expected resource name to be a string')
        if __opts__ and not isinstance(__opts__, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        __props__['egress'] = egress

        __props__['ingress'] = ingress

        __props__['subnet_id'] = subnet_id

        __props__['subnet_ids'] = subnet_ids

        __props__['tags'] = tags

        if not vpc_id:
            raise TypeError('Missing required property vpc_id')
        __props__['vpc_id'] = vpc_id

        __props__['owner_id'] = None

        super(NetworkAcl, __self__).__init__(
            'aws:ec2/networkAcl:NetworkAcl',
            __name__,
            __props__,
            __opts__)


    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop


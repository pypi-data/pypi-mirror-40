# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime
from .. import utilities, tables

class Agent(pulumi.CustomResource):
    """
    Manages an AWS DataSync Agent deployed on premises.
    
    > **NOTE:** One of `activation_key` or `ip_address` must be provided for resource creation (agent activation). Neither is required for resource import. If using `ip_address`, Terraform must be able to make an HTTP (port 80) GET request to the specified IP address from where it is running. The agent will turn off that HTTP server after activation.
    """
    def __init__(__self__, __name__, __opts__=None, activation_key=None, ip_address=None, name=None, tags=None):
        """Create a Agent resource with the given unique name, props, and options."""
        if not __name__:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(__name__, str):
            raise TypeError('Expected resource name to be a string')
        if __opts__ and not isinstance(__opts__, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        __props__['activation_key'] = activation_key

        __props__['ip_address'] = ip_address

        __props__['name'] = name

        __props__['tags'] = tags

        __props__['arn'] = None

        super(Agent, __self__).__init__(
            'aws:datasync/agent:Agent',
            __name__,
            __props__,
            __opts__)


    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop


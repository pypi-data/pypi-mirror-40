# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime
from .. import utilities, tables

class VpcEndpointConnectionNotification(pulumi.CustomResource):
    """
    Provides a VPC Endpoint connection notification resource.
    Connection notifications notify subscribers of VPC Endpoint events.
    """
    def __init__(__self__, __name__, __opts__=None, connection_events=None, connection_notification_arn=None, vpc_endpoint_id=None, vpc_endpoint_service_id=None):
        """Create a VpcEndpointConnectionNotification resource with the given unique name, props, and options."""
        if not __name__:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(__name__, str):
            raise TypeError('Expected resource name to be a string')
        if __opts__ and not isinstance(__opts__, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        if not connection_events:
            raise TypeError('Missing required property connection_events')
        __props__['connection_events'] = connection_events

        if not connection_notification_arn:
            raise TypeError('Missing required property connection_notification_arn')
        __props__['connection_notification_arn'] = connection_notification_arn

        __props__['vpc_endpoint_id'] = vpc_endpoint_id

        __props__['vpc_endpoint_service_id'] = vpc_endpoint_service_id

        __props__['notification_type'] = None
        __props__['state'] = None

        super(VpcEndpointConnectionNotification, __self__).__init__(
            'aws:ec2/vpcEndpointConnectionNotification:VpcEndpointConnectionNotification',
            __name__,
            __props__,
            __opts__)


    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop


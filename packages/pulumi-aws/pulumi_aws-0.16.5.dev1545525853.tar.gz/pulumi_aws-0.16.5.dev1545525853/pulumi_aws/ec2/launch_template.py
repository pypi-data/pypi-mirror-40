# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime
from .. import utilities, tables

class LaunchTemplate(pulumi.CustomResource):
    """
    Provides an EC2 launch template resource. Can be used to create instances or auto scaling groups.
    """
    def __init__(__self__, __name__, __opts__=None, block_device_mappings=None, capacity_reservation_specification=None, credit_specification=None, description=None, disable_api_termination=None, ebs_optimized=None, elastic_gpu_specifications=None, iam_instance_profile=None, image_id=None, instance_initiated_shutdown_behavior=None, instance_market_options=None, instance_type=None, kernel_id=None, key_name=None, license_specifications=None, monitoring=None, name=None, name_prefix=None, network_interfaces=None, placement=None, ram_disk_id=None, security_group_names=None, tag_specifications=None, tags=None, user_data=None, vpc_security_group_ids=None):
        """Create a LaunchTemplate resource with the given unique name, props, and options."""
        if not __name__:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(__name__, str):
            raise TypeError('Expected resource name to be a string')
        if __opts__ and not isinstance(__opts__, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        __props__['block_device_mappings'] = block_device_mappings

        __props__['capacity_reservation_specification'] = capacity_reservation_specification

        __props__['credit_specification'] = credit_specification

        __props__['description'] = description

        __props__['disable_api_termination'] = disable_api_termination

        __props__['ebs_optimized'] = ebs_optimized

        __props__['elastic_gpu_specifications'] = elastic_gpu_specifications

        __props__['iam_instance_profile'] = iam_instance_profile

        __props__['image_id'] = image_id

        __props__['instance_initiated_shutdown_behavior'] = instance_initiated_shutdown_behavior

        __props__['instance_market_options'] = instance_market_options

        __props__['instance_type'] = instance_type

        __props__['kernel_id'] = kernel_id

        __props__['key_name'] = key_name

        __props__['license_specifications'] = license_specifications

        __props__['monitoring'] = monitoring

        __props__['name'] = name

        __props__['name_prefix'] = name_prefix

        __props__['network_interfaces'] = network_interfaces

        __props__['placement'] = placement

        __props__['ram_disk_id'] = ram_disk_id

        __props__['security_group_names'] = security_group_names

        __props__['tag_specifications'] = tag_specifications

        __props__['tags'] = tags

        __props__['user_data'] = user_data

        __props__['vpc_security_group_ids'] = vpc_security_group_ids

        __props__['arn'] = None
        __props__['default_version'] = None
        __props__['latest_version'] = None

        super(LaunchTemplate, __self__).__init__(
            'aws:ec2/launchTemplate:LaunchTemplate',
            __name__,
            __props__,
            __opts__)


    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop


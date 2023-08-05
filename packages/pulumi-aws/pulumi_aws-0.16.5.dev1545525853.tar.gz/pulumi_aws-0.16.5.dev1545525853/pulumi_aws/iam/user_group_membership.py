# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime
from .. import utilities, tables

class UserGroupMembership(pulumi.CustomResource):
    """
    Provides a resource for adding an [IAM User][2] to [IAM Groups][1]. This
    resource can be used multiple times with the same user for non-overlapping
    groups.
    
    To exclusively manage the users in a group, see the
    [`aws_iam_group_membership` resource][3].
    """
    def __init__(__self__, __name__, __opts__=None, groups=None, user=None):
        """Create a UserGroupMembership resource with the given unique name, props, and options."""
        if not __name__:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(__name__, str):
            raise TypeError('Expected resource name to be a string')
        if __opts__ and not isinstance(__opts__, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        if not groups:
            raise TypeError('Missing required property groups')
        __props__['groups'] = groups

        if not user:
            raise TypeError('Missing required property user')
        __props__['user'] = user

        super(UserGroupMembership, __self__).__init__(
            'aws:iam/userGroupMembership:UserGroupMembership',
            __name__,
            __props__,
            __opts__)


    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop


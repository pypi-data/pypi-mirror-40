# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime
from .. import utilities, tables

class Account(pulumi.CustomResource):
    """
    Provides a resource to create a member account in the current organization.
    
    > **Note:** Account management must be done from the organization's master account.
    
    !> **WARNING:** Deleting this Terraform resource will only remove an AWS account from an organization. Terraform will not close the account. The member account must be prepared to be a standalone account beforehand. See the [AWS Organizations documentation](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_accounts_remove.html) for more information.
    """
    def __init__(__self__, __name__, __opts__=None, email=None, iam_user_access_to_billing=None, name=None, role_name=None):
        """Create a Account resource with the given unique name, props, and options."""
        if not __name__:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(__name__, str):
            raise TypeError('Expected resource name to be a string')
        if __opts__ and not isinstance(__opts__, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        if not email:
            raise TypeError('Missing required property email')
        __props__['email'] = email

        __props__['iam_user_access_to_billing'] = iam_user_access_to_billing

        __props__['name'] = name

        __props__['role_name'] = role_name

        __props__['arn'] = None
        __props__['joined_method'] = None
        __props__['joined_timestamp'] = None
        __props__['status'] = None

        super(Account, __self__).__init__(
            'aws:organizations/account:Account',
            __name__,
            __props__,
            __opts__)


    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop


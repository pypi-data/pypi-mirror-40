# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime
from .. import utilities, tables

class ApplicationVersion(pulumi.CustomResource):
    """
    Provides an Elastic Beanstalk Application Version Resource. Elastic Beanstalk allows
    you to deploy and manage applications in the AWS cloud without worrying about
    the infrastructure that runs those applications.
    
    This resource creates a Beanstalk Application Version that can be deployed to a Beanstalk
    Environment.
    
    > **NOTE on Application Version Resource:**  When using the Application Version resource with multiple 
    Elastic Beanstalk Environments it is possible that an error may be returned
    when attempting to delete an Application Version while it is still in use by a different environment.
    To work around this you can:
    <ol>
    <li>Create each environment in a separate AWS account</li>
    <li>Create your `aws_elastic_beanstalk_application_version` resources with a unique names in your 
    Elastic Beanstalk Application. For example &lt;revision&gt;-&lt;environment&gt;.</li>
    </ol>
    """
    def __init__(__self__, __name__, __opts__=None, application=None, bucket=None, description=None, force_delete=None, key=None, name=None):
        """Create a ApplicationVersion resource with the given unique name, props, and options."""
        if not __name__:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(__name__, str):
            raise TypeError('Expected resource name to be a string')
        if __opts__ and not isinstance(__opts__, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        if not application:
            raise TypeError('Missing required property application')
        __props__['application'] = application

        if not bucket:
            raise TypeError('Missing required property bucket')
        __props__['bucket'] = bucket

        __props__['description'] = description

        __props__['force_delete'] = force_delete

        if not key:
            raise TypeError('Missing required property key')
        __props__['key'] = key

        __props__['name'] = name

        super(ApplicationVersion, __self__).__init__(
            'aws:elasticbeanstalk/applicationVersion:ApplicationVersion',
            __name__,
            __props__,
            __opts__)


    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop


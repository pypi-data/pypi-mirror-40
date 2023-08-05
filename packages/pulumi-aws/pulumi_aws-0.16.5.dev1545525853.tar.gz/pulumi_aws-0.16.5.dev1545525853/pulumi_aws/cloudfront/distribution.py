# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime
from .. import utilities, tables

class Distribution(pulumi.CustomResource):
    """
    Creates an Amazon CloudFront web distribution.
    
    For information about CloudFront distributions, see the
    [Amazon CloudFront Developer Guide][1]. For specific information about creating
    CloudFront web distributions, see the [POST Distribution][2] page in the Amazon
    CloudFront API Reference.
    
    > **NOTE:** CloudFront distributions take about 15 minutes to a deployed state
    after creation or modification. During this time, deletes to resources will be
    blocked. If you need to delete a distribution that is enabled and you do not
    want to wait, you need to use the `retain_on_delete` flag.
    """
    def __init__(__self__, __name__, __opts__=None, aliases=None, cache_behaviors=None, comment=None, custom_error_responses=None, default_cache_behavior=None, default_root_object=None, enabled=None, http_version=None, is_ipv6_enabled=None, logging_config=None, ordered_cache_behaviors=None, origins=None, price_class=None, restrictions=None, retain_on_delete=None, tags=None, viewer_certificate=None, web_acl_id=None):
        """Create a Distribution resource with the given unique name, props, and options."""
        if not __name__:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(__name__, str):
            raise TypeError('Expected resource name to be a string')
        if __opts__ and not isinstance(__opts__, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        __props__['aliases'] = aliases

        __props__['cache_behaviors'] = cache_behaviors

        __props__['comment'] = comment

        __props__['custom_error_responses'] = custom_error_responses

        if not default_cache_behavior:
            raise TypeError('Missing required property default_cache_behavior')
        __props__['default_cache_behavior'] = default_cache_behavior

        __props__['default_root_object'] = default_root_object

        if not enabled:
            raise TypeError('Missing required property enabled')
        __props__['enabled'] = enabled

        __props__['http_version'] = http_version

        __props__['is_ipv6_enabled'] = is_ipv6_enabled

        __props__['logging_config'] = logging_config

        __props__['ordered_cache_behaviors'] = ordered_cache_behaviors

        if not origins:
            raise TypeError('Missing required property origins')
        __props__['origins'] = origins

        __props__['price_class'] = price_class

        if not restrictions:
            raise TypeError('Missing required property restrictions')
        __props__['restrictions'] = restrictions

        __props__['retain_on_delete'] = retain_on_delete

        __props__['tags'] = tags

        if not viewer_certificate:
            raise TypeError('Missing required property viewer_certificate')
        __props__['viewer_certificate'] = viewer_certificate

        __props__['web_acl_id'] = web_acl_id

        __props__['active_trusted_signers'] = None
        __props__['arn'] = None
        __props__['caller_reference'] = None
        __props__['domain_name'] = None
        __props__['etag'] = None
        __props__['hosted_zone_id'] = None
        __props__['in_progress_validation_batches'] = None
        __props__['last_modified_time'] = None
        __props__['status'] = None

        super(Distribution, __self__).__init__(
            'aws:cloudfront/distribution:Distribution',
            __name__,
            __props__,
            __opts__)


    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop


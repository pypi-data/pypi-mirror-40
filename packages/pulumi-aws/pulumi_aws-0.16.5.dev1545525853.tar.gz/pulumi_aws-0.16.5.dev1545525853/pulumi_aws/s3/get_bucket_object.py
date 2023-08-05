# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime
from .. import utilities, tables

class GetBucketObjectResult(object):
    """
    A collection of values returned by getBucketObject.
    """
    def __init__(__self__, body=None, cache_control=None, content_disposition=None, content_encoding=None, content_language=None, content_length=None, content_type=None, etag=None, expiration=None, expires=None, last_modified=None, metadata=None, server_side_encryption=None, sse_kms_key_id=None, storage_class=None, tags=None, version_id=None, website_redirect_location=None, id=None):
        if body and not isinstance(body, str):
            raise TypeError('Expected argument body to be a str')
        __self__.body = body
        """
        Object data (see **limitations above** to understand cases in which this field is actually available)
        """
        if cache_control and not isinstance(cache_control, str):
            raise TypeError('Expected argument cache_control to be a str')
        __self__.cache_control = cache_control
        """
        Specifies caching behavior along the request/reply chain.
        """
        if content_disposition and not isinstance(content_disposition, str):
            raise TypeError('Expected argument content_disposition to be a str')
        __self__.content_disposition = content_disposition
        """
        Specifies presentational information for the object.
        """
        if content_encoding and not isinstance(content_encoding, str):
            raise TypeError('Expected argument content_encoding to be a str')
        __self__.content_encoding = content_encoding
        """
        Specifies what content encodings have been applied to the object and thus what decoding mechanisms must be applied to obtain the media-type referenced by the Content-Type header field.
        """
        if content_language and not isinstance(content_language, str):
            raise TypeError('Expected argument content_language to be a str')
        __self__.content_language = content_language
        """
        The language the content is in.
        """
        if content_length and not isinstance(content_length, int):
            raise TypeError('Expected argument content_length to be a int')
        __self__.content_length = content_length
        """
        Size of the body in bytes.
        """
        if content_type and not isinstance(content_type, str):
            raise TypeError('Expected argument content_type to be a str')
        __self__.content_type = content_type
        """
        A standard MIME type describing the format of the object data.
        """
        if etag and not isinstance(etag, str):
            raise TypeError('Expected argument etag to be a str')
        __self__.etag = etag
        """
        [ETag](https://en.wikipedia.org/wiki/HTTP_ETag) generated for the object (an MD5 sum of the object content in case it's not encrypted)
        """
        if expiration and not isinstance(expiration, str):
            raise TypeError('Expected argument expiration to be a str')
        __self__.expiration = expiration
        """
        If the object expiration is configured (see [object lifecycle management](http://docs.aws.amazon.com/AmazonS3/latest/dev/object-lifecycle-mgmt.html)), the field includes this header. It includes the expiry-date and rule-id key value pairs providing object expiration information. The value of the rule-id is URL encoded.
        """
        if expires and not isinstance(expires, str):
            raise TypeError('Expected argument expires to be a str')
        __self__.expires = expires
        """
        The date and time at which the object is no longer cacheable.
        """
        if last_modified and not isinstance(last_modified, str):
            raise TypeError('Expected argument last_modified to be a str')
        __self__.last_modified = last_modified
        """
        Last modified date of the object in RFC1123 format (e.g. `Mon, 02 Jan 2006 15:04:05 MST`)
        """
        if metadata and not isinstance(metadata, dict):
            raise TypeError('Expected argument metadata to be a dict')
        __self__.metadata = metadata
        """
        A map of metadata stored with the object in S3
        """
        if server_side_encryption and not isinstance(server_side_encryption, str):
            raise TypeError('Expected argument server_side_encryption to be a str')
        __self__.server_side_encryption = server_side_encryption
        """
        If the object is stored using server-side encryption (KMS or Amazon S3-managed encryption key), this field includes the chosen encryption and algorithm used.
        """
        if sse_kms_key_id and not isinstance(sse_kms_key_id, str):
            raise TypeError('Expected argument sse_kms_key_id to be a str')
        __self__.sse_kms_key_id = sse_kms_key_id
        """
        If present, specifies the ID of the Key Management Service (KMS) master encryption key that was used for the object.
        """
        if storage_class and not isinstance(storage_class, str):
            raise TypeError('Expected argument storage_class to be a str')
        __self__.storage_class = storage_class
        """
        [Storage class](http://docs.aws.amazon.com/AmazonS3/latest/dev/storage-class-intro.html) information of the object. Available for all objects except for `Standard` storage class objects.
        """
        if tags and not isinstance(tags, dict):
            raise TypeError('Expected argument tags to be a dict')
        __self__.tags = tags
        """
        A mapping of tags assigned to the object.
        """
        if version_id and not isinstance(version_id, str):
            raise TypeError('Expected argument version_id to be a str')
        __self__.version_id = version_id
        """
        The latest version ID of the object returned.
        """
        if website_redirect_location and not isinstance(website_redirect_location, str):
            raise TypeError('Expected argument website_redirect_location to be a str')
        __self__.website_redirect_location = website_redirect_location
        """
        If the bucket is configured as a website, redirects requests for this object to another object in the same bucket or to an external URL. Amazon S3 stores the value of this header in the object metadata.
        """
        if id and not isinstance(id, str):
            raise TypeError('Expected argument id to be a str')
        __self__.id = id
        """
        id is the provider-assigned unique ID for this managed resource.
        """

async def get_bucket_object(bucket=None, key=None, range=None, tags=None, version_id=None):
    """
    The S3 object data source allows access to the metadata and
    _optionally_ (see below) content of an object stored inside S3 bucket.
    
    > **Note:** The content of an object (`body` field) is available only for objects which have a human-readable `Content-Type` (`text/*` and `application/json`). This is to prevent printing unsafe characters and potentially downloading large amount of data which would be thrown away in favour of metadata.
    """
    __args__ = dict()

    __args__['bucket'] = bucket
    __args__['key'] = key
    __args__['range'] = range
    __args__['tags'] = tags
    __args__['versionId'] = version_id
    __ret__ = await pulumi.runtime.invoke('aws:s3/getBucketObject:getBucketObject', __args__)

    return GetBucketObjectResult(
        body=__ret__.get('body'),
        cache_control=__ret__.get('cacheControl'),
        content_disposition=__ret__.get('contentDisposition'),
        content_encoding=__ret__.get('contentEncoding'),
        content_language=__ret__.get('contentLanguage'),
        content_length=__ret__.get('contentLength'),
        content_type=__ret__.get('contentType'),
        etag=__ret__.get('etag'),
        expiration=__ret__.get('expiration'),
        expires=__ret__.get('expires'),
        last_modified=__ret__.get('lastModified'),
        metadata=__ret__.get('metadata'),
        server_side_encryption=__ret__.get('serverSideEncryption'),
        sse_kms_key_id=__ret__.get('sseKmsKeyId'),
        storage_class=__ret__.get('storageClass'),
        tags=__ret__.get('tags'),
        version_id=__ret__.get('versionId'),
        website_redirect_location=__ret__.get('websiteRedirectLocation'),
        id=__ret__.get('id'))

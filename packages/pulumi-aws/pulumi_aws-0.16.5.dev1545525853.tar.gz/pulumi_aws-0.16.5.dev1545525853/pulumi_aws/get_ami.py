# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime
from . import utilities, tables

class GetAmiResult(object):
    """
    A collection of values returned by getAmi.
    """
    def __init__(__self__, architecture=None, block_device_mappings=None, creation_date=None, description=None, hypervisor=None, image_id=None, image_location=None, image_owner_alias=None, image_type=None, kernel_id=None, name=None, owner_id=None, platform=None, product_codes=None, public=None, ramdisk_id=None, root_device_name=None, root_device_type=None, root_snapshot_id=None, sriov_net_support=None, state=None, state_reason=None, tags=None, virtualization_type=None, id=None):
        if architecture and not isinstance(architecture, str):
            raise TypeError('Expected argument architecture to be a str')
        __self__.architecture = architecture
        """
        The OS architecture of the AMI (ie: `i386` or `x86_64`).
        """
        if block_device_mappings and not isinstance(block_device_mappings, list):
            raise TypeError('Expected argument block_device_mappings to be a list')
        __self__.block_device_mappings = block_device_mappings
        """
        The block device mappings of the AMI.
        * `block_device_mappings.#.device_name` - The physical name of the device.
        * `block_device_mappings.#.ebs.delete_on_termination` - `true` if the EBS volume
        will be deleted on termination.
        * `block_device_mappings.#.ebs.encrypted` - `true` if the EBS volume
        is encrypted.
        * `block_device_mappings.#.ebs.iops` - `0` if the EBS volume is
        not a provisioned IOPS image, otherwise the supported IOPS count.
        * `block_device_mappings.#.ebs.snapshot_id` - The ID of the snapshot.
        * `block_device_mappings.#.ebs.volume_size` - The size of the volume, in GiB.
        * `block_device_mappings.#.ebs.volume_type` - The volume type.
        * `block_device_mappings.#.no_device` - Suppresses the specified device
        included in the block device mapping of the AMI.
        * `block_device_mappings.#.virtual_name` - The virtual device name (for
        instance stores).
        """
        if creation_date and not isinstance(creation_date, str):
            raise TypeError('Expected argument creation_date to be a str')
        __self__.creation_date = creation_date
        """
        The date and time the image was created.
        """
        if description and not isinstance(description, str):
            raise TypeError('Expected argument description to be a str')
        __self__.description = description
        """
        The description of the AMI that was provided during image
        creation.
        """
        if hypervisor and not isinstance(hypervisor, str):
            raise TypeError('Expected argument hypervisor to be a str')
        __self__.hypervisor = hypervisor
        """
        The hypervisor type of the image.
        """
        if image_id and not isinstance(image_id, str):
            raise TypeError('Expected argument image_id to be a str')
        __self__.image_id = image_id
        """
        The ID of the AMI. Should be the same as the resource `id`.
        """
        if image_location and not isinstance(image_location, str):
            raise TypeError('Expected argument image_location to be a str')
        __self__.image_location = image_location
        """
        The location of the AMI.
        """
        if image_owner_alias and not isinstance(image_owner_alias, str):
            raise TypeError('Expected argument image_owner_alias to be a str')
        __self__.image_owner_alias = image_owner_alias
        """
        The AWS account alias (for example, `amazon`, `self`) or
        the AWS account ID of the AMI owner.
        """
        if image_type and not isinstance(image_type, str):
            raise TypeError('Expected argument image_type to be a str')
        __self__.image_type = image_type
        """
        The type of image.
        """
        if kernel_id and not isinstance(kernel_id, str):
            raise TypeError('Expected argument kernel_id to be a str')
        __self__.kernel_id = kernel_id
        """
        The kernel associated with the image, if any. Only applicable
        for machine images.
        """
        if name and not isinstance(name, str):
            raise TypeError('Expected argument name to be a str')
        __self__.name = name
        """
        The name of the AMI that was provided during image creation.
        """
        if owner_id and not isinstance(owner_id, str):
            raise TypeError('Expected argument owner_id to be a str')
        __self__.owner_id = owner_id
        """
        The AWS account ID of the image owner.
        """
        if platform and not isinstance(platform, str):
            raise TypeError('Expected argument platform to be a str')
        __self__.platform = platform
        """
        The value is Windows for `Windows` AMIs; otherwise blank.
        """
        if product_codes and not isinstance(product_codes, list):
            raise TypeError('Expected argument product_codes to be a list')
        __self__.product_codes = product_codes
        """
        Any product codes associated with the AMI.
        * `product_codes.#.product_code_id` - The product code.
        * `product_codes.#.product_code_type` - The type of product code.
        """
        if public and not isinstance(public, bool):
            raise TypeError('Expected argument public to be a bool')
        __self__.public = public
        """
        `true` if the image has public launch permissions.
        """
        if ramdisk_id and not isinstance(ramdisk_id, str):
            raise TypeError('Expected argument ramdisk_id to be a str')
        __self__.ramdisk_id = ramdisk_id
        """
        The RAM disk associated with the image, if any. Only applicable
        for machine images.
        """
        if root_device_name and not isinstance(root_device_name, str):
            raise TypeError('Expected argument root_device_name to be a str')
        __self__.root_device_name = root_device_name
        """
        The device name of the root device.
        """
        if root_device_type and not isinstance(root_device_type, str):
            raise TypeError('Expected argument root_device_type to be a str')
        __self__.root_device_type = root_device_type
        """
        The type of root device (ie: `ebs` or `instance-store`).
        """
        if root_snapshot_id and not isinstance(root_snapshot_id, str):
            raise TypeError('Expected argument root_snapshot_id to be a str')
        __self__.root_snapshot_id = root_snapshot_id
        """
        The snapshot id associated with the root device, if any
        (only applies to `ebs` root devices).
        """
        if sriov_net_support and not isinstance(sriov_net_support, str):
            raise TypeError('Expected argument sriov_net_support to be a str')
        __self__.sriov_net_support = sriov_net_support
        """
        Specifies whether enhanced networking is enabled.
        """
        if state and not isinstance(state, str):
            raise TypeError('Expected argument state to be a str')
        __self__.state = state
        """
        The current state of the AMI. If the state is `available`, the image
        is successfully registered and can be used to launch an instance.
        """
        if state_reason and not isinstance(state_reason, dict):
            raise TypeError('Expected argument state_reason to be a dict')
        __self__.state_reason = state_reason
        """
        Describes a state change. Fields are `UNSET` if not available.
        * `state_reason.code` - The reason code for the state change.
        * `state_reason.message` - The message for the state change.
        """
        if tags and not isinstance(tags, dict):
            raise TypeError('Expected argument tags to be a dict')
        __self__.tags = tags
        """
        Any tags assigned to the image.
        * `tags.#.key` - The key name of the tag.
        * `tags.#.value` - The value of the tag.
        """
        if virtualization_type and not isinstance(virtualization_type, str):
            raise TypeError('Expected argument virtualization_type to be a str')
        __self__.virtualization_type = virtualization_type
        """
        The type of virtualization of the AMI (ie: `hvm` or
        `paravirtual`).
        """
        if id and not isinstance(id, str):
            raise TypeError('Expected argument id to be a str')
        __self__.id = id
        """
        id is the provider-assigned unique ID for this managed resource.
        """

async def get_ami(executable_users=None, filters=None, most_recent=None, name_regex=None, owners=None, tags=None):
    """
    Use this data source to get the ID of a registered AMI for use in other
    resources.
    
    > **NOTE:** The `owners` argument will be **required** in the next major version.
    """
    __args__ = dict()

    __args__['executableUsers'] = executable_users
    __args__['filters'] = filters
    __args__['mostRecent'] = most_recent
    __args__['nameRegex'] = name_regex
    __args__['owners'] = owners
    __args__['tags'] = tags
    __ret__ = await pulumi.runtime.invoke('aws:index/getAmi:getAmi', __args__)

    return GetAmiResult(
        architecture=__ret__.get('architecture'),
        block_device_mappings=__ret__.get('blockDeviceMappings'),
        creation_date=__ret__.get('creationDate'),
        description=__ret__.get('description'),
        hypervisor=__ret__.get('hypervisor'),
        image_id=__ret__.get('imageId'),
        image_location=__ret__.get('imageLocation'),
        image_owner_alias=__ret__.get('imageOwnerAlias'),
        image_type=__ret__.get('imageType'),
        kernel_id=__ret__.get('kernelId'),
        name=__ret__.get('name'),
        owner_id=__ret__.get('ownerId'),
        platform=__ret__.get('platform'),
        product_codes=__ret__.get('productCodes'),
        public=__ret__.get('public'),
        ramdisk_id=__ret__.get('ramdiskId'),
        root_device_name=__ret__.get('rootDeviceName'),
        root_device_type=__ret__.get('rootDeviceType'),
        root_snapshot_id=__ret__.get('rootSnapshotId'),
        sriov_net_support=__ret__.get('sriovNetSupport'),
        state=__ret__.get('state'),
        state_reason=__ret__.get('stateReason'),
        tags=__ret__.get('tags'),
        virtualization_type=__ret__.get('virtualizationType'),
        id=__ret__.get('id'))

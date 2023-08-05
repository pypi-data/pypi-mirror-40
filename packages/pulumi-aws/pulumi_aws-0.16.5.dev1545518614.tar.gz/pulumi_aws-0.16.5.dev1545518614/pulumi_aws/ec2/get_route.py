# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime
from .. import utilities, tables

class GetRouteResult(object):
    """
    A collection of values returned by getRoute.
    """
    def __init__(__self__, destination_cidr_block=None, destination_ipv6_cidr_block=None, egress_only_gateway_id=None, gateway_id=None, instance_id=None, nat_gateway_id=None, network_interface_id=None, transit_gateway_id=None, vpc_peering_connection_id=None, id=None):
        if destination_cidr_block and not isinstance(destination_cidr_block, str):
            raise TypeError('Expected argument destination_cidr_block to be a str')
        __self__.destination_cidr_block = destination_cidr_block
        if destination_ipv6_cidr_block and not isinstance(destination_ipv6_cidr_block, str):
            raise TypeError('Expected argument destination_ipv6_cidr_block to be a str')
        __self__.destination_ipv6_cidr_block = destination_ipv6_cidr_block
        if egress_only_gateway_id and not isinstance(egress_only_gateway_id, str):
            raise TypeError('Expected argument egress_only_gateway_id to be a str')
        __self__.egress_only_gateway_id = egress_only_gateway_id
        if gateway_id and not isinstance(gateway_id, str):
            raise TypeError('Expected argument gateway_id to be a str')
        __self__.gateway_id = gateway_id
        if instance_id and not isinstance(instance_id, str):
            raise TypeError('Expected argument instance_id to be a str')
        __self__.instance_id = instance_id
        if nat_gateway_id and not isinstance(nat_gateway_id, str):
            raise TypeError('Expected argument nat_gateway_id to be a str')
        __self__.nat_gateway_id = nat_gateway_id
        if network_interface_id and not isinstance(network_interface_id, str):
            raise TypeError('Expected argument network_interface_id to be a str')
        __self__.network_interface_id = network_interface_id
        if transit_gateway_id and not isinstance(transit_gateway_id, str):
            raise TypeError('Expected argument transit_gateway_id to be a str')
        __self__.transit_gateway_id = transit_gateway_id
        if vpc_peering_connection_id and not isinstance(vpc_peering_connection_id, str):
            raise TypeError('Expected argument vpc_peering_connection_id to be a str')
        __self__.vpc_peering_connection_id = vpc_peering_connection_id
        if id and not isinstance(id, str):
            raise TypeError('Expected argument id to be a str')
        __self__.id = id
        """
        id is the provider-assigned unique ID for this managed resource.
        """

async def get_route(destination_cidr_block=None, destination_ipv6_cidr_block=None, egress_only_gateway_id=None, gateway_id=None, instance_id=None, nat_gateway_id=None, network_interface_id=None, route_table_id=None, transit_gateway_id=None, vpc_peering_connection_id=None):
    """
    `aws_route` provides details about a specific Route.
    
    This resource can prove useful when finding the resource
    associated with a CIDR. For example, finding the peering
    connection associated with a CIDR value.
    """
    __args__ = dict()

    __args__['destinationCidrBlock'] = destination_cidr_block
    __args__['destinationIpv6CidrBlock'] = destination_ipv6_cidr_block
    __args__['egressOnlyGatewayId'] = egress_only_gateway_id
    __args__['gatewayId'] = gateway_id
    __args__['instanceId'] = instance_id
    __args__['natGatewayId'] = nat_gateway_id
    __args__['networkInterfaceId'] = network_interface_id
    __args__['routeTableId'] = route_table_id
    __args__['transitGatewayId'] = transit_gateway_id
    __args__['vpcPeeringConnectionId'] = vpc_peering_connection_id
    __ret__ = await pulumi.runtime.invoke('aws:ec2/getRoute:getRoute', __args__)

    return GetRouteResult(
        destination_cidr_block=__ret__.get('destinationCidrBlock'),
        destination_ipv6_cidr_block=__ret__.get('destinationIpv6CidrBlock'),
        egress_only_gateway_id=__ret__.get('egressOnlyGatewayId'),
        gateway_id=__ret__.get('gatewayId'),
        instance_id=__ret__.get('instanceId'),
        nat_gateway_id=__ret__.get('natGatewayId'),
        network_interface_id=__ret__.get('networkInterfaceId'),
        transit_gateway_id=__ret__.get('transitGatewayId'),
        vpc_peering_connection_id=__ret__.get('vpcPeeringConnectionId'),
        id=__ret__.get('id'))

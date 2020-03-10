#!/usr/bin/python
#
# Copyright: Pureport
# GNU General Public License v3.0+ (see licenses/gpl-3.0-standalone.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
#
from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'Pureport'
}

DOCUMENTATION = '''
---
module: google_cloud_interconnect_connection
short_description: Create, update or delete a Google Cloud Interconnect connection
description:
    - "Create, update or delete a Google Cloud Interconnect connection"
version_added: "2.8"
requirements: [ pureport-client ]
author: Matt Traynham (@mtraynham)
options:
    primary_pairing_key:
        description:
            - The Google Cloud Interconnect Attachment's primary pairing key.
        required: true
        type: str
    secondary_pairing_key:
        description:
            - The Google Cloud Interconnect Attachment's secondary pairing key (HA).
        required: false
        type: str
extends_documentation_fragment:
    - pureport.fabric.client
    - pureport.fabric.network
    - pureport.fabric.state
    - pureport.fabric.resolve_existing
    - pureport.fabric.wait_for_server
    - pureport.fabric.connection_args
'''

EXAMPLES = '''
- name: Create a simple Google Cloud Interconnect connection for a network
  google_cloud_interconnect_connection:
    api_key: XXXXXXXXXXXXX
    api_secret: XXXXXXXXXXXXXXXXX
    network_href: /networks/network-XXXXXXXXXXXXXXXXXXXXXX
    name: My Ansible Google Cloud Interconnect Connection
    speed: 50
    high_availability: true
    location_href: /locations/XX-XXX
    billing_term: HOURLY
    primary_pairing_key: XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX/XX-XXXXXXXX#/1
    secondary_pairing_key: XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX/XX-XXXXXXXX#/2
    wait_for_server: true  # Wait for the server to finish provisioning the connection
  register: result  # Registers the connection as the result

- name: Update the newly created connection with changed properties
  google_cloud_interconnect_connection:
    api_key: XXXXXXXXXXXXX
    api_secret: XXXXXXXXXXXXXXXXX
    network_href: /networks/network-XXXXXXXXXXXXXXXXXXXXXX
    name: "{{ result.name }}"
    speed: 100
    high_availability: "{{ result.high_availability }}"
    location_href: "{{ result.location.href }}"
    billing_term: "{{ result.billing_term }}"
    primary_pairing_key: "{{ result.primary_pairing_key }}"
    secondary_pairing_key: "{{ result.secondary_pairing_key }}"
    wait_for_server: true  # Wait for the server to finish updating the connection
  register: result  # Registers the connection as the result

- name: Delete the newly created connection using the 'absent' state
  google_cloud_interconnect_connection:
    api_key: XXXXXXXXXXXXX
    api_secret: XXXXXXXXXXXXXXXXX
    network_href: /networks/network-XXXXXXXXXXXXXXXXXXXXXX
    state: absent
    name: "{{ result.name }}"
    speed: "{{ result.speed }}"
    high_availability: "{{ result.high_availability }}"
    location_href: "{{ result.location.href }}"
    billing_term: "{{ result.billing_term }}"
    primary_pairing_key: "{{ result.primary_pairing_key }}"
    secondary_pairing_key: "{{ result.secondary_pairing_key }}"
    wait_for_server: true  # Wait for the server to finish deleting the connection

- name: Create a Google Cloud Interconnect connection with all properties configured
  google_cloud_interconnect_connection:
    api_key: XXXXXXXXXXXXX
    api_secret: XXXXXXXXXXXXXXXXX
    network_href: /networks/network-XXXXXXXXXXXXXXXXXXXXXX
    name: My Ansible Google Cloud Interconnect
    speed: 50
    high_availability: true
    location_href: /locations/XX-XXX
    billing_term: HOURLY
    primary_pairing_key: XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX/XX-XXXXXXXX#/1
    secondary_pairing_key: XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX/XX-XXXXXXXX#/2
    # Optional properties start here
    description: My Ansible managed Google Cloud Interconnect connection
    customer_networks:
      - address: a.b.c.d/x  # A valid CIDR address
        name: My AWS accessible CIDR address
    nat_enabled: true
    nat_mappings:
      - a.b.c.d/x  # A valid CIDR address, likely referencing a Customer Network
'''

RETURN = '''
network:
    description: The network the connection belongs to.
    returns: success
    type: complex
    contains:
        id:
            description: The network's id.
            returns: success
            type: str
            sample: "network-XXXXXXXXXXXXXXXXXXXXXX"
        href:
            description: The network's href.
            returns: success
            type: str
            sample: "/networks/network-XXXXXXXXXXXXXXXXXXXXXX"
        title:
            description: The network's name.
            returns: success
            type: str
            sample: "My Network"
id:
    description: The connection's id.
    returns: success
    type: str
    sample: "conn-XXXXXXXXXXXXXXXXXXXXXX"
href:
    description: The connection's href.
    returns: success
    type: str
    sample: "/connections/conn-XXXXXXXXXXXXXXXXXXXXXX"
state:
    description: The connection's state.
    returns: success
    type: str
    sample: "ACTIVE"
type:
    description: The connection's type.
    returns: success
    type: str
    sample: "GOOGLE_CLOUD_INTERCONNECT"
name:
    description: The connection's name.
    returns: success
    type: str
    sample: "My Connection"
description:
    description: The connection's description.
    returns: success
    type: str
    sample: "My example connection"
location:
    description: The location the connection is attached to.
    returns: success
    type: complex
    contains:
        id:
            description: The location's id.
            returns: success
            type: str
            sample: "us-sea"
        href:
            description: The location's href.
            returns: success
            type: str
            sample: "/locations/us-sea"
        title:
            description: The location's name.
            returns: success
            type: str
            sample: "Seattle, WA"
speed:
    description: The connection's speed (in Mbps).
    returns: success
    type: int
    sample: 50
high_availability:
    description: A boolean representing if the connection is high available (2 gateways).
    returns: success
    type: bool
    sample: false
billing_term:
    description: The connection's billing term.
    returns: success
    type: str
    sample: "HOURLY"
customer_asn:
    description: The customer provided ASN for the connection.
    returns: success
    type: int
    sample: 16550
customer_networks:
    description: A list of subnet's that exist behind this connection on the customer side.
    returns: success
    type: list
    contains:
        address:
            description: The customer network's CIDR address subnet.
            returns: success
            type: str
            sample: "10.0.0.0/24"
        name:
            description: The customer network's name.
            returns: success
            type: str
            sample: "My Connection's Subnet"
nat:
    description: A NAT configuration for this connection.
    returns: success
    type: complex
    contains:
        enabled:
            description: A boolean representing if NAT is enabled for this connection.
            returns: success
            type: bool
            sample: true
        pnat_cidr:
            description:
                - The default range of addresses that will be assigned as the source IP on traffic passing through
                  this connection.
            returns: success
            type: str
            sample: "100.64.255.240/28"
        blocks:
            description:
                - These are the blocks of Carrier-Grade NAT IPs that have been assigned to this gateway.  With
                - NAT enabled, all traffic that passes through this gateway will have a source address that falls
                - within these blocks of IP.  New blocks are automatically allocated as-needed when new mappings
                - are created.
            returns: success
            type: list[str]
            sample: ["100.64.0.0/16"]
        mappings:
            description:
                - These mappings override the default port-address translation functionality, allowing certain
                - devices and/or subnets on your network to be reached from other connections using the assigned
                - NAT addresses instead of the native IPs (which presumably overlap with other IPs on other
                - connections).  If a range is defined, the suffix portion of the address is mapped one-to-one
                - between the native CIDR and the NAT CIDR.  For example, if a mapping is defined from
                - 192.168.1.0/24 to 100.64.5.0/24, then a device with a native IP of 192.168.1.42 would
                - be reachable using 100.64.5.42.
            returns: success
            type: list
            contains:
                block:
                    description: The block allocated for this NAT mapping.
                    returns: success
                    type: str
                    sample: "100.64.0.0/16"
                native_cidr:
                    description: The native CIDR address for this NAT mapping.
                    returns: success
                    type: str
                    sample: "10.0.0.0/24"
                nat_cidr:
                    description: The allocated NAT CIDR address for this NAT mapping.
                    returns: success
                    type: str
                    sample: "100.64.0.0/24"
primary_gateway:
    description: Information about this connection's primary gateway.
    returns: success
    type: complex
    contains:
        id:
            description: The gateway's id.
            returns: success
            type: str
            sample: "gateway-XXXXXXXXXXXXXXXXXXXXXX"
        state:
            description: The gateway's state.
            returns: success
            type: str
            sample: "ACTIVE"
        link_state:
            description: The gateway's link state.
            returns: success
            type: str
            sample: "UP"
        type:
            description: The gateway's type.
            returns: success
            type: str
            sample: "STANDARD"
        name:
            description: The gateway's name.
            returns: success
            type: str
            sample: "GOOGLE_CLOUD_INTERCONNECT"
        remote_id:
            description: The gateway's remote id, e.g. the Google interconnect attachment ID.
            returns: success
            type: str
            sample: "abcd1234"
        availability_domain:
            description: The gateway's availability domain ("PRIMARY" or "SECONDARY").
            returns: success
            type: str
            sample: "PRIMARY"
        bgp_config:
            description: Information about this gateway's bgp configuration.
            returns: success
            type: complex
            contains:
                state:
                    description: The gateway's bgp state.
                    returns: success
                    type: str
                    sample: "UP"
                peering_subnet:
                    description: The gateway's peering subnet.
                    returns: success
                    type: str
                    sample: "169.254.100.0/30"
                pureport_ip:
                    description: The gateway's Pureport IP with prefix.
                    returns: success
                    type: str
                    sample: "169.254.100.1/30"
                pureport_asn:
                    description: The gateway's Pureport ASN.
                    returns: success
                    type: int
                    sample: 394351
                customer_ip:
                    description: The gateway's Customer IP with prefix.
                    returns: success
                    type: str
                    sample: "169.254.100.2/30"
                customer_asn:
                    description: The gateway's Customer ASN.
                    returns: success
                    type: int
                    sample: 16550
                public_nat_ip:
                    description: The gateway's public NAT IP.
                    returns: success
                    type: str
                password:
                    description: The gateway's BGP shared key.
                    returns: success
                    type: str
        error_code:
            description: If the gateway transitioned state in error, this is the code representing that error.
            returns: if the connection is in a failed state
            type: str
            sample: "BAD_REQUEST"
        error_message:
            description: If the connection transitioned state in error, this is the message representing that error.
            returns: if the connection is in a failed state
            type: str
secondary_gateway:
    description: Information about this connection's secondary gateway.
    returns: if the connection is high available
    type: complex
    contains:
        id:
            description: The gateway's id.
            returns: success
            type: str
            sample: "gateway-XXXXXXXXXXXXXXXXXXXXXX"
        state:
            description: The gateway's state.
            returns: success
            type: str
            sample: "ACTIVE"
        link_state:
            description: The gateway's link state.
            returns: success
            type: str
            sample: "UP"
        type:
            description: The gateway's type.
            returns: success
            type: str
            sample: "STANDARD"
        name:
            description: The gateway's name.
            returns: success
            type: str
            sample: "GOOGLE_CLOUD_INTERCONNECT"
        remote_id:
            description: The gateway's remote id, e.g. the Google interconnect attachment ID.
            returns: success
            type: str
            sample: "abcd1234"
        availability_domain:
            description: The gateway's availability domain ("PRIMARY" or "SECONDARY").
            returns: success
            type: str
            sample: "PRIMARY"
        bgp_config:
            description: Information about this gateway's bgp configuration.
            returns: success
            type: complex
            contains:
                state:
                    description: The gateway's bgp state.
                    returns: success
                    type: str
                    sample: "UP"
                peering_subnet:
                    description: The gateway's peering subnet.
                    returns: success
                    type: str
                    sample: "169.254.100.0/30"
                pureport_ip:
                    description: The gateway's Pureport IP with prefix.
                    returns: success
                    type: str
                    sample: "169.254.100.1/30"
                pureport_asn:
                    description: The gateway's Pureport ASN.
                    returns: success
                    type: int
                    sample: 394351
                customer_ip:
                    description: The gateway's Customer IP with prefix.
                    returns: success
                    type: str
                    sample: "169.254.100.2/30"
                pureport_asn:
                    description: The gateway's Customer ASN.
                    returns: success
                    type: int
                    sample: 65000
                public_nat_ip:
                    description: The gateway's public NAT IP.
                    returns: success
                    type: str
                password:
                    description: The gateway's BGP shared key.
                    returns: success
                    type: str
        error_code:
            description: If the gateway transitioned state in error, this is the code representing that error.
            returns: if the connection is in a failed state
            type: str
            sample: "BAD_REQUEST"
        error_message:
            description: If the connection transitioned state in error, this is the message representing that error.
            returns: if the connection is in a failed state
            type: str
billing_plan:
    description: The inferred billing plan information for this connection.
    returns: success
    type: complex
    contains:
        id:
            description: The billing plan id.
            returns: success
            type: str
            sample: "plan_XXXXXXXXXXXX"
        amount:
            description: The billing plan amount (cents).
            returns: success
            type: int
            sample: 15
        term:
            description: The billing interval which the amount is charged for usage.
            returns: success
            type: str
            sample: "HOURLY"
        billing_interval:
            description: The billing interval which a invoice is sent to the connection owner.
            returns: success
            type: str
            sample: "MONTH"
error_code:
    description: If the connection transitioned state in error, this is the code representing that error.
    returns: if the connection is in a failed state
    type: str
    sample: BAD_REQUEST
error_message:
    description: If the connection transitioned state in error, this is the message representing that error.
    returns: if the connection is in a failed state
    type: str
created_at:
    description: A date-time representing connection creation.
    returns: success
    type: str
    sample: "2019-05-14T14:41:42.932253Z"
active_at:
    description: A date-time representing connection billing term start.
    returns: success
    type: str
    sample: "2019-05-14T14:41:42.932253Z"
deleted_at:
    description: A date-time representing connection deletion.
    returns: success
    type: str
    sample: "2019-05-14T14:41:42.932253Z"
primary_pairing_key:
    description: The primary pairing key for the GCI connection.
    returns: success
    type: str
    sample: "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX/XX-XXXXXXXX#/1"
secondary_pairing_key:
    description: The secondary pairing key for the GCI connection.
    returns: if the connection is high available
    type: str
    sample: "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX/XX-XXXXXXXX#/2"
'''

from functools import partial
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.dict_transformations import \
    camel_dict_to_snake_dict, \
    snake_dict_to_camel_dict

from ..module_utils.pureport_client import \
    get_object_link, \
    get_client_argument_spec, \
    get_client_mutually_exclusive, \
    get_network_argument_spec, \
    get_network_mutually_exclusive
from ..module_utils.pureport_crud import \
    get_state_argument_spec, \
    get_resolve_existing_argument_spec
from ..module_utils.pureport_connection_crud import \
    get_wait_for_server_argument_spec, \
    get_connection_argument_spec, \
    get_connection_required_one_of, \
    get_cloud_connection_argument_spec, \
    connection_crud


def construct_connection(module):
    """
    Construct a Connection from the Ansible module arguments
    :param AnsibleModule module: the Ansible module
    :rtype: pureport.api.client.Connection
    """
    connection = dict((k, module.params.get(k)) for k in (
        'id',
        'name',
        'description',
        'speed',
        'high_availability',
        'billing_term',
        'customer_networks',
        'primary_pairing_key',
        'secondary_pairing_key'
    ))
    connection.update(dict(
        type='GOOGLE_CLOUD_INTERCONNECT',
        location=get_object_link(module, '/locations', 'location_id', 'location_href'),
        nat=dict(
            enabled=module.params.get('nat_enabled'),
            mappings=[dict(native_cidr=nat_mapping)
                      for nat_mapping in module.params.get('nat_mappings')]
        )
    ))
    connection = snake_dict_to_camel_dict(connection)
    connection.update(dict(
        tags=module.params.get('tags')
    ))
    return connection


def main():
    argument_spec = dict()
    argument_spec.update(get_client_argument_spec())
    argument_spec.update(get_network_argument_spec())
    argument_spec.update(get_state_argument_spec())
    argument_spec.update(get_resolve_existing_argument_spec())
    argument_spec.update(get_wait_for_server_argument_spec())
    argument_spec.update(get_connection_argument_spec())
    argument_spec.update(get_cloud_connection_argument_spec())
    argument_spec.update(
        dict(
            primary_pairing_key=dict(type='str', required=True),
            secondary_pairing_key=dict(type='str')
        )
    )
    mutually_exclusive = []
    mutually_exclusive += get_client_mutually_exclusive()
    required_one_of = []
    required_one_of += get_network_mutually_exclusive()
    required_one_of += get_connection_required_one_of()
    module = AnsibleModule(
        argument_spec=argument_spec,
        mutually_exclusive=mutually_exclusive,
        required_one_of=required_one_of
    )
    # Using partials to fill in the method params
    (
        changed,
        changed_connection,
        argument_connection,
        existing_connection
    ) = connection_crud(
        module,
        partial(construct_connection, module)
    )
    module.exit_json(
        changed=changed,
        **camel_dict_to_snake_dict(changed_connection)
    )


if __name__ == '__main__':
    main()

# encoding: utf-8

from cloudify import ctx
from cloudify.exceptions import NonRecoverableError
from cloudify.state import ctx_parameters as inputs


def get_interface_from_ip_addr_output(ip_addr_output, ip_address):
    ctx.logger.info(ip_address)

    lines = ip_addr_output.split('\n')

    for line in lines:
        if ip_address in line:
            return line.split(' ')[-1]

    raise NonRecoverableError(
        'Cannot obtain physical interface for IP address "{0}" name from '
        '"ip addr" command execution result: "{1}"'
        .format(ip_address, ip_addr_output)
    )


def rewrite_runtime_properites(instance):
    result_properties = instance.runtime_properties.get(
        'result_properties',
        {}
    )

    id = result_properties['id']
    mac_address = result_properties['mac_address']
    ip_address_with_mask = result_properties['ip_address_with_mask']
    ip_address, netmask = ip_address_with_mask.split('/')

    instance.runtime_properties['mac_address'] = mac_address
    instance.runtime_properties['ip_address'] = ip_address
    instance.runtime_properties['netmask'] = netmask
    instance.runtime_properties['id'] = id


if __name__ == '__main__':
    ctx.instance.runtime_properties['physical_interface'] = \
        get_interface_from_ip_addr_output(
            ctx.instance.runtime_properties
                .get('result_properties', {})
                .get('text', ''),
            inputs['ip']
        )

    rewrite_runtime_properites(ctx.instance)

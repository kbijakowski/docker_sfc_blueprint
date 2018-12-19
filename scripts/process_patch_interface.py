# encoding: utf-8

from cloudify import ctx
from cloudify.exceptions import NonRecoverableError
from cloudify.state import ctx_parameters as inputs


def get_ofport_id(cmd_execution_result, if_name_to_find):
    descriptions = cmd_execution_result.split('\n\n')

    for description in descriptions:
        lines = description.split('\n')
        if_name = lines[0].split(' : ')[1].strip('"')
        of_port = lines[1].split(' : ')[1]

        if if_name == if_name_to_find:
            return of_port

    raise NonRecoverableError(
        'Cannot obtain openflow interface for '
        'physical interface "{0}" name from '
        'command execution result: "{1}"'
        .format(if_name_to_find, cmd_execution_result)
    )


if __name__ == '__main__':
    ofport = get_ofport_id(
        ctx.instance.runtime_properties
            .get('result_properties', {})
            .get('text', ''),
        inputs['physical_interface_name']
    )

    peer_ofport = get_ofport_id(
        ctx.instance.runtime_properties
            .get('result_properties', {})
            .get('text', ''),
        inputs['physical_peer_interface_name']
    )

    ctx.instance.runtime_properties['id'] = ofport
    ctx.instance.runtime_properties['peer_id'] = peer_ofport

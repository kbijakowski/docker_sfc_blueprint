# encoding: utf-8

from cloudify import ctx


strip_unicode = lambda s: "".join(i for i in s if 31 < ord(i) < 127)


def rewrite_runtime_properites(instance):
    result_properties = instance.runtime_properties.get(
        'result_properties',
        {}
    )

    id = result_properties['text']
    instance.runtime_properties['id'] = strip_unicode(id)


if __name__ == '__main__':
    rewrite_runtime_properites(ctx.instance)

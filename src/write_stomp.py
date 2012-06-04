
import random
import collectd
import stomp
import json

# TODO: manage connection, see 'init' method.

config = {
    'destination':'/queue/messages',
    'host':'localhost',
    'port': 61613
}

def stomp_event_type(vl):
    if vl.plugin and vl.type_instance:
        return "%s_%s" % (vl.plugin, vl.type_instance)
    elif vl.plugin and vl.type and vl.type != vl.plugin:
        return "%s_%s" % (vl.plugin, vl.type)
    else:
        return vl.plugin


def stomp_write(vl, data=None):
    global config

    # print vl
    
    try:
        conn = stomp.Connection(host_and_ports=[(config['host'],
            config['port'])])
        conn.start()
        conn.connect()

        value = vl.type
        if vl.type_instance:
            value = "%s_%s" % (vl.type, vl.type_instance)

        msg = {
            'eventtype': 'collectd',
            'host': vl.host,
            'plugin': vl.plugin,
            'pluginInstance': vl.plugin_instance,
            'type': vl.type,
            'typeInstance': vl.type_instance,
            'timestamp': vl.time,
            'values': vl.values
        }

        #msg = {
            #'host': vl.host,
            #'value': vl.values,
            #'timestamp': vl.time
        #}
        #if vl.plugin_instance:
            #msg['instance'] = vl.plugin_instance

        # print msg
        conn.send(json.dumps(msg), destination=config['destination'],
                headers={'eventtype': 'collectd'}) # stomp_event_type(vl)})
        conn.disconnect()

    except stomp.exception.ConnectFailedException as error:
        print "Connection error."
        print error

def stomp_config(c):
    global config

    for child in c.children:
        if child.key == 'host':
            config['host'] = child.values[0]
        elif child.key == 'port':
            config['port'] = int(child.values[0])
        elif child.key == 'destination':
            config['destination'] = child.values[0]

    # register writer
    collectd.register_write(stomp_write)

collectd.register_config(stomp_config)

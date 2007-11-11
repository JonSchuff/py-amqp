#!/usr/bin/env python
"""
Test AMQP library.

"""
import sys
from amqp import Connection, Content

def main():
    if len(sys.argv) > 1:
        msg = sys.argv[1]
    else:
        msg = 'Hello from Python'

    conn = Connection('10.66.0.8')
    ch = conn.channel(1)
    ticket = ch.access_request('/data', active=True, write=True, read=True)

    ch.exchange_declare(ticket, 'myfan', 'fanout', auto_delete=True)
    qname, _, _ = ch.queue_declare(ticket)
    ch.queue_bind(ticket, qname, 'myfan')

    msg = Content(msg, content_type='text/plain', headers={'foo': 7, 'bar': 'baz'})
    ch.basic_publish(msg, ticket, 'myfan')

    msg2 = ch.basic_get(ticket, qname, no_ack=True)[5]
    if 'content_encoding' in msg2.properties:
        msg2.body = msg2.body.decode(msg2.properties['content_encoding'])
    print 'received', msg2.body, type(msg2.body), msg2.properties

    ch.close()
    conn.close()

if __name__ == '__main__':
    main()
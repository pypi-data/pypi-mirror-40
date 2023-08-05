# encoding=utf-8

import kombu
import uuid
import json

class RabbitMQWrapper(object):

    def __init__(self, conn_or_uri='amqp://tubsiss:ab123456@bejxax0501.cn.oracle.com:5672//'):
        if isinstance(conn_or_uri, kombu.Connection):
            self.conn = conn_or_uri
        elif self.validate_amqp_uri(conn_or_uri):
            self.conn = kombu.Connection(conn_or_uri) 
        else:
            raise TypeError("Unknown amqp_connection type %s" % type(conn_or_uri))
        
        # self.cur = self.conn.cursor()   # 创建一个Cursor:


    def validate_amqp_uri(self, uri):
        # amqp://guest:[email protected]:5672//
        return True


    def send(self, to_queue, msg, wait_reply=True):
        print('to_queue:%s, msg:%s' %(to_queue, msg))
        assert isinstance(msg, dict), 'msg should be a python_dict'
        #unique = uuid.uuid4().hex
        #msg.update({'id':unique})
        # recv_queue = self.conn.SimpleQueue(unique)

        send_queue = self.conn.SimpleQueue(to_queue)
        for i in range(1000):
            send_queue.put({'count':i}, serializer="json", compression="zlib")
        #resp = recv_queue.get(block=True)   # , timeout=1)
        #print("Received: %s" % resp.payload)
        #resp.ack()


    def recv(self, from_queue):    
        # 对于consumer，首先连接到rabbit server，然后获得producer的queue，从queue中获取信息在处理
        recv_queue = self.conn.SimpleQueue(from_queue)
        msg = recv_queue.get(block=True)    # , timeout=1)
        print("Received: %s" % msg.payload)
        msg.ack()
        # simple_queue.close()


    def __del__(self):
        # self.cur.close()
        self.conn.close()


if __name__=='__main__':
    from threading import Thread
    producer = RabbitMQWrapper()
    # Thread(target=producer.send, args=('test_q', {'a':1, 'b':2})).start()
    producer.send(to_queue='test_q', msg={'a':1, 'b':2})

    #consumer = RabbitMQWrapper()
    #Thread(target=consumer.recv, args=('test_q',)).start()

    #import time
    #time.sleep(5)
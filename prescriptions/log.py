import logging
import logstash

l = logging.getLogger()
h = logstash.UDPLogstashHandler(host='logstash', port=5044,
                                tags={'type': 'log'})

l.addHandler(h)
l.setLevel(logging.INFO)

l.info('Hello World!')


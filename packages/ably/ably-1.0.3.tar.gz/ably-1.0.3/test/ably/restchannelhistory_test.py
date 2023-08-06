from __future__ import absolute_import

import logging
import time

import responses
import six
import msgpack
from six.moves import range

from ably import AblyException
from ably import AblyRest
from ably.http.paginatedresult import PaginatedResult

from test.ably.restsetup import RestSetup
from test.ably.utils import VaryByProtocolTestsMetaclass, dont_vary_protocol, BaseTestCase

test_vars = RestSetup.get_test_vars()
log = logging.getLogger(__name__)


@six.add_metaclass(VaryByProtocolTestsMetaclass)
class TestRestChannelHistory(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        cls.ably = AblyRest(key=test_vars["keys"][0]["key_str"],
                            rest_host=test_vars["host"],
                            port=test_vars["port"],
                            tls_port=test_vars["tls_port"],
                            tls=test_vars["tls"])
        cls.time_offset = cls.ably.time() - int(time.time())

    def per_protocol_setup(self, use_binary_protocol):
        self.ably.options.use_binary_protocol = use_binary_protocol
        self.use_binary_protocol = use_binary_protocol

    def test_channel_history_types(self):
        history0 = self.ably.channels[
            self.protocol_channel_name('persisted:channelhistory_types')]

        history0.publish('history0', six.u('This is a string message payload'))
        history0.publish('history1', b'This is a byte[] message payload')
        history0.publish('history2', {'test': 'This is a JSONObject message payload'})
        history0.publish('history3', ['This is a JSONArray message payload'])

        history = history0.history()
        self.assertIsInstance(history, PaginatedResult)
        messages = history.items
        self.assertIsNotNone(messages, msg="Expected non-None messages")
        self.assertEqual(4, len(messages), msg="Expected 4 messages")

        message_contents = {m.name: m for m in messages}
        self.assertEqual(six.u("This is a string message payload"),
                         message_contents["history0"].data,
                         msg="Expect history0 to be expected String)")
        self.assertEqual(b"This is a byte[] message payload",
                         message_contents["history1"].data,
                         msg="Expect history1 to be expected byte[]")
        self.assertEqual({"test": "This is a JSONObject message payload"},
                         message_contents["history2"].data,
                         msg="Expect history2 to be expected JSONObject")
        self.assertEqual(["This is a JSONArray message payload"],
                         message_contents["history3"].data,
                         msg="Expect history3 to be expected JSONObject")

        expected_message_history = [
            message_contents['history3'],
            message_contents['history2'],
            message_contents['history1'],
            message_contents['history0'],
        ]

        self.assertEqual(expected_message_history, messages,
                msg="Expect messages in reverse order")

    def test_channel_history_multi_50_forwards(self):
        history0 = self.ably.channels[
            self.protocol_channel_name('persisted:channelhistory_multi_50_f')]

        for i in range(50):
            history0.publish('history%d' % i, str(i))

        history = history0.history(direction='forwards')
        self.assertIsNotNone(history)
        messages = history.items
        self.assertEqual(50, len(messages),
                msg="Expected 50 messages")

        message_contents = {m.name:m for m in messages}
        expected_messages = [message_contents['history%d' % i] for i in range(50)]
        self.assertEqual(expected_messages, messages,
                msg='Expect messages in forward order')

    def test_channel_history_multi_50_backwards(self):
        history0 = self.ably.channels[
            self.protocol_channel_name('persisted:channelhistory_multi_50_b')]

        for i in range(50):
            history0.publish('history%d' % i, str(i))

        history = history0.history(direction='backwards')
        self.assertIsNotNone(history)
        messages = history.items
        self.assertEqual(50, len(messages),
                msg="Expected 50 messages")

        message_contents = {m.name:m for m in messages}
        expected_messages = [message_contents['history%d' % i] for i in range(49, -1, -1)]

        self.assertEqual(expected_messages, messages,
                msg='Expect messages in reverse order')

    def history_mock_url(self, channel_name):
        kwargs = {
            'scheme': 'https' if test_vars['tls'] else 'http',
            'host': test_vars['host'],
            'channel_name': channel_name
        }
        port = test_vars['tls_port'] if test_vars.get('tls') else kwargs['port']
        if port == 80:
            kwargs['port_sufix'] = ''
        else:
            kwargs['port_sufix'] = ':' + str(port)
        url = '{scheme}://{host}{port_sufix}/channels/{channel_name}/history'
        return url.format(**kwargs)

    @responses.activate
    @dont_vary_protocol
    def test_channel_history_default_limit(self):
        self.per_protocol_setup(True)
        channel = self.ably.channels['persisted:channelhistory_limit']
        url = self.history_mock_url('persisted:channelhistory_limit')
        self.responses_add_empty_msg_pack(url)
        channel.history()
        self.assertNotIn('limit=', responses.calls[0].request.url.split('?')[-1])

    @responses.activate
    @dont_vary_protocol
    def test_channel_history_with_limits(self):
        self.per_protocol_setup(True)
        channel = self.ably.channels['persisted:channelhistory_limit']
        url = self.history_mock_url('persisted:channelhistory_limit')
        self.responses_add_empty_msg_pack(url)
        channel.history(limit=500)
        self.assertIn('limit=500', responses.calls[0].request.url.split('?')[-1])
        channel.history(limit=1000)
        self.assertIn('limit=1000', responses.calls[1].request.url.split('?')[-1])

    @dont_vary_protocol
    def test_channel_history_max_limit_is_1000(self):
        channel = self.ably.channels['persisted:channelhistory_limit']
        with self.assertRaises(AblyException):
            channel.history(limit=1001)

    def test_channel_history_limit_forwards(self):
        history0 = self.ably.channels[
            self.protocol_channel_name('persisted:channelhistory_limit_f')]

        for i in range(50):
            history0.publish('history%d' % i, str(i))

        history = history0.history(direction='forwards', limit=25)
        self.assertIsNotNone(history)
        messages = history.items
        self.assertEqual(25, len(messages),
                msg="Expected 25 messages")

        message_contents = {m.name:m for m in messages}
        expected_messages = [message_contents['history%d' % i] for i in range(25)]

        self.assertEqual(expected_messages, messages,
                msg='Expect messages in forward order')

    def test_channel_history_limit_backwards(self):
        history0 = self.ably.channels[
            self.protocol_channel_name('persisted:channelhistory_limit_b')]

        for i in range(50):
            history0.publish('history%d' % i, str(i))

        history = history0.history(direction='backwards', limit=25)
        self.assertIsNotNone(history)
        messages = history.items
        self.assertEqual(25, len(messages),
                msg="Expected 25 messages")

        message_contents = {m.name:m for m in messages}
        expected_messages = [message_contents['history%d' % i] for i in range(49, 24, -1)]

        self.assertEqual(expected_messages, messages,
                msg='Expect messages in forward order')

    def test_channel_history_time_forwards(self):
        history0 = self.ably.channels[
            self.protocol_channel_name('persisted:channelhistory_time_f')]

        for i in range(20):
            history0.publish('history%d' % i, str(i))

        interval_start = self.ably.time()

        for i in range(20, 40):
            history0.publish('history%d' % i, str(i))

        interval_end = self.ably.time()

        for i in range(40, 60):
            history0.publish('history%d' % i, str(i))

        history = history0.history(direction='forwards', start=interval_start,
                                   end=interval_end)

        messages = history.items
        self.assertEqual(20, len(messages))

        message_contents = {m.name:m for m in messages}
        expected_messages = [message_contents['history%d' % i] for i in range(20, 40)]

        self.assertEqual(expected_messages, messages,
                msg='Expect messages in forward order')

    def test_channel_history_time_backwards(self):
        history0 = self.ably.channels[
            self.protocol_channel_name('persisted:channelhistory_time_b')]

        for i in range(20):
            history0.publish('history%d' % i, str(i))

        interval_start = self.ably.time()

        for i in range(20, 40):
            history0.publish('history%d' % i, str(i))

        interval_end = self.ably.time()

        for i in range(40, 60):
            history0.publish('history%d' % i, str(i))

        history = history0.history(direction='backwards', start=interval_start,
                                   end=interval_end)

        messages = history.items
        self.assertEqual(20, len(messages))

        message_contents = {m.name:m for m in messages}
        expected_messages = [message_contents['history%d' % i] for i in range(39, 19, -1)]

        self.assertEqual(expected_messages, messages,
                msg='Expect messages in reverse order')

    def test_channel_history_paginate_forwards(self):
        history0 = self.ably.channels[
            self.protocol_channel_name('persisted:channelhistory_paginate_f')]

        for i in range(50):
            history0.publish('history%d' % i, str(i))

        history = history0.history(direction='forwards', limit=10)
        messages = history.items

        self.assertEqual(10, len(messages))

        message_contents = {m.name:m for m in messages}
        expected_messages = [message_contents['history%d' % i] for i in range(0, 10)]

        self.assertEqual(expected_messages, messages,
                msg='Expected 10 messages')
        
        history = history.next()
        messages = history.items

        self.assertEqual(10, len(messages))

        message_contents = {m.name:m for m in messages}
        expected_messages = [message_contents['history%d' % i] for i in range(10, 20)]

        self.assertEqual(expected_messages, messages,
                msg='Expected 10 messages')
        
        history = history.next()
        messages = history.items

        self.assertEqual(10, len(messages))

        message_contents = {m.name:m for m in messages}
        expected_messages = [message_contents['history%d' % i] for i in range(20, 30)]

        self.assertEqual(expected_messages, messages,
                msg='Expected 10 messages')
        
    def test_channel_history_paginate_backwards(self):
        history0 = self.ably.channels[
            self.protocol_channel_name('persisted:channelhistory_paginate_b')]

        for i in range(50):
            history0.publish('history%d' % i, str(i))

        history = history0.history(direction='backwards', limit=10)
        messages = history.items

        self.assertEqual(10, len(messages))

        message_contents = {m.name:m for m in messages}
        expected_messages = [message_contents['history%d' % i] for i in range(49, 39, -1)]

        self.assertEqual(expected_messages, messages,
                msg='Expected 10 messages')
        
        history = history.next()
        messages = history.items

        self.assertEqual(10, len(messages))

        message_contents = {m.name:m for m in messages}
        expected_messages = [message_contents['history%d' % i] for i in range(39, 29, -1)]

        self.assertEqual(expected_messages, messages,
                msg='Expected 10 messages')
        
        history = history.next()
        messages = history.items

        self.assertEqual(10, len(messages))

        message_contents = {m.name:m for m in messages}
        expected_messages = [message_contents['history%d' % i] for i in range(29, 19, -1)]

        self.assertEqual(expected_messages, messages,
                msg='Expected 10 messages')
        
    def test_channel_history_paginate_forwards_first(self):
        history0 = self.ably.channels[
            self.protocol_channel_name('persisted:channelhistory_paginate_first_f')]

        for i in range(50):
            history0.publish('history%d' % i, str(i))

        history = history0.history(direction='forwards', limit=10)
        messages = history.items

        self.assertEqual(10, len(messages))

        message_contents = {m.name:m for m in messages}
        expected_messages = [message_contents['history%d' % i] for i in range(0, 10)]

        self.assertEqual(expected_messages, messages,
                msg='Expected 10 messages')
        
        history = history.next()
        messages = history.items

        self.assertEqual(10, len(messages))

        message_contents = {m.name:m for m in messages}
        expected_messages = [message_contents['history%d' % i] for i in range(10, 20)]

        self.assertEqual(expected_messages, messages,
                msg='Expected 10 messages')
        
        history = history.first()
        messages = history.items

        self.assertEqual(10, len(messages))

        message_contents = {m.name:m for m in messages}
        expected_messages = [message_contents['history%d' % i] for i in range(0, 10)]

        self.assertEqual(expected_messages, messages,
                msg='Expected 10 messages')
        
    def test_channel_history_paginate_backwards_rel_first(self):
        history0 = self.ably.channels[
            self.protocol_channel_name('persisted:channelhistory_paginate_first_b')]

        for i in range(50):
            history0.publish('history%d' % i, str(i))

        history = history0.history(direction='backwards', limit=10)
        messages = history.items

        self.assertEqual(10, len(messages))

        message_contents = {m.name:m for m in messages}
        expected_messages = [message_contents['history%d' % i] for i in range(49, 39, -1)]

        self.assertEqual(expected_messages, messages,
                msg='Expected 10 messages')
        
        history = history.next()
        messages = history.items

        self.assertEqual(10, len(messages))

        message_contents = {m.name:m for m in messages}
        expected_messages = [message_contents['history%d' % i] for i in range(39, 29, -1)]

        self.assertEqual(expected_messages, messages,
                msg='Expected 10 messages')
        
        history = history.first()
        messages = history.items

        self.assertEqual(10, len(messages))

        message_contents = {m.name:m for m in messages}
        expected_messages = [message_contents['history%d' % i] for i in range(49, 39, -1)]

        self.assertEqual(expected_messages, messages,
                msg='Expected 10 messages')

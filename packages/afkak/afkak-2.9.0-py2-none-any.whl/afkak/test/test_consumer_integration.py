# -*- coding: utf-8 -*-
# Copyright (C) 2015 Cyan, Inc.

import os

import logging

from nose.twistedtools import threaded_reactor, deferred
from twisted.internet.defer import inlineCallbacks, returnValue, setDebugging
from twisted.internet.base import DelayedCall

from afkak import (Consumer, create_message, )
from afkak.common import (
    ProduceRequest, ConsumerFetchSizeTooSmall,
    OFFSET_EARLIEST, OFFSET_COMMITTED,
    )
from afkak.consumer import FETCH_BUFFER_SIZE_BYTES
from fixtures import ZookeeperFixture, KafkaFixture
from testutil import (
    kafka_versions, KafkaIntegrationTestCase, async_delay,
    random_string,
    )

from twisted.trial import unittest

log = logging.getLogger(__name__)

DEBUGGING = True
setDebugging(DEBUGGING)
DelayedCall.debug = DEBUGGING


class TestConsumerIntegration(KafkaIntegrationTestCase, unittest.TestCase):

    # Default partition
    partition = 0

    @classmethod
    def setUpClass(cls):
        if not os.environ.get('KAFKA_VERSION'):  # pragma: no cover
            log.warning("WARNING: KAFKA_VERSION not found in environment")
            return

        DEBUGGING = True
        setDebugging(DEBUGGING)
        DelayedCall.debug = DEBUGGING

        # Single zookeeper, 3 kafka brokers
        zk_chroot = random_string(10)
        replicas = 3
        partitions = 2

        cls.zk = ZookeeperFixture.instance()
        kk_args = [cls.zk.host, cls.zk.port, zk_chroot, replicas, partitions]
        cls.kafka_brokers = [
            KafkaFixture.instance(i, *kk_args) for i in range(replicas)]
        # server is used by our superclass when creating the client...
        cls.server = cls.kafka_brokers[0]

        # Startup the twisted reactor in a thread. We need this before the
        # the KafkaClient can work, since KafkaBrokerClient relies on the
        # reactor for its TCP connection
        cls.reactor, cls.thread = threaded_reactor()

    @classmethod
    def tearDownClass(cls):
        if not os.environ.get('KAFKA_VERSION'):  # pragma: no cover
            log.warning("WARNING: KAFKA_VERSION not found in environment")
            return

        for broker in cls.kafka_brokers:
            broker.close()
        cls.zk.close()

    @inlineCallbacks
    def send_messages(self, partition, messages):
        messages = [create_message(self.msg(str(msg))) for msg in messages]
        produce = ProduceRequest(self.topic, partition, messages=messages)
        resp, = yield self.client.send_produce_request([produce])

        self.assertEqual(resp.error, 0)

        returnValue([x.value for x in messages])

    def assert_message_count(self, messages, num_messages):
        # Make sure we got them all
        self.assertEqual(len(messages), num_messages)

        # Make sure there are no duplicates
        self.assertEqual(len(set(messages)), num_messages)

    @kafka_versions("all")
    @deferred(timeout=15)
    @inlineCallbacks
    def test_consumer(self):
        yield async_delay(3)  # 0.8.1.1 fails otherwise

        yield self.send_messages(self.partition, range(0, 100))

        # Create a consumer.
        consumer = self.consumer()

        # Check for messages on the processor
        self.assertFalse(consumer.processor._messages)

        # Start the consumer from the beginning
        start_d = consumer.start(OFFSET_EARLIEST)

        # Send some more messages
        yield self.send_messages(self.partition, range(100, 200))

        # Loop waiting for all the messages to show up
        while len(consumer.processor._messages) < 200:
            # Wait a bit for them to arrive
            yield async_delay()

        # Make sure we got all 200
        self.assertEqual(len(consumer.processor._messages), 200)

        # Send some more messages
        yield self.send_messages(self.partition, range(200, 250))
        # Loop waiting for the new message
        while len(consumer.processor._messages) < 250:
            # Wait a bit for them to arrive
            yield async_delay()

        # make sure we got them all
        self.assert_message_count(consumer.processor._messages, 250)

        # Clean up
        consumer.stop()
        self.successResultOf(start_d)

    @kafka_versions("all")
    @deferred(timeout=15)
    @inlineCallbacks
    def test_large_messages(self):
        # Produce 10 "normal" size messages
        small_messages = yield self.send_messages(
            0, [str(x) for x in range(10)])

        # Produce 10 messages that are large (bigger than default fetch size)
        large_messages = yield self.send_messages(
          0, [random_string(FETCH_BUFFER_SIZE_BYTES * 3) for x in range(10)])

        # Consumer should still get all of them
        consumer = self.consumer()

        # Start the consumer from the beginning
        d = consumer.start(OFFSET_EARLIEST)

        # Loop waiting for all the messages to show up
        while len(consumer.processor._messages) < 20:
            # Wait a bit for them to arrive
            yield async_delay()

        expected_messages = set(small_messages + large_messages)
        actual_messages = set([x.message.value for x in
                               consumer.processor._messages])
        self.assertEqual(expected_messages, actual_messages)

        # Clean up
        consumer.stop()
        self.successResultOf(d)

    @kafka_versions("all")
    @deferred(timeout=15)
    @inlineCallbacks
    def test_huge_messages(self):
        # Produce 10 "normal" size messages
        yield self.send_messages(0, [str(x) for x in range(10)])

        # Setup a max buffer size for the consumer, and put a message in
        # Kafka that's bigger than that
        MAX_FETCH_BUFFER_SIZE_BYTES = (256 * 1024) - 10
        huge_message, = yield self.send_messages(
            0, [random_string(MAX_FETCH_BUFFER_SIZE_BYTES + 10)])

        # Create a consumer with the (smallish) max buffer size
        consumer = self.consumer(max_buffer_size=MAX_FETCH_BUFFER_SIZE_BYTES)

        # This consumer fails to get the message, and errbacks the start
        # deferred
        d = consumer.start(OFFSET_EARLIEST)

        # Loop waiting for the errback to be called
        while not d.called:
            # Wait a bit for them to arrive
            yield async_delay()
        # Make sure the failure is as expected
        self.failureResultOf(d, ConsumerFetchSizeTooSmall)

        # Make sure the smaller, earlier messages were delivered
        self.assert_message_count(consumer.processor._messages, 10)

        # last offset seen
        last_offset = consumer.processor._messages[-1].offset

        # Stop the consumer: d already errbacked, but stop still must be called
        consumer.stop()

        # Create a consumer with no fetch size limit
        big_consumer = self.consumer()
        # Start just past the last message processed
        d = big_consumer.start(last_offset + 1)
        # Consume giant message successfully
        while not big_consumer.processor._messages:
            # Wait a bit for it to arrive
            yield async_delay()

        self.assertEqual(big_consumer.processor._messages[0].message.value,
                         huge_message)

        # Clean up
        big_consumer.stop()
        self.successResultOf(d)

    @kafka_versions("0.8.1", "0.8.1.1", "0.8.2.1", "0.8.2.2", "0.9.0.1")
    @deferred(timeout=15)
    @inlineCallbacks
    def test_consumer_restart(self):
        sent_messages = yield self.send_messages(self.partition, range(0, 100))

        # Create & start our default consumer (auto-commit)
        consumer = self.consumer()

        # Check for messages on the processor
        self.assertFalse(consumer.processor._messages)

        # Start the consumer from the beginning
        start_d = consumer.start(OFFSET_EARLIEST)

        # Send some more messages
        sent_messages += yield self.send_messages(
            self.partition, range(100, 200))

        # Loop waiting for all the messages to show up
        while len(consumer.processor._messages) < 200:
            # Wait a bit for them to arrive
            yield async_delay()

        # Make sure we got all 200
        self.assertEqual(len(consumer.processor._messages), 200)

        # Stop the consumer and record offset at which to restart (next after
        # last processed message offset)
        offset = consumer.stop() + 1
        self.successResultOf(start_d)

        # Send some more messages
        sent_messages += yield self.send_messages(
            self.partition, range(200, 250))
        # Restart the consumer at the returned offset
        start_d2 = consumer.start(offset)
        # Loop waiting for the new message
        while len(consumer.processor._messages) < 250:
            # Wait a bit for them to arrive
            yield async_delay()

        # make sure we got them all
        self.assert_message_count(consumer.processor._messages, 250)
        expected_messages = set(sent_messages)
        actual_messages = set([x.message.value for x in
                               consumer.processor._messages])
        self.assertEqual(expected_messages, actual_messages)

        # Clean up
        consumer.stop()
        self.successResultOf(start_d2)

    @kafka_versions("0.8.2.1", "0.8.2.2", "0.9.0.1")
    @deferred(timeout=15)
    @inlineCallbacks
    def test_consumer_commit_offsets(self):
        # Start off by sending messages before the consumer is started
        yield self.send_messages(self.partition, range(0, 100))

        # Create a consumer, allow commit, disable auto-commit
        consumer = self.consumer(consumer_group=self.id(),
                                 auto_commit_every_n=0,
                                 auto_commit_every_ms=0)

        # Check for messages on the processor
        self.assertFalse(consumer.processor._messages)

        # Start the consumer from the beginning
        start_d = consumer.start(OFFSET_EARLIEST)

        # Send some more messages
        yield self.send_messages(self.partition, range(100, 200))

        # Loop waiting for all the messages to show up
        while len(consumer.processor._messages) < 200:
            # Wait a bit for them to arrive
            yield async_delay()

        # Make sure we got all 200
        self.assertEqual(len(consumer.processor._messages), 200)

        # Stop the consumer
        consumer.stop()
        self.successResultOf(start_d)
        # Commit the offsets
        yield consumer.commit()

        # Send some more messages
        last_batch = yield self.send_messages(self.partition, range(200, 300))

        # Create another consumer
        consumer2 = self.consumer(consumer_group=self.id(),
                                  auto_commit_every_n=0,
                                  auto_commit_every_ms=0)
        # Start it at the last offset for the group
        start_d2 = consumer2.start(OFFSET_COMMITTED)
        # Loop waiting for all the messages to show up
        while len(consumer2.processor._messages) < 100:
            # Wait a bit for them to arrive
            yield async_delay()
        # Make sure we got all 100, and the right 100
        self.assertEqual(len(consumer2.processor._messages), 100)
        self.assertEqual(last_batch, [x.message.value for x in
                                      consumer2.processor._messages])

        # Stop the consumer
        consumer2.stop()
        self.successResultOf(start_d2)

    def consumer(self, **kwargs):
        def make_processor():
            def default_message_proccessor(consumer_instance, messages):
                """Default message processing function

                   Strictly for testing.
                   Just adds the messages to its own _messages attr
                """
                default_message_proccessor._messages.extend(messages)
                return None

            # Setup a list property '_messages' on the processor function
            default_message_proccessor._messages = []

            return default_message_proccessor

        topic = kwargs.pop('topic', self.topic)
        partition = kwargs.pop('partition', self.partition)
        processor = kwargs.pop('processor', make_processor())
        group = kwargs.pop('consumer_group', None)

        return Consumer(self.client, topic, partition, processor, group,
                        **kwargs)

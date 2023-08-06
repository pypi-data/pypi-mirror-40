# coding=utf-8
# Licensed Materials - Property of IBM
# Copyright IBM Corp. 2019

import datetime
from tempfile import gettempdir
import json
import streamsx.spl.op
import streamsx.spl.types
from streamsx.topology.schema import CommonSchema


def subscribe(topology, topic, appConfigName, schema, group=None, name=None):
    """Subscribe to messages from a Kafka broker for a single topic.

    Adds a Kafka consumer that subscribes to a topic
    and converts each message to a stream tuple.

    Args:
        topology(Topology): Topology that will contain the stream of messages.
        topic(str): Topic to subscribe messages from.
        appConfigName(str): The name of the application configuration containing the consumer configurations, at minimum the ``bootstrap.servers`` property. Must not be set to ``None``.
        schema(StreamSchema): Schema for returned stream.
        group(str): Kafka consumer group identifier. When not specified it default to the job name with `topic` appended separated by an underscore.
        name(str): Consumer name in the Streams context, defaults to a generated name.

    Returns:
         Stream: Stream containing messages.
    """
    if schema is CommonSchema.Json:
        msg_attr_name='jsonString'
    elif schema is CommonSchema.String:
        msg_attr_name='string'
    else:
        raise TypeError(schema)

    if group is None:
        group = streamsx.spl.op.Expression.expression('getJobName() + "_" + "' + str(topic) + '"')

    if name is None:
        name = topic

    _op = _KafkaConsumer(topology, schema=schema, outputMessageAttributeName=msg_attr_name, appConfigName=appConfigName, topic=topic, groupId=group, name=name)
    return _op.stream


def publish(stream, topic, appConfigName, name=None):
    """Publish messages to a topic in a Kafka broker.

    Adds a Kafka producer where each tuple on `stream` is
    published as a stream message.

    Args:
        stream(Stream): Stream of tuples to published as messages.
        topic(str): Topic to publish messages to.
        appConfigName(str): The name of the application configuration containing the producer configurations, at minimum the ``bootstrap.servers`` property. Must not be set to ``None``.
        name(str): Producer name in the Streams context, defaults to a generated name.

    Returns:
        streamsx.topology.topology.Sink: Stream termination.
    """
    if stream.oport.schema == CommonSchema.Json:
        msg_attr = 'jsonString'
    elif stream.oport.schema == CommonSchema.String:
        msg_attr = 'string'
    else:
        raise TypeError(schema)

    _op = _KafkaProducer (stream, appConfigName=appConfigName, topic=topic)
    _op.params['messageAttribute'] = _op.attribute(stream, msg_attr)

    return streamsx.topology.topology.Sink(_op)

class _KafkaConsumer(streamsx.spl.op.Source):
  def __init__(self, topology, schema, vmArg=None, appConfigName=None, clientId=None, commitCount=None, groupId=None, outputKeyAttributeName=None, outputMessageAttributeName=None, outputTimestampAttributeName=None, outputOffsetAttributeName=None, outputPartitionAttributeName=None, outputTopicAttributeName=None, partition=None, propertiesFile=None, startPosition=None, startOffset=None, startTime=None, topic=None, triggerCount=None, userLib=None, name=None):
        kind="com.ibm.streamsx.kafka::KafkaConsumer"
        inputs=None
        schemas=schema
        params = dict()
        if vmArg is not None:
            params['vmArg'] = vmArg
        if appConfigName is not None:
            params['appConfigName'] = appConfigName
        if clientId is not None:
            params['clientId'] = clientId
        if commitCount is not None:
            params['commitCount'] = commitCount
        if groupId is not None:
           params['groupId'] = groupId
        if outputKeyAttributeName is not None:
            params['outputKeyAttributeName'] = outputKeyAttributeName
        if outputMessageAttributeName is not None:
            params['outputMessageAttributeName'] = outputMessageAttributeName
        if outputTimestampAttributeName is not None:
            params['outputTimestampAttributeName'] = outputTimestampAttributeName
        if outputOffsetAttributeName is not None:
            params['outputOffsetAttributeName'] = outputOffsetAttributeName
        if outputPartitionAttributeName is not None:
            params['outputPartitionAttributeName'] = outputPartitionAttributeName
        if outputTopicAttributeName is not None:
            params['outputTopicAttributeName'] = outputTopicAttributeName
        if partition is not None:
            params['partition'] = partition
        if propertiesFile is not None:
            params['propertiesFile'] = propertiesFile
        if startPosition is not None:
            params['startPosition'] = startPosition
        if startOffset is not None:
            params['startOffset'] = startOffset
        if startTime is not None:
            params['startTime'] = startTime
        if topic is not None:
            params['topic'] = topic
        if triggerCount is not None:
            params['triggerCount'] = triggerCount
        if userLib is not None:
            params['userLib'] = userLib
        super(_KafkaConsumer, self).__init__(topology,kind,schemas,params,name)


class _KafkaProducer(streamsx.spl.op.Sink):
    def __init__(self, stream, vmArg=None, appConfigName=None, clientId=None, keyAttribute=None, messageAttribute=None, partitionAttribute=None, propertiesFile=None, timestampAttribute=None, topicAttribute=None, topic=None, userLib=None, name=None):
        topology = stream.topology
        kind="com.ibm.streamsx.kafka::KafkaProducer"
        params = dict()
        if vmArg is not None:
            params['vmArg'] = vmArg
        if appConfigName is not None:
            params['appConfigName'] = appConfigName
        if keyAttribute is not None:
            params['keyAttribute'] = keyAttribute
        if clientId is not None:
            params['clientId'] = clientId
        if messageAttribute is not None:
            params['messageAttribute'] = messageAttribute
        if partitionAttribute is not None:
            params['partitionAttribute'] = partitionAttribute
        if propertiesFile is not None:
            params['propertiesFile'] = propertiesFile
        if timestampAttribute is not None:
            params['timestampAttribute'] = timestampAttribute
        if topicAttribute is not None:
            params['topicAttribute'] = topicAttribute
        if topic is not None:
            params['topic'] = topic
        if userLib is not None:
            params['userLib'] = userLib
        super(_KafkaProducer, self).__init__(kind,stream,params,name)

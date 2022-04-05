# PubSub util

Util for subscribing or publishing messages to Google's PubSub subscriptions/topics.

## run_subscriber

Creates and a subscriber to some PubSub subscription. A callback function will be called for each new message. This 
function does not acknowledge messages, it just passes them on to a callback function. The amount of time subscriber
will listen for messages is dictated by the timeout parameter (if it is set to None, it waits indefinitely). Flow 
control is managed by max_concurrent_messages parameter.

## publish

Publishes a string message to a given PubSub topic, encoding it with utf-8. 

## publish_bytes

Publishes bytes to a given PubSub topic

## Publisher class

Creates a publisher client and reuses it to send messages to a single pubsub topic.
Awaits futures in batches - dictated by futures_batch_size parameter, or by calling 
flush()

from concurrent import futures
from typing import Callable

from google.cloud import pubsub_v1


def run_subscriber(
        project_id: str,
        subscription_id: str,
        callback: Callable[[pubsub_v1.subscriber.message.Message], None],
        timeout: int = None,
        max_concurrent_messages: int = 1000  # pubsub_v1.types.FlowControl default
):
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    flow_control = pubsub_v1.types.FlowControl(max_messages=max_concurrent_messages)

    streaming_pull_future = subscriber.subscribe(
        subscription_path,
        callback=callback,
        flow_control=flow_control,
    )
    print(f"Listening for messages on {subscription_path}..\n")

    with subscriber:
        try:
            streaming_pull_future.result(timeout=timeout)
        except futures.TimeoutError:
            streaming_pull_future.cancel()  # Trigger the shutdown.
            streaming_pull_future.result()  # Block until the shutdown is complete.


class Publisher:
    def __init__(self, project: str, topic: str):
        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = self.publisher.topic_path(project, topic)

    def send_bytes(self, message: bytes):
        """Send bytes and wait for the future"""
        future = self.publisher.publish(self.topic_path, message)
        futures.wait([future])

    def send(self, message: str):
        """Encode with utf-8, send and wait for the future"""
        self.send_bytes(message.encode("utf-8"))


def publish(project: str, topic: str, message: str) -> None:
    """Create a one-off publisher, encode the message with utf-8, send and wait for
    the future """
    Publisher(project, topic).send(message)


def publish_bytes(project: str, topic: str, message: bytes) -> None:
    """Create a one-off publisher, send bytes and wait for the future"""
    Publisher(project, topic).send_bytes(message)

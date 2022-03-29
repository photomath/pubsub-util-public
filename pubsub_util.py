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


def publish(project: str, topic: str, message: str) -> None:
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project, topic)
    future = publisher.publish(topic_path, message.encode("utf-8"))
    futures.wait([future])

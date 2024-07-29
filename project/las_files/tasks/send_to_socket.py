from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from config.celery import celery


@celery.task(
    ignore_result=True,
    time_limit=5,
    soft_time_limit=3,
    default_retry_delay=5,
)
def send_to_socket(message, group_name: str) -> None:
    async_to_sync(get_channel_layer().group_send)(
        group_name, {"type": "send.message", "message": message}
    )


def send_to_general_layer(
    message_type: str,
    data,
) -> None:

    send_to_socket(
        group_name="general",
        message={
            "message_type": message_type,
            "data": data,
        },
    )

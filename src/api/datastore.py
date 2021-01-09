from google.cloud import datastore
from google.cloud.datastore import Entity

import configuration
import logging
from uuid import uuid1
from enum import auto, IntEnum

client = datastore.Client()


class RequestStatus(IntEnum):
    NEW = auto()
    PROCESSING = auto()
    SUCCESS = auto()
    FAILED = auto()


def _generate_new_request_entity() -> Entity:
    request_id = client.key(configuration.GoogleConfigurations.datastore_requests_kind, str(uuid1()).replace("-", ""))

    entity = client.get(key=request_id)
    while entity is not None:
        entity = client.get(key=request_id)

    return datastore.Entity(request_id)


def create_request(hash_tag: str, count: int):

    request_entity = _generate_new_request_entity()

    request_entity.update({
        "hash_tag": hash_tag,
        "count": count,
        "status": RequestStatus.NEW,
    })

    client.put(request_entity)

    return request_entity


def _get_request(request_id: str):
    return client.get(client.key(configuration.GoogleConfigurations.datastore_requests_kind, request_id))


def update_request(request_id: str, status: RequestStatus):
    entity = _get_request(request_id=request_id)
    entity.update({
        "status": status
    })
    client.put(entity)

    logging.info(f"Updated request {request_id} with status {status}")


if __name__ == "__main__":
    request = create_request("puppy", 5)
    logging.info(f"Created request: {request}")
    update_request(request.key.name, status=RequestStatus.FAILED)

import typing as T

from ry_redis_bus.helpers import RedisInfo
from ry_redis_bus.redis_client_base import RedisClientBase
from ryutils.firebase.firebase_manager import CollectionConfig, FirebaseManager
from ryutils.verbose import Verbose


class FirebaseRedisClient(RedisClientBase):
    """Redis client wrapper around FirebaseManager."""

    def __init__(
        self,
        verbose: Verbose,
        redis_info: RedisInfo,
        collection_configs: list[CollectionConfig],
        message_handlers: T.Optional[dict[T.Any, T.Callable[..., T.Any]]] = None,
    ):
        super().__init__(redis_info=redis_info, verbose=verbose)
        self.firebase_manager = FirebaseManager(
            verbose=verbose,
            collection_configs=collection_configs,
            publish_func=self.publish,
            message_handlers=message_handlers,
        )
        self.message_handlers = message_handlers or {}

    def is_active(self) -> bool:
        return self.firebase_manager.is_active()

    def init(self) -> None:
        self.firebase_manager.init()
        for channel, handler in self.message_handlers.items():
            self.subscribe(channel, handler)

    def step(self) -> None:
        super().step()
        self.firebase_manager.step()

    @property
    def collection_configs(self) -> list[CollectionConfig]:
        return self.firebase_manager.collection_configs

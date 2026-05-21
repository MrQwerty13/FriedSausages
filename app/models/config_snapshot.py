# models/config_snapshot.py
from datetime import datetime


class ConfigSnapshot:
    def __init__(
        self,
        id: int,
        device_id: int,
        version_number: str,
        config_text: str,
        config_hash: str,
        collected_by: str,
        collected_at: datetime,
        source: str,
    ):
        self._id = id
        self._device_id = device_id
        self._version_number = version_number
        self._config_text = config_text
        self._config_hash = config_hash
        self._collected_by = collected_by
        self._collected_at = collected_at
        self._source = source

    @property
    def id(self) -> int:
        return self._id

    @property
    def device_id(self) -> int:
        return self._device_id

    @property
    def version_number(self) -> str:
        return self._version_number

    @property
    def config_text(self) -> str:
        return self._config_text

    @property
    def config_hash(self) -> str:
        return self._config_hash

    @property
    def collected_by(self) -> str:
        return self._collected_by

    @property
    def collected_at(self) -> datetime:
        return self._collected_at

    @property
    def source(self) -> str:
        return self._source
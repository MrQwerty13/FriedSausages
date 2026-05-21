# models/alert.py
from datetime import datetime


class Alert:
    def __init__(
        self,
        id: int,
        device_id: int,
        type: str,
        severity: str,
        message: str,
        status: str,
        created_at: datetime,
    ):
        self._id = id
        self._device_id = device_id
        self._type = type
        self._severity = severity
        self._message = message
        self._status = status
        self._created_at = created_at

    @property
    def id(self) -> int:
        return self._id

    @property
    def device_id(self) -> int:
        return self._device_id

    @property
    def type(self) -> str:
        return self._type

    @property
    def severity(self) -> str:
        return self._severity

    @property
    def message(self) -> str:
        return self._message

    @property
    def status(self) -> str:
        return self._status

    @property
    def created_at(self) -> datetime:
        return self._created_at
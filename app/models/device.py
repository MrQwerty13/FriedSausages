# models/device.py
from datetime import datetime
from typing import Optional


class Device:
    def __init__(
        self,
        id: int,
        name: str,
        ip_address: str,
        vendor: str,
        device_type: str,
        os_version: Optional[str],
        status: str,
        created_at: datetime,
        updated_at: datetime,
    ):
        self._id = id
        self._name = name
        self._ip_address = ip_address
        self._vendor = vendor
        self._device_type = device_type
        self._os_version = os_version
        self._status = status
        self._created_at = created_at
        self._updated_at = updated_at

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def ip_address(self) -> str:
        return self._ip_address

    @property
    def vendor(self) -> str:
        return self._vendor

    @property
    def device_type(self) -> str:
        return self._device_type

    @property
    def os_version(self) -> Optional[str]:
        return self._os_version

    @property
    def status(self) -> str:
        return self._status

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        return self._updated_at
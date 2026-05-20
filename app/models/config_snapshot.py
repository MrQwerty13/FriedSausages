# /app/models/config_snapshot.py

class ConfigSnapshot:
    def __init__(self):
        self._id = None
        self._device_id = None
        self._version_number = None
        self._config_text = None
        self._config_hash = None
        self._collected_by = None
        self._collected_at = None
        self._source = None

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def device_id(self):
        return self._device_id

    @device_id.setter
    def device_id(self, value):
        self._device_id = value

    @property
    def version_number(self):
        return self._version_number

    @version_number.setter
    def version_number(self, value):
        self._version_number = value

    @property
    def config_text(self):
        return self._config_text

    @config_text.setter
    def config_text(self, value):
        self._config_text = value

    @property
    def config_hash(self):
        return self._config_hash

    @config_hash.setter
    def config_hash(self, value):
        self._config_hash = value

    @property
    def collected_by(self):
        return self._collected_by

    @collected_by.setter
    def collected_by(self, value):
        self._collected_by = value

    @property
    def collected_at(self):
        return self._collected_at

    @collected_at.setter
    def collected_at(self, value):
        self._collected_at = value

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, value):
        self._source = value
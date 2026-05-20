# /app/models/config_diff.py

class ConfigDiff:
    def __init__(self):
        self._id = None
        self._device_id = None
        self._old_snapshot_id = None
        self._new_snapshot_id = None
        self._diff_text = None
        self._risk_level = None
        self._summary = None
        self._created_at = None

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
    def old_snapshot_id(self):
        return self._old_snapshot_id

    @old_snapshot_id.setter
    def old_snapshot_id(self, value):
        self._old_snapshot_id = value

    @property
    def new_snapshot_id(self):
        return self._new_snapshot_id

    @new_snapshot_id.setter
    def new_snapshot_id(self, value):
        self._new_snapshot_id = value

    @property
    def diff_text(self):
        return self._diff_text

    @diff_text.setter
    def diff_text(self, value):
        self._diff_text = value

    @property
    def risk_level(self):
        return self._risk_level

    @risk_level.setter
    def risk_level(self, value):
        self._risk_level = value

    @property
    def summary(self):
        return self._summary

    @summary.setter
    def summary(self, value):
        self._summary = value

    @property
    def created_at(self):
        return self._created_at

    @created_at.setter
    def created_at(self, value):
        self._created_at = value
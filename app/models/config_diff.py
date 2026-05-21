# /app/models/config_diff.py


class ConfigDiff:
    def __init__(self, id=None, device_id=None, old_snapshot_id=None, new_snapshot_id=None, diff_text=None, risk_level=None, created_at=None):
        self.id = id
        self.device_id = device_id
        self.old_snapshot_id = old_snapshot_id
        self.new_snapshot_id = new_snapshot_id
        self.diff_text = diff_text
        self.risk_level = risk_level
        self.created_at = created_at
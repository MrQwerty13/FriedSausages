# /app/models/compliance_result.py


class ComplianceResult:
    def __init__(self, id=None, device_id=None, snapshot_id=None, rule_id=None, status=None, details=None, created_at=None):
        self.id = id
        self.device_id = device_id
        self.snapshot_id = snapshot_id
        self.rule_id = rule_id
        self.status = status
        self.details = details
        self.created_at = created_at
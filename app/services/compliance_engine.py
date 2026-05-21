class ComplianceEngine:
    def __init__(self, rules):
        self.rules = rules

    def check(self, config_data):
        results = []

        for rule in self.rules:
            rule_name = rule["name"]
            target = rule["target"]
            expected = rule["expected"]

            actual = config_data.get(target, "")

            passed = expected in actual

            results.append({
                "rule": rule_name,
                "target": target,
                "passed": passed,
                "expected": expected
            })

        return results

    @staticmethod
    def summary(results):
        total = len(results)
        passed = len([r for r in results if r["passed"]])
        failed = total - passed

        return {
            "total": total,
            "passed": passed,
            "failed": failed
        }
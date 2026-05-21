import difflib


class ConfigDiff:
    @staticmethod
    def compare(old_config, new_config):
        old_lines = old_config.splitlines()
        new_lines = new_config.splitlines()

        diff = difflib.unified_diff(
            old_lines,
            new_lines,
            fromfile="old_config",
            tofile="new_config",
            lineterm=""
        )

        return "\n".join(diff)

    @staticmethod
    def has_changes(old_config, new_config):
        return old_config.strip() != new_config.strip()
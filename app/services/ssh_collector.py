import parsmiko


class SSHCollector:
    def __init__(self, host, username, password=None, key_path=None, port=22):
        self.host = host
        self.username = username
        self.password = password
        self.key_path = key_path
        self.port = port

    def connect(self):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        if self.key_path:
            client.connect(
                self.host,
                port=self.port,
                username=self.username,
                key_filename=self.key_path,
                timeout=10
            )
        else:
            client.connect(
                self.host,
                port=self.port,
                username=self.username,
                password=self.password,
                timeout=10
            )

        return client

    def run_command(self, command):
        client = self.connect()
        stdin, stdout, stderr = client.exec_command(command)

        result = stdout.read().decode()
        error = stderr.read().decode()

        client.close()

        if error:
            raise RuntimeError(error)

        return result

    def collect_config(self, commands):
        data = {}

        for name, command in commands.items():
            data[name] = self.run_command(command)

        return data
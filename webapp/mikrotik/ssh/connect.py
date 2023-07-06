import paramiko

class SSHConnection:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect(self):
        try:
            self.client.connect(
                hostname=self.host,
                port=self.port,
                username=self.username,
                password=self.password
            )
            print("Conexión SSH establecida.")
            return 1
        except paramiko.AuthenticationException:
            print("Error de autenticación al conectar por SSH.")
            return 0
        except paramiko.SSHException as ssh_exc:
            print(f"Error al establecer la conexión SSH: {str(ssh_exc)}")
            return 0
        except paramiko.ssh_exception.NoValidConnectionsError as no_conn_exc:
            print(f"No se pudo establecer una conexión SSH: {str(no_conn_exc)}")
            return 0
        except Exception as e:
            print(f"Error inesperado: {str(e)}")

    def execute_command(self, command):
        stdin, stdout, stderr = self.client.exec_command(command)
        output = stdout.read().decode()
        print(output)
        return output

    def close(self):
        self.client.close()
        print("Conexión SSH cerrada.")


# Ejemplo de uso
host = '10.200.3.176'
port = 22
username = 'admin'
password = '3l1pgo%123'

ssh_connection = SSHConnection(host, port, username, password)
response = ssh_connection.connect()
if response:
    print("connected")
    ssh_connection.execute_command('?')
    ssh_connection.execute_command('quit')
    #ssh_connection.execute_command('comando_2')

    ssh_connection.close()
else:
    print("Not connected")
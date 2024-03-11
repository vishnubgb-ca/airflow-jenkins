import paramiko
import os

#airflow_instance_private_key = os.environ["airflow_instance_private_key"]
airflow_instance_ip = os.environ["airflow_instance_ip"]
print(airflow_instance_ip)
ssh_client=paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
key = paramiko.RSAKey.from_private_key_file('test.pem')
print("connecting to instance........")
ssh_client.connect(hostname = airflow_instance_ip, username='ubuntu', pkey = key)
print("connected")
ftp_client=ssh_client.open_sftp()
commands = ["sudo docker exec b8ab62bbea5e airflow dags trigger -c airflow_dag_id refresh_dags"]

for cmd in commands:
    stdin, stdout, stderr = ssh_client.exec_command(cmd)
    print(stdout.read())
    print(stderr.read())

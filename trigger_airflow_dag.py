import paramiko
import os

airflow_instance_private_key = os.environ["airflow_instance_private_key"]
#key_file = "/home/ubuntu/MLOps_Repo/backend/mlflow_as_a_service/test.pem"
airflow_instance_ip = os.environ["airflow_instance_ip"]
ssh_client=paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
key = paramiko.RSAKey.from_private_key_file(airflow_instance_private_key)
ssh_client.connect(hostname = '172.31.61.199', username='ubuntu', pkey = key)
ftp_client=ssh_client.open_sftp()
commands = ["docker exec df677905f4d2 airflow trigger_dag -c airflow-jenkins-dag refresh_dags"]

for cmd in commands:
    stdin, stdout, stderr = ssh_client.exec_command(cmd)
    print(stdout.read())
    print(stderr.read())

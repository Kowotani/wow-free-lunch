import boto3
import paramiko
import sys


# =========
# Constants
# =========

INSTANCE_ID = 'instance-id'
REGION_NAME = 'us-west-1'
USER = 'ec2-user'
PEM_FILE = 'WoWFreeLunch.pem'


# =========
# Functions
# =========

def print_std(stream):
    data = stream.read().splitlines()
    for line in data:
        print(line)


def lambda_handler(event, context):

    # get ec2 instance
    ec2 = boto3.resource('ec2', region_name=REGION_NAME)
    instance = ec2.Instance(INSTANCE_ID)
    
    # get ssh client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    privkey = paramiko.RSAKey.from_private_key_file(PEM_FILE)
    
    ssh.connect(
        hostname=instance.private_dns_name, 
        username=USER, 
        pkey=privkey
    )
    
    # call script
    cmd = 'python /home/ec2-user/environment/wow-free-lunch/server/scripts/load_auctions.py'
    stdin, stdout, stderr = ssh.exec_command(cmd)
    
    stdin.flush()
    print('stdout')
    print('------------')
    print_std(stdout)
    print('stderr')
    print('------------')
    print_std(stderr)
        
    ssh.close()

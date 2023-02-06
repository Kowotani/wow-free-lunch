# https://github.com/gpoudel/ssh-ec2-lambda/blob/master/lambda_function.py
# https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-lifecycle.html

import os
import paramiko
import time


# =========
# Constants
# =========

EC2_PRIVATE_DNS_NAME = os.getenv('EC2_PRIVATE_DNS_NAME')
REGION_NAME = 'us-west-1'
USER = 'ec2-user'
PEM_FILE = 'WoWFreeLunch.pem'


# =========
# Functions
# =========

def std_print(name, stream):
    
    print(name)
    print('------------')
    data = stream.read().splitlines()
    for line in data:
        print(line)
    print('------------')


def lambda_handler(event, context):
    
    # get ssh client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    privkey = paramiko.RSAKey.from_private_key_file(PEM_FILE)
    
    print('Connect SSH')
    ssh.connect(
        hostname=EC2_PRIVATE_DNS_NAME,
        username=USER, 
        pkey=privkey
    )

    # call command
    print('Call /scripts/load_auctions')
    cmd = 'python3 /home/ec2-user/environment/wow-free-lunch/server/scripts/load_auctions.py'
    stdin, stdout, stderr = ssh.exec_command(cmd)
    print('Finished /scripts/load_auctions')
    
    # stdin.flush()
    std_print('stdout', stdout)
    std_print('stderr', stderr)
    
    # close SSH
    ssh.close()

    return {
        'message': 'Completed /scripts/load_auctions'
    }
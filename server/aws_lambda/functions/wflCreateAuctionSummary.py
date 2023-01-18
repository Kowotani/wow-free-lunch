# https://github.com/gpoudel/ssh-ec2-lambda/blob/master/lambda_function.py
# https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-lifecycle.html

import boto3
import paramiko
import time


# =========
# Constants
# =========

INSTANCE_ID = 'i-056f7b22ff2f852aa'
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


def lambda_handler(event, context):
    
    # get instance
    ec2 = boto3.resource('ec2', region_name=REGION_NAME)
    instance = ec2.Instance(INSTANCE_ID)
    initial_state = instance.state['Name']

    # is instance already runnning
    if instance.state['Name'] == 'running':
        print('Instance already running')

    else:
    
        # start instance, if stopped
        if instance.state['Name'] == 'stopped':
            print('Starting instance')
            instance.start()
            time.sleep(30)    
            
        # wait additional 30s (up to 2m), if not yet running
        counter = 0
        while instance.state['Name'] != 'running' and counter < 3:
            print('Waiting additional 30s for instance')
            counter += 1
            time.sleep(30)
        
        # quit if instance is not running after 2m
        if instance.state['Name'] != 'running':
            raise Exception('Instance in state {} after 2m'.format(
                instance.state['Name']))
    
    # get ssh client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    privkey = paramiko.RSAKey.from_private_key_file(PEM_FILE)
    
    print('Connect SSH')
    ssh.connect(
        hostname=instance.public_dns_name,
        username=USER, 
        pkey=privkey
    )

    # call command
    print('Call /scripts/load_auctions')
    cmd = 'python3 /home/ec2-user/environment/wow-free-lunch/server/scripts/load_auctions.py'
    stdin, stdout, stderr = ssh.exec_command(cmd)
    print('Finished /scripts/load_auctions')
    
    stdin.flush()
    std_print('stdout', stdout)
    std_print('stderr', stderr)
    
    # close SSH
    ssh.close()
    
    # stop instance, if it was initially stopped
    if initial_state == 'stopped':
        print('Stopping instance')
        instance.stop()
        
    return {
        'message': 'Completed /scripts/load_auctions'
    }
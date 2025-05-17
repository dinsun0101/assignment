
import json
import boto3
import uuid
from datetime import datetime

ec2 = boto3.client('ec2')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('VPCMetadata')

def lambda_handler(event, context):
    try:
        vpc = ec2.create_vpc(CidrBlock='10.0.0.0/16')
        vpc_id = vpc['Vpc']['VpcId']
        ec2.modify_vpc_attribute(VpcId=vpc_id, EnableDnsSupport={'Value': True})
        ec2.modify_vpc_attribute(VpcId=vpc_id, EnableDnsHostnames={'Value': True})

        subnets = []
        azs = ec2.describe_availability_zones()['AvailabilityZones'][:2]

        for i, az in enumerate(azs):
            subnet = ec2.create_subnet(
                VpcId=vpc_id,
                CidrBlock=f'10.0.{i}.0/24',
                AvailabilityZone=az['ZoneName']
            )
            subnets.append(subnet['Subnet']['SubnetId'])

        record = {
            'id': str(uuid.uuid4()),
            'vpc_id': vpc_id,
            'subnets': subnets,
            'created_at': datetime.utcnow().isoformat()
        }
        table.put_item(Item=record)

        return {
            'statusCode': 201,
            'body': json.dumps(record)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

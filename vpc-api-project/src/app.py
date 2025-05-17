import boto3
import uuid
import json
import os

# AWS clients
dynamodb = boto3.resource("dynamodb")
ec2 = boto3.client("ec2")

# DynamoDB table name from environment variable
TABLE_NAME = os.environ.get("TABLE_NAME")

def create_vpc(event, context):
    """
    Create a VPC with subnets and store the details in DynamoDB.
    """
    try:
        body = json.loads(event.get("body", "{}"))
        vpc_cidr = body.get("VpcCidr", "10.0.0.0/16")
        subnets = body.get("Subnets", [])

        # Create a VPC
        vpc_response = ec2.create_vpc(CidrBlock=vpc_cidr)
        vpc = vpc_response["Vpc"]
        vpc_id = vpc["VpcId"]

        # Enable DNS features for the VPC
        ec2.modify_vpc_attribute(VpcId=vpc_id, EnableDnsSupport={"Value": True})
        ec2.modify_vpc_attribute(VpcId=vpc_id, EnableDnsHostnames={"Value": True})

        # Create Subnets
        subnet_ids = []
        for subnet in subnets:
            subnet_response = ec2.create_subnet(
                VpcId=vpc_id,
                CidrBlock=subnet["CidrBlock"],
                AvailabilityZone=subnet["AvailabilityZone"]
            )
            subnet_ids.append(subnet_response["Subnet"]["SubnetId"])

        # Save VPC and subnet details in DynamoDB
        table = dynamodb.Table(TABLE_NAME)
        record_id = str(uuid.uuid4())
        table.put_item(
            Item={
                "ResourceId": record_id,
                "VpcId": vpc_id,
                "VpcCidr": vpc_cidr,
                "Subnets": subnet_ids
            }
        )

        return {
            "statusCode": 201,
            "body": json.dumps({
                "ResourceId": record_id,
                "VpcId": vpc_id,
                "VpcCidr": vpc_cidr,
                "Subnets": subnet_ids
            })
        }

    except Exception as e:
        print(e)
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}

def get_resources(event, context):
    """
    Fetch all VPC and subnet details from DynamoDB.
    """
    try:
        table = dynamodb.Table(TABLE_NAME)
        results = table.scan()

        return {
            "statusCode": 200,
            "body": json.dumps(results["Items"])
        }

    except Exception as e:
        print(e)
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}

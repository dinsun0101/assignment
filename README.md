##Project Overview: 

This project provides serverless APIs to create AWS VPCs with subnets and retrieve their details.

## Features
- Create VPCs with subnets using a POST API.
- Retrieve details of created VPCs/subnets with a GET API.
- Cognito-authenticated API Gateway for secure access.

## Project folder structure
vpc-api-project
 - template.yaml         # AWS SAM template for infrastructure as code
 - src/                  # Python Lambda source code
    - app.py            # Lambda Handlers (create_vpc and get_resources)
    - requirements.txt  # Python dependencies


##Architecture
Creating an API that automates the creation of AWS VPCs with multiple subnets, securely stores results, and allows authenticated users to retrieve the resource data can be achieved using AWS serverless services such as AWS Lambda, Amazon API Gateway, Amazon DynamoDB, AWS IAM, and Amazon Cognito.

##Below is a high-level implementation and the Python code for this API:

##Components:
- API Gateway: Acts as the entry point for HTTP requests, handling authentication and routing to Lambda functions.
- AWS Lambda: Business logic to create VPCs, manage subnets, and store/retrieve data from DynamoDB.
- DynamoDB: Stores data about created VPCs and subnets.
= AWS Cognito: Manages authentication and secures the API.


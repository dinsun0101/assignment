## Project Overview: 

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


## Architecture
Creating an API that automates the creation of AWS VPCs with multiple subnets, securely stores results, and allows authenticated users to retrieve the resource data can be achieved using AWS serverless services such as AWS Lambda, Amazon API Gateway, Amazon DynamoDB, AWS IAM, and Amazon Cognito.


   <img width="379" alt="image" src="https://github.com/user-attachments/assets/0c6d0139-d067-4ddb-a207-f38995f3ab60" />


                


Below is a high-level implementation and the Python code for this API:

## Explanation
A client first log in via Cognito
After successful login, Cognito returns an id_token to the client;
The client sends a request to the API Gateway with the received id_token;
The API Gateway verifies in Cognito whether the id_token is valid;
Cognito will return to API Gateway a success response when the id_token is valid;
The API Gateway sends the request to the lambda function;
The lambda function executes and sends its response to the API Gateway;
The API Gateway sends the response to the client.


# Ferryman - AWS Resource Cleanup Lambda

## Overview
**Ferryman** is an AWS Lambda function designed to automatically delete AWS resources that have been tagged for cleanup. This helps manage cloud costs and prevents orphaned resources from lingering in your AWS environment. 

## Purpose
Cloud environments often accumulate unused or orphaned resources, leading to unnecessary costs and clutter. Ferryman provides an automated way to clean up these resources based on a specific tag, ensuring that only designated resources are removed while keeping everything else intact.

### Features
- Deletes AWS resources tagged with `shred=true`.
- Supports **EC2 Instances, EBS Volumes, S3 Buckets, Lambda Functions, and RDS Instances**.
- Logs execution details to **CloudWatch Logs**.
- Can be triggered manually or automatically via **AWS EventBridge (CloudWatch Schedule)**.

## Usage

### 1. Tag Resources for Cleanup
To mark resources for deletion, add the following tag:

```text
Key: shred
Value: true
```

### 2. Deploy the Lambda Function
You can deploy Ferryman using AWS CLI, Terraform, or manually in the AWS console.

#### Manual Deployment via AWS CLI
1. Zip the function code:
    ```bash
    zip -r ferryman.zip .
    ```
2. Deploy the function:
    ```bash
    aws lambda create-function --function-name Ferryman \
        --runtime python3.9 \
        --role arn:aws:iam::YOUR_ACCOUNT_ID:role/YOUR_LAMBDA_ROLE \
        --handler ferryman.lambda_handler \
        --zip-file fileb://ferryman.zip
    ```

### 3. Triggering Ferryman
#### Manual Execution
You can invoke Ferryman manually:
```bash
aws lambda invoke --function-name Ferryman output.json
```

#### Automated Execution via EventBridge
To schedule automatic cleanup (e.g., daily at midnight):
1. Go to **AWS EventBridge** → Create Rule
2. Set **Schedule Expression** to:
    ```
    cron(0 0 * * ? *)
    ```
3. Select **Ferryman Lambda Function** as the target

## IAM Permissions
Ferryman requires an IAM role with the following permissions:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:TerminateInstances",
                "ec2:DeleteVolume",
                "s3:ListBucket",
                "s3:GetBucketTagging",
                "s3:DeleteBucket",
                "lambda:ListFunctions",
                "lambda:DeleteFunction",
                "rds:DescribeDBInstances",
                "rds:DeleteDBInstance"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": "logs:CreateLogGroup",
            "Resource": "arn:aws:logs:*:*:*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:*:*:log-group:/aws/lambda/Ferryman:*"
        }
    ]
}
```

## Notes
- **Caution:** Ferryman permanently deletes resources. Use with care.
- Test in a **non-production** environment before enabling automatic cleanup.

## Future Enhancements
- Support for additional AWS resources (e.g., DynamoDB, Elastic Load Balancers)
- Dry-run mode for previewing deletions
- AWS CLI tool integration

## License
MIT License



#todo:
1 - Infrastructure
    1a - lambda ** Modulize lambda
    1b - IAM ** Modulize IAM
    1c - Cloudwatch ** Modulize Cloudwatch

2 - Correct actions
    2a - tag resources for destruction
    2b - schedule lambda for execution

3 - test

4 - clean up and accurize readme

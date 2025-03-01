import boto3

# Define the tag key and value to identify resources for deletion
TAG_KEY = "shred"
TAG_VALUE = "true"

def delete_ec2_instances():
    ec2 = boto3.client("ec2")
    instances = ec2.describe_instances(
        Filters=[{"Name": f"tag:{TAG_KEY}", "Values": [TAG_VALUE]}]
    )

    instance_ids = [
        i["InstanceId"]
        for r in instances["Reservations"]
        for i in r["Instances"]
        if i["State"]["Name"] != "terminated"
    ]

    if instance_ids:
        print(f"Terminating EC2 Instances: {instance_ids}")
        ec2.terminate_instances(InstanceIds=instance_ids)

def delete_ebs_volumes():
    ec2 = boto3.client("ec2")
    volumes = ec2.describe_volumes(
        Filters=[{"Name": f"tag:{TAG_KEY}", "Values": [TAG_VALUE]}]
    )

    volume_ids = [v["VolumeId"] for v in volumes["Volumes"]]
    
    if volume_ids:
        print(f"Deleting EBS Volumes: {volume_ids}")
        for vid in volume_ids:
            ec2.delete_volume(VolumeId=vid)

def delete_s3_buckets():
    s3 = boto3.client("s3")
    buckets = s3.list_buckets()["Buckets"]

    for bucket in buckets:
        tags = s3.get_bucket_tagging(Bucket=bucket["Name"])
        if any(tag["Key"] == TAG_KEY and tag["Value"] == TAG_VALUE for tag in tags["TagSet"]):
            print(f"Deleting S3 Bucket: {bucket['Name']}")
            s3.delete_bucket(Bucket=bucket["Name"])

def delete_lambda_functions():
    lambda_client = boto3.client("lambda")
    functions = lambda_client.list_functions()["Functions"]

    for function in functions:
        tags = lambda_client.list_tags(Resource=function["FunctionArn"])
        if tags.get("Tags", {}).get(TAG_KEY) == TAG_VALUE:
            print(f"Deleting Lambda Function: {function['FunctionName']}")
            lambda_client.delete_function(FunctionName=function["FunctionName"])

def delete_rds_instances():
    rds = boto3.client("rds")
    instances = rds.describe_db_instances()["DBInstances"]

    for instance in instances:
        tags = rds.list_tags_for_resource(ResourceName=instance["DBInstanceArn"])["TagList"]
        if any(tag["Key"] == TAG_KEY and tag["Value"] == TAG_VALUE for tag in tags):
            print(f"Deleting RDS Instance: {instance['DBInstanceIdentifier']}")
            rds.delete_db_instance(DBInstanceIdentifier=instance["DBInstanceIdentifier"], SkipFinalSnapshot=True)

if __name__ == "__main__":
    print("Running AWS Shredder...")

    delete_ec2_instances()
    delete_ebs_volumes()
    delete_s3_buckets()
    delete_lambda_functions()
    delete_rds_instances()

    print("Shredder execution complete!")

#todo: get rid of name main and move to lambda_handler

import boto3
import argparse
import logging


def setup_logger():
    logging.getLogger('boto3').setLevel(logging.CRITICAL)
    logging.getLogger('botocore').setLevel(logging.CRITICAL)
    logger = logging.getLogger(__name__)

    logging.basicConfig(level=logging.INFO,
                        format='[%(asctime)s] %(name)-10s %(levelname)-8s %(message)s'
                        )
    return logger

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-tk', help='Tag Key by which the resources must be filtered')
    parser.add_argument('-tv', help='Tag Value by which the resources must be filtered')
    parser.add_argument('-r', help='Region of the AWS resource')
    args = parser.parse_args()

    if not (args.tk and args.tv):
        parser.error('-tk and -tv argument must be provided in order to run the script')
    return args

def main():
    logger = setup_logger()
    args = parse_args()

    FILTER_TAG_KEY = args.tk
    FILTER_TAG_VALUE = args.tv
    REGION = args.r if args.r else 'us-east-1'

    session = boto3.Session()
    asg_client = session.client('autoscaling', region_name=REGION)
    ec2_client = session.client('ec2', region_name=REGION)

    paginator = asg_client.get_paginator('describe_auto_scaling_groups')
    page_iterator = paginator.paginate()

    filtered_asgs = page_iterator.search(
        'AutoScalingGroups[] | [?contains(Tags[?Key==`{}`].Value, `{}`)]'.format(
            FILTER_TAG_KEY, FILTER_TAG_VALUE)
    )

    isGeneratorEmpty = True
    #iterate over all filtered ASGs
    for asg in filtered_asgs:
        isGeneratorEmpty = False
        instance_ids = []
        asg_tags = {}
        #get tags and instances associated with this ASG
        logger.info('Processing ASG: '+asg.get('AutoScalingGroupName'))
        asg_tags_detail = asg.get('Tags')
        for tag in asg_tags_detail:
            asg_tags[tag.get('Key')] = tag.get('Value')
        for instance in asg['Instances']:
            instance_ids.append(instance['InstanceId'])

        #get tags for instances attached to the ASG and remove any tags that are not there in ASG
        ec2_response = ec2_client.describe_instances(InstanceIds = instance_ids)
        for instances in ec2_response['Reservations']:
            for instance in instances.get('Instances'):
                instance_tags = {}
                instance_id = instance.get('InstanceId')
                logger.info('Processing instance: '+instance_id)
                instance_tags_detail = instance.get('Tags')
                for tag in instance_tags_detail:
                    instance_tags[tag.get('Key')] = (tag.get('Value'))
                non_required_tags = []
                required_tags = []
                for tag_key in instance_tags:
                    if tag_key not in asg_tags and tag_key != 'aws:autoscaling:groupName':
                        non_required_tags.append({'Key': tag_key})
                for tag_key, tag_value in asg_tags.items():
                    if tag_key not in instance_tags:
                        required_tags.append({'Key': tag_key, 'Value': tag_value})
                if non_required_tags:
                    logger.info('Deleting tags {}'.format(non_required_tags))
                    ec2_client.delete_tags(Resources=[instance_id], Tags=non_required_tags)
                if required_tags:
                    logger.info('Adding tags {}'.format(required_tags))
                    ec2_client.create_tags(Resources=[instance_id], Tags=required_tags)

    if isGeneratorEmpty:
        logger.info('Did not find any ASGs with tag key: {} and value: {}'.format(FILTER_TAG_KEY, FILTER_TAG_VALUE))
        return

    logger.info('Tag syncing complete')


if __name__ == "__main__":
    main()

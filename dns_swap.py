#!/usr/bin/python3.6

import json, argparse, boto3, botocore, os

def s3_get_file(uuid, s3, bucket):
    try:
        s3.Object(bucket_name=bucket, key='base/config/{0}.json'.format(uuid)).download_file('{0}/{1}.json'.format(os.getcwd(), uuid))
        print('{0}.json found in {1} bucket and downloaded'.format(uuid, bucket))
        return True
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print('NOTICE: file {0}.json not found in {1} bucket'.format(uuid, bucket))
        return False

def s3_put_file(uuid, s3, bucket):
    try:
        s3.Object(bucket_name=bucket, key='base/config/{0}.json'.format(uuid)).upload_file('{0}/{1}.json'.format(os.getcwd(), uuid))
        print('\"' + uuid + '.json\" uploaded to ' + b + ' bucket.')
        return True
    except botocore.exceptions.ClientError as e:
        print(e)
    return False

def swap_zone(source, destination, zone):
    source_state_file='{0}/{1}.json'.format(os.getcwd(), source)
    dest_state_file='{0}/{1}.json'.format(os.getcwd(), destination)

    try:
        with open(source_state_file, "r") as f:
            source_state_json = json.loads(f.read())

        with open(dest_state_file, "r") as f:
            dest_state_json = json.loads(f.read())

        zone_dict={}

        for i in source_state_json['dns']:
            if i['origin'] == zone:
                print('Found DNS zone named {0}'.format(zone))
                zone_dict = i
    
        if zone_dict == {}:
            print('ERROR: No {0} DNS zone found in the source file, exiting'.format(zone))
            return False
    
        source_state_json['dns'].remove(zone_dict)
    
        with open(source_state_file, "w") as f:
            f.write(json.dumps(source_state_json))

        dest_state_json['dns'].append(zone_dict)

        with open(dest_state_file, "w") as f:
            f.write(json.dumps(dest_state_json))

        print('Moved {0} DNS zone from {1} to {2}'.format(zone, source, destination))
        return True
    except:        
        print('ERROR: some of the files not found, exiting.')
        return False

#remove files after execution

def cleanup(source, destination):
    source_file=source + '.json'
    destination_file = destination + '.json'

    if os.path.isfile(source_file):
        os.remove(source_file)
        print('{0} file removed'.format(source_file))

    if os.path.isfile(destination + '.json'):
        os.remove(destination_file)
        print('{0} file removed'.format(destination_file))

parser = argparse.ArgumentParser(description='Swap DNS zones between Stratus instances')
parser.add_argument('-s', '--source', help='UUID you want to migrate DNS zone from', required=True)
parser.add_argument('-d', '--destination', help='UUID you want to migrate DNS zone to', required=True)
parser.add_argument('-z', '--zone', help='DNS zone you want to migrate', required=True)

args = parser.parse_args()

if (len(args.source) or len(args.destination)) != 16:
    print('UUIDs lenght is wrong, exiting')   
    exit(1)

if args.source == args.destination:
    print('UUIDs are identical, exiting')
    exit(1)

print('Starting DNS zone copy. Fetching files from S3...')

s3 = boto3.resource('s3')

bucket_list=['stratus-pillar-us-east-1', 'stratus-pillar-ap-southeast-2', 'stratus2111-pillar-eu-central-1']

# iterate through buckets; swap zones only if both config files found in the same bucket (= same region), else exit

for b in bucket_list:
    if s3_get_file(args.source, s3, b):
        if s3_get_file(args.destination, s3, b):                                           
            if swap_zone(args.source, args.destination, args.zone):

                #put files back after zone is moved

                if s3_put_file(args.source, s3, b) and s3_put_file(args.destination, s3, b):
                    print('Zone swap finished successfully. Please recheck panel/resolving.')
                    cleanup(args.source, args.destination)
                    exit(0)
            else:
                break
        else:
            print('ERROR: either {0} UUID does not exist, or source and destination instances are in different regions, exiting'.format(args.destination))
            break
    else:
        continue
exit(1)

import boto3
import time
from datetime import datetime
import csv

route53 = boto3.client('route53')
s3 = boto3.client('s3')

s3_bucket_name = "osher-buck"
s3_bucket_region = "us-east-2"

def get_hosted_zones():
    response = route53.list_hosted_zones_by_name()
    hosted_zones = response['HostedZones']
    return hosted_zones

def get_records(zone_id):
    response = route53.list_resource_record_sets (HostedZoneId=zone_id)
    zone_records= response['ResourceRecordSets']
    return zone_records

def upload_to_s3(folder, filename, bucket_name, key):
    key = folder + '/' + key
    response = s3.upload_file(filename, bucket_name, key)
    return response


def write_to_csv(zone, zone_records):
    zone_file_name = '/tmp/' + zone['Name'] + 'csv'
    with open(zone_file_name, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([ 'NAME', 'TYPE' ])

        for record in zone_records:
            csv_row = [''] * 2
            csv_row[0] = record['Name']
            print(record['Name'])
            csv_row[1] = record['Type']
            print(record['Type'])
            writer.writerow(csv_row)
           
    return zone_file_name
  

#def lambda_handler(event, context):
time_stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ",
    datetime.utcnow().utctimetuple()
)
hosted_zones = get_hosted_zones()
for zone in hosted_zones:
    zone_folder = (time_stamp + 'route53-hostesd-zones')
    zone_records = get_records(zone['Id'])
    text_file = write_to_csv(zone, zone_records)
    upload_to_s3(
        zone_folder,
        write_to_csv(zone, zone_records),
        s3_bucket_name,
        (zone['Name'] + 'csv')
    )
        

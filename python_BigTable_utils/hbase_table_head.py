#!/usr/bin/env python
#
# Code is small modification of this example:
#  https://github.com/GoogleCloudPlatform/python-docs-samples/tree/master/bigtable/hello_happybase
#    
# Demonstrates how to connect to Cloud Bigtable
# Create table
# insert list of words to the table
# Prerequisites:
#- Create a Cloud Bigtable cluster.
#  https://cloud.google.com/bigtable/docs/creating-cluster
#- Set your Google Application Default Credentials.
#  https://developers.google.com/identity/protocols/application-default-credentials
#
# usage: words_from_BigTable_tables_to_output.py [-h] [--table TABLE] project_id instance_id

import argparse

from google.cloud import bigtable
from google.cloud import happybase


def main(project_id, instance_id, table_name):
    # [START connecting_to_bigtable]
    # The client must be created with admin=True because it will create a
    # table.
    client = bigtable.Client(project=project_id, admin=True)
    instance = client.instance(instance_id)
    connection = happybase.Connection(instance=instance)
    # [END connecting_to_bigtable]

    try:
        # [START creating_a_table]
        tablese = connection.tables()
        print('existing tables: ', tablese)
        column_family_name = 'cf'
        
        table = connection.table(table_name)

        # [START scanning_all_rows]
        print('Scanning all words in table: ', table_name)

        
        column_name = '{fam}:count'.format(fam=column_family_name)
        print('column_name ', column_name)
		
        i = 0
        for key, row in table.scan(limit=40):
            #
            # Do your staff here with the words in the table...
            # For simplycity, we just print them to stdout
            #if (i>=5): 
            #     break
            i += 1
            #print('\t{}: {}'.format(key, row[column_name.encode('utf-8')]))
            #print(i, key, row)
            #print(i, row[b'cf:count']) 
            #print('\t{}: {}'.format(key, row[column_name.encode('utf-8')]))
    
            #print('little', 'word: ', key, 'orig: ', row[b'cf:count'], ' encoded: ', int.from_bytes(row[b'cf:count'], byteorder='little'))    
            print(i, ' word: ', key.decode("utf-8"),  'count: ', int.from_bytes(row[b'cf:count'], byteorder='big'))
            
        # [END scanning_all_rows]

        # [START deleting_a_table]
        #print('Deleting the {} table.'.format(table_name))
        #connection.delete_table(table_name)
        # [END deleting_a_table]

    finally:
        connection.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('project_id', help='Your Cloud Platform project ID.')
    parser.add_argument(
        'instance_id', help='ID of the Cloud Bigtable instance to connect to.')
    parser.add_argument(
        '--table',
        help='Table to list all words and destroy.',
        default='words_table_example')

    args = parser.parse_args()
    main(args.project_id, args.instance_id, args.table)
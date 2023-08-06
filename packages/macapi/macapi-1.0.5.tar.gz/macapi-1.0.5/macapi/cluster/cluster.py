#!/usr/bin/env python

import os, argparse, json, logging, time, sys

from macapi.api_base import ApiBase
from pprint import pprint
from collections import OrderedDict
from requests.auth import HTTPDigestAuth
from requests import Session

class Cluster(ApiBase):
    """creates and gets cluster configruation"""
    def __init__(self, group_id, api_user, api_key):
        super(Cluster, self).__init__(group_id, api_user, api_key)

    def get_cluster(self, group_id, *argv):
        base_url = self.base_url
        url = "{}/groups/{}/clusters/{}".format(base_url, group_id, *argv)
        data = {}
        data = self.get(url)
        keys = ['links', 'groupId', 'id',
                'mongoURI', 'mongoURIUpdated',
                'mongoURIWithOptions', 'stateName'
                ]
        details = {k:v for (k, v) in data.items() if k not in keys}
        results = {}

        try:
            # remove duplicate keys if any
            for key,value in details.items():
                if 'replicationSpecs' not in results.keys():
                    results[key] = value

                json_file = json.dumps(results, indent=1)

            return json_file

        except Exception as e:
            print('error found: ' + e)

    # creates an m10 replicaSet
    def create_cluster_3(self, group_id, name, size, nodes):
        s = Session()
        base_url = self.base_url
        # use join to make directory platform independent
        file_dir = os.path.dirname(os.path.relpath('__file__'))
        base_config_3 = os.path.join(file_dir, 'configs/json_files/base_config_3.json')
        url = "{}/groups/{}/clusters".format(base_url, group_id)
        auth = HTTPDigestAuth(self.api_user, self.api_key)
        headers = {'content-type': 'application/json'}
        logging.info("Executing POST: {}".format(url))

        with open(base_config_3) as f:
            json_file = json.load(f)
            for key in json_file.keys():
                if key == 'name':
                    json_file['name'] = name

                if key == 'providerSettings':
                    json_file['providerSettings']['instanceSizeName'] = size

                    #yield True
                #r = s.post(json_file)
            try:
                print(json_file)
                self.post(url, json_file)

            except:
                pass

    def create_cluster_5(self, group_id, name, size, nodes):
        s = Session()
        base_url = self.base_url
        file_dir = os.path.dirname(os.path.relpath('__file__'))
        base_config_5 = os.path.join(file_dir, 'configs/json_files/base_config_5.json')
        url = "{}/groups/{}/clusters".format(base_url, group_id)
        auth = HTTPDigestAuth(self.api_user, self.api_key)
        headers = {'content-type': 'application/json'}
        logging.info("Executing POST: {}".format(url))

        with open(create_cluster_5) as f:
            json_file = json.load(f)
            for key in json_file.keys():
                if key == 'name':
                    json_file['name'] = name

                if key == 'providerSettings':
                    json_file['providerSettings']['instanceSizeName'] = size

                    #yield True
                #r = s.post(json_file)
            try:

                print(json_file)
                self.post(url, json_file)

                        #yield false
            except:
                pass


    def resize(self, group_id, name, size):
        base_url = self.base_url
        url = "{}/groups/{}/clusters/{}".format(base_url, group_id, name)
        data = {'providerSettings.instanceSizeName' : size}
        try:
            result = self.patch(url, data)
            return result

        except:
            pass


    def delete_cluster(self, group_id, name):
        base_url = self.base_url
        url = '{}/groups/{}/clusters/{}'.format(base_url, group_id, name)
        s = Session()
        headers = {'content-type': 'application/json'}
        auth=HTTPDigestAuth(self.api_user, self.api_key)
        try:
            result = s.delete(url, auth=auth, headers=headers)
            return result
        except Exception as e:
            print('\033[1;41m{}\033[1;m'.format(e))




# Initialize the command line options parser
parser = argparse.ArgumentParser()
parser.add_argument('-G', '--get', action='store_true', help="get's the currnet group cluster configuration")
parser.add_argument('-C', '--create', action='store_true', help='creates a new cluster')
parser.add_argument('-f', '--file', help='write file to current directy or path')
parser.add_argument('-n', '--name', required=True, help='the name of the cluster')
parser.add_argument('-g', '--group_id', required=True, help='id of the group that you are trying to make the changes for')
parser.add_argument('-u', '--api_user', required=True, help='the email address you use to login')
parser.add_argument('-k', '--api_key', required=True, help='Your Atlas api key')
parser.add_argument('-D', '--delete', action='store_true', help='deletes a cluster from a project')
parser.add_argument('--resize', action='store_true', help='resizes an instace')
parser.add_argument('--size', default='M10', type=str, help="size of an instance in ['M10',...,'M60']")
parser.add_argument('--nodes', default=3, type=int, help='number of nodes per shard or replicaSet')
parser.add_argument('--shards', default=1, type=int, help='number of replicaSets to deploy')
args = parser.parse_args()
run = Cluster(args.group_id, args.api_user, args.api_key)

if args.get:
    if args.file:
        # makes directory platform independent
        directory = os.path.relpath(args.file)
        with open(directory, 'w') as f:
            sys.stdout = f
            get = run.get_cluster(args.group_id, args.name)
            # printing get so that it gets redirected into standard out which is the object f
            print(get)

    else:
        get = run.get_cluster(args.group_id, args.name)
        print(get)
elif args.create:
        #if args.size:
        instance_size = ['M10', 'M20', 'M30', 'M40', 'M50', 'M60']
        if args.size not in instance_size:
            print('\033[1;33m--size must be one of the following: M10, M20, M30, M40, M50 or M60\033[1;m')
        #if args.size.upper().startswith('m'):

        if args.nodes == 3:
            print('****3 nodes***')
            print('\033[1;33mcreating a cluster with Name: {}, instance type: {} and number of nodes: {}\033[1;m'.format(args.name, args.size, args.nodes))
            answer = raw_input('type y/n: ')
            if answer.lower().startswith('y'):
                create = run.create_cluster_3(args.group_id, args.name, args.size, args.nodes)
                # print the return object so we get some verbosity
                print(create)
            elif answer.lower().startswith('n'):
                print('aborting...')
                sys.exit(0) # exit cleanly
        elif args.nodes == 5:
            print('***5nodes***')
            print('\033[1;33mcreating a cluster with Name: {}, instance type: {} and number of nodes: {}\033[1;m'.format(args.name, args.size, args.nodes))
            answer = raw_input('type y/n: ')
            if answer.lower().startswith('y'):
                create = run.create_cluster_5(args.group_id, args.name, args.size, args.nodes)
                print(create)
            elif answer.lower().startswith('n'):
                print('aborting...')
                sys.exit(0) # exit cleanly

        else:
            print('\033[1;33mcreating a cluster with Name: {}, instance type: {} and number of nodes: {}\033[1;m]'.format(args.name, args.size, args.nodes))
            create = run.create_cluster_3(args.group_id, args.name, args.size, args.nodes)
            sys.exit(0)

elif args.resize:
    print('\033[1;33mchoices are M10, M20, M30, M40, M50 and M60\033[1;m]')
    size_name = raw_input('enter the instance size to resize to : ')
    # check that the size_name variable is not empty and that it start with M
    if size_name.upper().startswith('m'):
        print('you are about to rezie cluster name: {} to {}!'.format(args.name, size_name))
        answer = raw_input('type y/n: ')
        if answer.lower().startswith('y'):
            create = run.resize(args.group_id, args.name, size_name)
            print(create)
        elif answer.lower().startswith('n'):
            print('aborting...')
            sys.exit(0) # exit cleanly
    else:
        sys.exit(0) # exit cleanly


elif args.delete:
    print('\033[1;33myou are about to delete cluster name: {}\033[1;m'.format(args.name))
    answer = raw_input('are you sure you want to proceed?: ')

    while answer:

        if answer.lower().startswith('y'):
            delete = run.delete_cluster(args.group_id, args.name)
            print('\033[1;32mdeleted {}, {}\033[1;m'.format(args.name, delete))
            break
        elif answer.lower().startswith('n'):
            print('aborting...')
            break
        else:
            print('\033[1;33myou must enter either y/n\033[1;m')
            # restore the value for answer so that it can be re-evaluated
            answer = raw_input('are you sure you want to proceed?: ')
            continue
    sys.exit(0)

else:
    print('you did not enter an option...')

def main():
    run


if __name__ == '__main__':
    sys.exit(main())

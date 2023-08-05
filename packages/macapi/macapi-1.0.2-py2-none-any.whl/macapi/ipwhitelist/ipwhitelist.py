#!/usr/bin/env python

import os, argparse, json, logging, time, sys

from macapi.api_base import ApiBase
from pprint import pprint
from collections import OrderedDict


class Whitelist(ApiBase):
    def __init__(self, group_id, api_user, api_key):
        super(Whitelist, self).__init__(group_id, api_user, api_key)

    def get_whitelist(self, group_id):
        base_url = self.base_url
        url = "{}/groups/{}/whitelist".format(base_url, group_id)
        data = self.get(url)
        data1 = data['results']
        keys = ["cidrBlock", "comment"]
        details = [{k:v for k, v in i.items() if k in keys} for i in data1]
        pprint(details)

    def post_whitelist(self, group_id):
        base_url = self.base_url
        url = "{}/groups/{}/whitelist".format(base_url, group_id)
        ipAddress = raw_input('enter an IP address or cider block: ')
        comment = raw_input('enter a comment for the ip address you entered above: ')
        data = []
        data.append({"ipAddress": ipAddress,
                "comment": comment
                })
        print(data)
        json_file = json.dumps(data)
        self.post(url, json_file)



parser = argparse.ArgumentParser()
parser.add_argument('-G', '--get', action='store_true', help="get's the currnet group IP Whitelist")
parser.add_argument('-C', '--create', action='store_true', help='replace current alerts confifuration')
parser.add_argument('-D', '--delete', action='store_true', help='delte a single alert')
parser.add_argument('-f', '--file', help='write file to current directory unless absolute path is provided')
parser.add_argument('-g', '--group_id', required=True, help='id of the group that you are trying to make the changes for')
parser.add_argument('-u', '--api_user', required=True, help='the email address you use to login')
parser.add_argument('-k', '--api_key', required=True, help='Your Atlas api key')
args = parser.parse_args()
run = Whitelist(args.group_id, args.api_user, args.api_key)

if args.get:
    if args.file:
        directory = os.path.relpath(args.file)
        with open(directory, 'w+') as f:
            sys.stdout = f
            run.get_whitelist(args.group_id)
    else:
        run.get_whitelist(args.group_id)

elif args.create:
    run.post_whitelist(args.group_id)

else:
    print('you did not enter an option...')

def main():
    run


if __name__ == '__main__':
    sys.exit(main())

#!/usr/bin/env python

import os, argparse, json, logging, time, sys

from macapi.api_base import ApiBase
from pprint import pprint
from requests import post, Session
from requests.auth import HTTPDigestAuth

class OpsmanagerApi(ApiBase):
    def __init__(self, group_id, api_user, api_key):
        super(OpsmanagerApi, self).__init__(group_id, api_user, api_key)

    def get_alerts(self, group_id):
        base_url = self.base_url
        url = "{}/groups/{}/alertConfigs".format(base_url, group_id)
        print(url)
        data = self.get(url)
        print(data)
        data1 = data['results']
        print(data1)
        keys = ["groupId", "eventTypeName", "enabled", "metricThreshold", "notifications"]
        alerts = [{k:v for k, v in i.items() if k in keys} for i in data1]
        isconfig_dir = os.path.isdir('configs')
        if isconfig_dir == False:
            os.mkdir('configs')

        json_file = os.path.join("configs", 'alert_file.json')
        logging.info("Getting alert configuration from: {}" + "for goupId: {}".format(url, group_id))

        with open(json_file, 'w') as f:
            json.dump(alerts, f, indent=4)
            logging.debug("{}".format(pprint(alerts)))

    def create_alerts(self, group_id):
        s = Session()
        base_url = self.base_url
        url = "{}/groups/{}/alertConfigs".format(base_url, group_id)
        auth = HTTPDigestAuth(self.api_user, self.api_key)
        headers = {'content-type': 'application/json'}
        logging.info("Executing POST: {}".format(url))
        with open('configs/alert_file.json') as json_file:
            data = json.load(json_file)
            keys = ["groupId", "eventTypeName", "enabled", "metricThreshold", "notifications"]
            #key2 = ["groupId", "eventTypeName", "enabled", "notifications"]
            #keys = [key1, key2]
            alerts = [{k:v for k, v in i.items() if k in keys} for i in data]
            #print(alerts)
            for line in alerts:
                try:

                    r = s.post(url,
                        auth=auth,
                        data=json.dumps(line),
                        headers=headers
                        )
                    print(r)
                except:
                    self.check_response(r)

    def update_alerts(self, group_id):
        base_url = self.base_url
        url = "{}/groups/{}/alertConfigs".format(base_url, group_id)
        with open('configs/alert_file.json') as f:
            r = self.put(url)

    def delete_alerts(self, group_id):
        s = Session()
        base_url = self.base_url
        url = "{}/groups/{}/alertConfigs/".format(base_url, group_id)
        auth = HTTPDigestAuth(self.api_user, self.api_key)
        headers = {'content-type': 'application/json'}
        data = self.get(url)
        data1 = data['results']
        key = ['id']
        alerts = [{k:v for k, v in i.items() if k in key} for i in data1]
        print('**********************************************')
        print('There are {} alerts'.format(len(alerts)))
        print('**********************************************')

        for i in alerts:
            for k, v in i.iteritems():
                print('Deleting alert id: {}'.format(v))
                r = s.delete(url + v,
                    auth=auth,
                    data=json.dumps(v),
                    headers=headers
                    )

                self.check_response(r)

        print('**********************************************')
        print('{} alerts were deleted'.format(len(alerts)))
        print('**********************************************')

parser = argparse.ArgumentParser()
parser.add_argument('-G', '--get', action='store_true', help='get a group alert and monitoring configuration')
parser.add_argument('-U', '--update', action='store_true', help='update current alerts configuration')
parser.add_argument('-C', '--create', action='store_true', help='replace current alerts confifuration')
parser.add_argument('-D', '--delete', action='store_true', help='delte a single alert')
parser.add_argument('-f', '--file', help='write file to current directory unless absolute path is provided')
parser.add_argument('-g', '--group_id', required=True)
parser.add_argument('-u', '--api_user', required=True)
parser.add_argument('-k', '--api_key', required=True)
args = parser.parse_args()
run = OpsmanagerApi(args.group_id, args.api_user, args.api_key)

if args.get:
    if args.file:
        directory = os.path.relpath(args.file)
        with open(directory, 'w+') as f:
            sys.stdout = f
            print(f)
            run.get_alerts(args.group_id)
    else:
        run.get_alerts(args.group_id)
elif args.update:
    if args.file:
        directory = os.path.relpath(args.file)
        with open(directory, 'w+') as f:
            sys.stdout = f
            run.update_alerts(args.base_url, args.group_id)
    else:
        run.update_alerts(args.base_url, args.group_id)
elif args.create:
    if args.file:
        directory = os.path.relpath(args.file)
        with open(directory, 'w+') as f:
            sys.stdout = f
            run.create_alerts(args.base_url, args.group_id)
    else:
        run.create_alerts(args.group_id)
elif args.delete:
    print('This will delete all alerts for the group id: {}'.format(args.group_id))
    print('**********************************************')
    answer = raw_input('Are you sure you want to continue?: ')
    print('**********************************************')
    if answer.lower().startswith('y'):
        if args.file:
            directory = os.path.relpath(args.file)
            with open(directory, 'w+') as f:
                sys.stdout = f
                run.delete_alerts(args.group_id)
        else:
            run.delete_alerts(args.group_id)
    elif answer.lower().startswith('n'):
        print('action aborted!!')
        exit()
    else:
        print('Must type yes or no')

else:
    print('you did not enter an option...')


def main():
    run = OpsmanagerApi(args.group_id, args.api_user, args.api_key)
    return 0


if __name__ == '__main__':
    sys.exit(main())

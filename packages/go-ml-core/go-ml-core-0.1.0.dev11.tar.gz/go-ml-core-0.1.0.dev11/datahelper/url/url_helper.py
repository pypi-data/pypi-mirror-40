import requests
import json
import configparser

from bs4 import BeautifulSoup

class URLHelper():
    def __init__(
        self,
        logger=None,
        config_file='go_servers.ini',
        host_name='DataPlatform_DEV_API'):
        self.logger = logger
        self.config_file = config_file
        self.host_name = host_name

    def get_cipher(self):
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file)

        refresh_url = self.config[self.host_name]['refresh_url']
        r = requests.get(refresh_url)
        lines = str(r.content).split('\\n')
        lines = [x.strip().replace('<td>','').replace('</td>','') for x in lines]
        ind = lines.index(self.config[self.host_name]['account'])
        return lines[ind+1]

    
    def get_cipher_tmp(self):
        self.host_name = 'DataPlatform_DEV_API_TMP'
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file)

        params = self.config[self.host_name]
        url = '%s?env=%s&app=%s&resource=%s&username=%s&password=%s' % (params['base_url'],
                                                                        params['env'],
                                                                        params['app'],
                                                                        params['resource'],
                                                                        params['account'],
                                                                        params['password'])
        response = requests.get(url).text
        print(response)
        bs = BeautifulSoup(response, 'html.parser')
        results = []
        for tr in bs.find_all('tr'):
            tds = tr.find_all('td')
            if len(tds)==2 and tds[0].string==params['account']:
                return tds[1].string
        return None


    def post_json(self, url, json_obj, json_option=None):
        #self.cipher = self.get_cipher()
        # headers = {
        #         'Go-Client':'stage',
        #         'Authorization':'Bearer {}'.format(self.cipher),
        # }
        self.cipher = self.get_cipher_tmp()
        headers = {
                'Go-Client':'dev',
                'Authorization':'Bearer {}'.format(self.cipher),
        }
        r = requests.post(url, headers=headers, json=json_obj)
        if json_option is None:
            json_option = {}
        return json.loads(r.content.decode('utf-8'),**json_option)

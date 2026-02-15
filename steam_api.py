import requests
import json
import os
import random
from dotenv import load_dotenv
import time
import pandas as pd
import logging

class steam_api:
    logger = logging.getLogger(__name__)
    level = {0: logging.DEBUG, 1:logging.INFO, 2:logging.WARNING, 3:logging.ERROR}
    def __init__(self,API_KEY=None, USER_ID=None, level=1):

        logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', level=self.level[level])

        if API_KEY is None or USER_ID is None:
            faltante = ", ".join(x[0] is x[1] is None for x in {"API_KEY":API_KEY, 'USER_ID':USER_ID}.items())
            raise Exception('No se encontró {faltante}')
                            
        self.steam_url =  'http://api.steampowered.com'
        self.API_KEY = API_KEY
        self.USER_ID = USER_ID

    def get_news_for_app(self,app_id=None,count=3,max_lenght=300,formato='json',force_to_wait=False):
        if app_id is None:
            is_random = True
            app_id = random.randint(1, 10000)
        else:
            is_random = False


        url_appid_news = self.steam_url + \
                        f'/ISteamNews/GetNewsForApp/v0002/'
        
        parameters = {'appid': app_id,
                        'count':count,
                        'maxlength': max_lenght,
                        'format':formato}
        news_appid = self.retrieve_api(url=url_appid_news,parameters=parameters, force_to_wait=force_to_wait)
        return news_appid

    def retrieve_api(self,url=None,parameters=None, force_to_wait=False):
        if url is None:
            url = self.steam_url 
        
        url += f'?key={self.API_KEY}'

        if isinstance(parameters,dict):
            url += '&' + '&'.join(str(x[0])+"="+str(x[1]) for x in parameters.items())

        try:
            response = requests.get(url=url)
        except SSLError as s:
            print('SSL Error:', s)
        
            for i in range(5, 0, -1):
                print('\rWaiting... ({})'.format(i), end='')
                time.sleep(1)
            print('\rRetrying.' + ' '*10)
            
            # recusively try again
            return self.retrieve_api(url, parameters)
    
        if response and response.status_code == 200:
            return response.json()
       
       
        elif response.status_code == 429 and not force_to_wait:
            self.logger.warning(f'Response:{response.status_code} - Too many requests. Sleep for 10 sec. Maybe wait 5 min')
            self.logger.warning(f'url: {url}')
            time.sleep(10)


        elif response.status_code == 403:
            self.logger.warning(f'Response:{response.status_code} - Forbidden to access. Sleep for 5 min.')
            self.logger.warning(f'url: {url}')
            time.sleep(5 * 60)

        else:
            self.logger.error(f"ERROR: status code: {response.status_code}")
            self.logger.warning(f'url: {url}')
        return None
    
    def get_all_app_id(self):
            # get all app id
        url = "https://api.steampowered.com/IStoreService/GetAppList/v1/"
        all_ids = self.retrieve_api(url=url, parameters={'last_appid': 0, 'max_results':50000})
        self.all_games = pd.DataFrame(all_ids['response']['apps'])
        self.all_games['last_modified'] = self.all_games['last_modified'].dt.datetime.fromtimestamp
        return self.all_games
       
                            
                            
                            
                            
                            
                            
                            
                            
                            

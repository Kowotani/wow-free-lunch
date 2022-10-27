import datetime as dt
import json
import requests
from requests.auth import HTTPBasicAuth




'''
This class handles interfacing with the Battle.net API for retrieval of
game data
'''

class BNetAPIUtil:

    '''
    Battle.net API access keys
    '''
    __CLIENT_ID__ = '4e41cbadc23f466ea64c61e382c08bd1'
    __CLIENT_SECRET__ = '1f768iHJc3bPjS6D8j4zXO1nLvYFXE5l'
    
    
    '''
    Access token metadata
    '''
    __access_token__ = None
    access_token_expiration = None


    '''
    Other API Inputs
    '''
    # TODO: consider non-static namespaces (eg. dynamic, profile)
    # Only use US region
    namespaces = {
        'classic': 'static-classic-us',
        'retail': 'static-us'
    }
    # Only use en_US
    locale = 'en_US'

    '''
    DESC
        Class constructor
        
    INPUT
    
    RETURN
        Empty state object
    '''
    def __init__(self):
        self.__access_token__ = None
    
    '''
    ==============
    Auth Functions
    ==============
    
    These functions handle auth and access token managment
    '''
    
    '''
    DESC
        Creates an HTTPBasicAuth object with Battle.net API access keys
        
    INPUT
        
    RETURN
        HTTPBasicAuth object       
    '''
    def __get_auth_object(self) -> HTTPBasicAuth:
        return HTTPBasicAuth(self.__CLIENT_ID__, self.__CLIENT_SECRET__)

    '''
    DESC
        Determines if the access token is still valid
    
    INPUT
    
    RETURN
        TRUE if the access token is still valid, FALSE otherwise
    '''
    def has_valid_access_token(self) -> bool:
        return self.__access_token__ is not None and \
            dt.datetime.now() < self.access_token_expiration


    '''
    DESC
        Update the new access token from Battle.net service for API use if
        necessary (ie. existing token is None or is expired). This should only 
        be called after checking the validity of any existing token
    
    INPUT
    
    RETURN
    '''
    def get_access_token(self) -> None:
        # prepare POST metadata
        url = 'https://oauth.battle.net/token'
        auth = self.__get_auth_object()
        data = {'grant_type' : 'client_credentials'}
        
        # POST request
        r = requests.post(url, auth=auth, data=data)
        if r.status_code == 200:
            r_body = r.json()
            self.__access_token__ = r_body['access_token']
            self.access_token_expiration = dt.datetime.now() + \
                dt.timedelta(seconds=r_body['expires_in'])
        else:
            r.raise_for_status()


    '''
    =============
    API Functions
    =============
    
    These functions map 1:1 with Battle.net API functions defined in
    https://develop.battle.net/documentation/world-of-warcraft and
    https://develop.battle.net/documentation/world-of-warcraft-classic
    '''
    
    '''
    -----------
    WoW Classic
    -----------
    '''
    
    
    '''
    DESC
        Creates a dictionary initialized with the base params for Battle.net API
        GET requests
    
    INPUT
    
    RETURN
        Dictionary with the following base params defined
        - namespace
        - access_token
        - locale
    '''
    def get_base_payload(self) -> dict:
        # check existing token
        if not self.has_valid_access_token():
            self.get_access_token()
        return {
            'namespace': self.namespaces['classic'],
            'locale': self.locale,
            'access_token': self.__access_token__
        }
    
    
    '''
    DESC
        Item data endpoint /data/wow/item/{itemId}
        
    INPUT
        Unique ItemID of the item
        
    RETURN
        JSON response body
    '''
    def get_item_metadata(self, itemid) -> dict:  
        # prepare GET metadata
        base_url = 'https://us.api.blizzard.com/data/wow/item/{itemid}'
        url = base_url.format(itemid=itemid)
        payload = self.get_base_payload()
        
        # GET request
        r = requests.get(url, params=payload)
        if r.status_code == 200:
            return r.json()
        else:
            r.raise_for_status()
            
        return None
        

    '''
    DESC
        Item media endpoint /data/wow/media/item/{itemId}
        
    INPUT
        Unique ItemID of the item
        
    RETURN
        JSON response body
    '''
    def get_item_media_metadata(self, itemid) -> dict:  
        # prepare GET metadata
        base_url = 'https://us.api.blizzard.com/data/wow/media/item/{itemid}'
        url = base_url.format(itemid=itemid)
        payload = self.get_base_payload()
        
        # GET request
        r = requests.get(url, params=payload)
        if r.status_code == 200:
            return r.json()
        else:
            r.raise_for_status()
            
        return None


'''
Main code
'''

def main():
    util = BNetAPIUtil()
    if not util.has_valid_access_token():
        util.get_access_token()
    item_data = util.get_item_media_metadata(19019)
    print(json.dumps(item_data))
    
if __name__ == "__main__":
    main()
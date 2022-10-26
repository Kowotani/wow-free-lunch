import requests
from requests.auth import HTTPBasicAuth
import datetime as dt


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
    DESC
        Class constructor
        
    INPUT
    
    RETURN
        Empty state object
    '''
    def __init__(self):
        self.__access_token__ = None
    
    '''
    DESC
        Creates an HTTPBasicAuth object with Battle.net API access keys
        
    INPUT
        
    RETURN
        HTTPBasicAuth object       
    '''
    def __get_auth_object(self):
        return HTTPBasicAuth(self.__CLIENT_ID__, self.__CLIENT_SECRET__)


    '''
    DESC
        Update the new access token from Battle.net service for API use if
        necessary (ie. existing token is None or is expired)
    
    INPUT
    
    RETURN
    '''
    def update_access_token(self):
        # only update if necessary
        if self.__access_token__ is None or \
            dt.datetime.now() > self.access_token_expiration:
        
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
Main code
'''

def main():
    util = BNetAPIUtil()
    util.update_access_token()


if __name__ == "__main__":
    main()
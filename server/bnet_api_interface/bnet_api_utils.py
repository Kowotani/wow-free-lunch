import datetime as dt
from enum import Enum
import json
import requests
from requests.auth import HTTPBasicAuth


'''
This enum enumerates the CLASSIC and RETAIL versions of WoW
'''
class GameVersion(Enum):
    CLASSIC = 1
    RETAIL = 2


'''
This class handles interfacing with the Battle.net API for retrieval of
game data
'''

class BNetAPIUtil:

    '''
    ===============
    Class Variables
    ===============
    '''

    '''
    --------------------------
    Generic Endpoint Variables
    --------------------------
    '''

    '''
    Battle.net API access keys
    '''
    _CLIENT_ID = '4e41cbadc23f466ea64c61e382c08bd1'
    _CLIENT_SECRET = '1f768iHJc3bPjS6D8j4zXO1nLvYFXE5l'
    
    
    '''
    Access token metadata
    '''
    _access_token = None
    access_token_expiration = None


    '''
    Other API Inputs
    '''
    base_api_url = 'https://us.api.blizzard.com/data/wow'
    # TODO: consider non-static namespaces (eg. dynamic, profile)
    # Only use US region
    namespaces = {
        GameVersion.CLASSIC: 'static-classic-us',
        GameVersion.RETAIL: 'static-us'
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
        self._access_token = None
    
    
    '''
    ================
    Helper Functions
    ================
    '''
    
    '''
    DESC
        Handles a response from a Requests call - if the status is good (200) 
        this will return the response body, otherwise it will raise an exception
        
    INPUT
        Response from a Requests GET or POST call
        
    RETURN
        Response body as JSON if the status is good (200)
    '''
    @staticmethod
    def handle_request_response(response) -> dict:
        
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
            
        return None
    
    
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
    def _get_auth_object(self) -> HTTPBasicAuth:
        
        return HTTPBasicAuth(self._CLIENT_ID, self._CLIENT_SECRET)

    '''
    DESC
        Determines if the access token is still valid
    
    INPUT
    
    RETURN
        TRUE if the access token is still valid, FALSE otherwise
    '''
    def has_valid_access_token(self) -> bool:
        
        return self._access_token is not None and \
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
        auth = self._get_auth_object()
        data = {'grant_type' : 'client_credentials'}
        
        # POST request
        r = requests.post(url, auth=auth, data=data)
        body = BNetAPIUtil.handle_request_response(r)
        self._access_token = body['access_token']
        self.access_token_expiration = dt.datetime.now() + \
            dt.timedelta(seconds=body['expires_in'])
            

    '''
    =============
    API Functions
    =============
    
    These functions map 1:1 with Battle.net API functions defined in
    https://develop.battle.net/documentation/world-of-warcraft and
    https://develop.battle.net/documentation/world-of-warcraft-classic
    '''
    
    
    '''
    ----------------
    Helper Functions
    ----------------
    '''
    
    
    '''
    DESC
        Verifies whether the input is of type GameVersion, raise an exception
        if it is not
    
    INPUT
        Maybe a GameVersion enum
    
    RETURN
    '''
    def _verify_game_version(self, game_version) -> None:
        
        if game_version not in GameVersion:
            raise TypeError('{} not found in GameVersion'.format(game_version))
    
    
    '''
    DESC
        Creates a dictionary initialized with the base params for Battle.net API
        GET requests
    
    INPUT
        GameVersion enum
    
    RETURN
        Dictionary with the following base params defined
        - namespace
        - access_token
        - locale
    '''
    def _get_base_payload(self, game_version) -> dict:
        
        # check existing token
        if not self.has_valid_access_token():
            self.get_access_token()
            
        return {
            'namespace': self.namespaces[game_version],
            'locale': self.locale,
            'access_token': self._access_token
        }
    
        
    '''
    --------------
    Item Endpoints
    --------------
    '''
    
    
    '''
    DESC
        Item data endpoint /item/{itemId}
        
    INPUT
        - Unique ItemID of the item
        - Version of WoW (Classic / Retail)
        
    RETURN
        JSON response body
    '''
    def get_item_metadata(self, item_id, game_version) -> dict: 
        
        # prepare GET metadata
        self._verify_game_version(game_version)
        base_url = self.base_api_url + '/item/{item_id}'
        url = base_url.format(item_id=item_id)
        payload = self._get_base_payload(game_version)
        
        # GET request
        r = requests.get(url, params=payload)
        return BNetAPIUtil.handle_request_response(r)
        

    '''
    DESC
        Item media endpoint /media/item/{itemId}
        
    INPUT
        - Unique ItemID of the item
        - Version of WoW (Classic / Retail)
        
    RETURN
        JSON response body
    '''
    def get_item_media_metadata(self, item_id, game_version) -> dict:  
        
        # prepare GET metadata
        self._verify_game_version(game_version)
        base_url = self.base_api_url + '/media/item/{item_id}'
        url = base_url.format(item_id=item_id)
        payload = self._get_base_payload(game_version)
        
        # GET request
        r = requests.get(url, params=payload)
        return BNetAPIUtil.handle_request_response(r)


    '''
    DESC
        Item class index endpoint /item-class/index. This endpoint is 
        supported on both CLASSIC and RETAIL but this method will only be
        used on RETAIL.
        
    INPUT
        
    RETURN
        JSON response body
    '''
    def get_item_class_index(self) -> dict: 
        
        # prepare GET metadata
        url = self.base_api_url + '/item-class/index'
        # this method will only be called on RETAIL
        payload = self._get_base_payload(GameVersion.RETAIL)
        
        # GET request
        r = requests.get(url, params=payload)
        return BNetAPIUtil.handle_request_response(r)


    '''
    DESC
        Item subclass endpoint 
        /item-class/{itemCLassId}/item-subclass/{itemSubclassId}. This endpoint 
        is supported on both CLASSIC and RETAIL but this method will only be
        used on RETAIL.
        
    INPUT
        
    RETURN
        JSON response body
    '''
    def get_item_subclass(self, item_class_id, item_subclass_id) -> dict: 
        
        # prepare GET metadata
        base_url = self.base_api_url + \
            '/item-class/{item_class_id}/item-subclass/{item_subclass_id}'
        url = base_url.format(item_class_id=item_class_id, 
            item_subclass_id=item_subclass_id)
        # this method will only be called on RETAIL
        payload = self._get_base_payload(GameVersion.RETAIL)
        
        # GET request
        r = requests.get(url, params=payload)
        return BNetAPIUtil.handle_request_response(r)


    '''
    --------------------
    Profession Endpoints
    --------------------
    '''
    

    '''
    DESC
        Profession index endpoint /profession/index. Only supported on RETAIL
        
    INPUT
        
    RETURN
        JSON response body
    '''
    def get_profession_index(self) -> dict:  
        
        # prepare GET metadata
        url = self.base_api_url + '/profession/index'
        # this endpoint is only supported on RETAIL
        payload = self._get_base_payload(GameVersion.RETAIL)
        
        # GET request
        r = requests.get(url, params=payload)
        return BNetAPIUtil.handle_request_response(r)  


    '''
    DESC
        Profession endpoint /profession/{professionId}
        
    INPUT
        Unique ProfessionID of the Profession
        
    RETURN
        JSON response body
    '''
    def get_profession_metadata(self, profession_id) -> dict: 
        
        # prepare GET metadata
        base_url = self.base_api_url + '/profession/{profession_id}'
        url = base_url.format(profession_id=profession_id)
        # this endpoint is only supported on RETAIL
        payload = self._get_base_payload(GameVersion.RETAIL)
        
        # GET request
        r = requests.get(url, params=payload)
        return BNetAPIUtil.handle_request_response(r)


    '''
    DESC
        Profession endpoint /media/profession/{professionId}
        
    INPUT
        Unique ProfessionID of the Profession
        
    RETURN
        JSON response body
    '''
    def get_profession_media_metadata(self, profession_id) -> dict: 
        
        # prepare GET metadata
        base_url = self.base_api_url + '/media/profession/{profession_id}'
        url = base_url.format(profession_id=profession_id)
        # this endpoint is only supported on RETAIL
        payload = self._get_base_payload(GameVersion.RETAIL)
        
        # GET request
        r = requests.get(url, params=payload)
        return BNetAPIUtil.handle_request_response(r)


    '''
    DESC
        Profession skill tier endpoint 
        /profession/{professionId}/skill-tier/{skillTierId}
        
    INPUT
        - Unique ProfessionID of the Profession
        - Unique SkilltierID of the Profession's Skill Tier
        
    RETURN
        JSON response body
    '''
    def get_profession_skill_tier_metadata(self, profession_id, 
        skill_tier_id) -> dict:  
            
        # prepare GET metadata
        base_url = self.base_api_url + \
            '/profession/{profession_id}/skill-tier/{skill_tier_id}'
        url = base_url.format(profession_id=profession_id, 
            skill_tier_id=skill_tier_id)
        # this endpoint is only supported on RETAIL
        payload = self._get_base_payload(GameVersion.RETAIL)
        
        # GET request
        r = requests.get(url, params=payload)
        return BNetAPIUtil.handle_request_response(r)


    '''
    DESC
        Recipe endpoint /recipe/{recipeID}
        
    INPUT
        Unique RecipeID of the Recipe
        
    RETURN
        JSON response body
    '''
    def get_recipe_metadata(self, recipe_id) -> dict:  
            
        # prepare GET metadata
        base_url = self.base_api_url + '/recipe/{recipe_id}'
        url = base_url.format(recipe_id=recipe_id)
        # this endpoint is only supported on RETAIL
        payload = self._get_base_payload(GameVersion.RETAIL)
        
        # GET request
        r = requests.get(url, params=payload)
        return BNetAPIUtil.handle_request_response(r)
        
        
    '''
    DESC
        Recipe Media endpoint /media/recipe/{recipeID}
        
    INPUT
        Unique RecipeID of the Recipe
        
    RETURN
        JSON response body
    '''
    def get_recipe_media_metadata(self, recipe_id) -> dict:  
            
        # prepare GET metadata
        base_url = self.base_api_url + '/media/recipe/{recipe_id}'
        url = base_url.format(recipe_id=recipe_id)
        # this endpoint is only supported on RETAIL
        payload = self._get_base_payload(GameVersion.RETAIL)
        
        # GET request
        r = requests.get(url, params=payload)
        return BNetAPIUtil.handle_request_response(r)         


'''
Main code
'''

def main():
    util = BNetAPIUtil()
    # data = util.get_profession_index()
    data = util.get_profession_media(164)
    # data = util.get_item_media_metadata(19019, GameVersion.RETAIL)
    # data = util.get_profession_skill_tier_metadata(197, 2540)
    # data = util.get_recipe_media_metadata(2360)
    print(json.dumps(data))
    
if __name__ == "__main__":
    main()
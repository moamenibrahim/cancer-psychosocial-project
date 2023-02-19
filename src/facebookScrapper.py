import requests
import json

class FacebookScraper():
    def __init__(base_url="https://graph.facebook.com/me"):
        self.base_url = base_url
        
    def get_content():
        """ Get 10 likes for 10 friends """
        fields = "id,name,friends.limit(10).fields(likes.limit(10))"
        url = "{base_url}?fields={fields}&access_token={ACCESS_TOKEN}"
        content = requests.get(url).json()
        print(json.dumps(content, indent=1))

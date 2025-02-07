## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2747.html

## Affected version

i22 V1.0.0.3(4687)

## Vulnerability details

In the i22 V1.0.0.3(4687) firmware has a stack overflow vulnerability in the `formSetUrlFilterRule` function. The `v1` variable receives the `groupIndex` parameter from a POST request and is passed to function `sub_75B4C` as `a3`. In function `sub_75B4C`, variable `a3` is passed to function `sub_752D4` as `a2`. However, since the user can control the input of `groupIndex`, the statement `sprintf(v7, "%s%d", a1, a2);` can cause a buffer overflow. The user-provided  `groupIndex` can exceed the capacity of the `v7` array, triggering this security vulnerability.

![image-20240419170841776](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240419170841776.png)

![image-20240419171112268](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240419171112268.png)

![image-20240419171054168](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240419171054168.png)

## POC

```python
data = {"groupIndex": payload}
response = requests.post(url, data=data)
```

![image-20240419162115799](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240419162115799.png)

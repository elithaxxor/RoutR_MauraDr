## Overview

- Firmware download website: https://www.tendacn.com/download/detail-2722.html

## Affected version

W15EV1.0 V15.11.0.14

## Vulnerability details

The Tenda W15EV1.0 V15.11.0.14 firmware has a stack overflow vulnerability in the `formQOSRuleDel` function. The `indexSet` variable receives the `qosIndex` parameter from a POST request and is directly assigned to `strcpy`. However, since the user can control the input of `qosIndex `, the statement`strcpy((char *)&input, (const char *)indexSet);` can cause a buffer overflow. The user-provided  `qosIndex` can exceed the capacity of the `input` array, triggering this security vulnerability.

![image-20240417100646839](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240417100646839.png)

## POC

![image-20240416114043980](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240416114043980.png)

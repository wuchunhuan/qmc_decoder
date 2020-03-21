# QQ音乐解密器
可以解密app中下载的（qmc3，qmc0，qmcflac）文件，python实现

[![LICENSE](https://img.shields.io/badge/license-MIT-red)](./LICENSE)

![Python Version](https://img.shields.io/badge/Python-V3-blue)

## 使用方法
```
python3 path/to/qmc_decoder -m -o output_path input_path
```
### 参数
- `-m` 使用多进程同时解密，可以利用多核CPU加速解密，可选参数
- `-o` 设置输出目录，默认为当前目录下新建output，可选参数
- `input_path` 设置包含qmc3，qmc0，qmcflac等文件的目录

## Support
wuchunhuan@gmail.com
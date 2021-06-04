# fileprotect 文件保护
此脚本目的是为了在awd比赛中保护文件，防止木马上传、修改文件等行为

## 功能
* 备份当前目录所有文件至./bacck目录中
* 计算当前目录所有文件md5值，防止文件被篡改
* 实时检测是否有新文件或有文件被删除
* 删除的文件放在./bacck/deleteee中，并会加上随机数后缀以区分重名文件

## 使用
python2 或 python3
```bash
python3 ./fileprotect.py
```

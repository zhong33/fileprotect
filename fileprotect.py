#-*- encoding: utf-8 -*-

import os
import time
import random
import shutil
import hashlib

# 获取文件、目录
def getResList(dir):
    fileRes = []
    dirRes = []
    g = os.walk(dir)
    for path, dirList, fileList in g:
        if not path.startswith("./bacck"):
            for fileName in fileList:
                if fileName != "./filelog.log":
                    fileRes.append(os.path.join(path, fileName))
            for dirName in dirList:
                dirRes.append(os.path.join(path, dirName))
    return (fileRes, dirRes)

# 获取文件hash
def getHash(fileList):
    hashRes = []
    for fileName in fileList:
        with open(fileName, "rb") as f:
            data = f.read()
        hashRes.append([fileName, hashlib.md5(data).hexdigest()])
    return hashRes

# 备份文件
def backup(fileList, dirList, hashList, log):
    backupDir = "./bacck"
    backupList = []
    if os.path.isdir(backupDir):
        shutil.rmtree(backupDir)
        backup(fileList, dirList, hashList, log)
    else:
        os.makedirs(backupDir)
        for now in dirList:
            if now != backupDir:
                os.makedirs(backupDir + now[1:])
        for now in fileList:
            tmpDir = backupDir + now[1:]
            backupList.append(tmpDir)
            shutil.copy(now, tmpDir)
        log.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " [+] backup files success!\n")
        print("[+] backup files success!")

# 检测文件
def check(path, oldList, log):
    deleteDir = "./bacck/deleteee"
    if not os.path.isdir(deleteDir):
        os.makedirs(deleteDir)
    newList = getResList(path)[0]
    for now in newList:
        if oldList.count(now) == 0:
            rand = str(random.randint(0,99999))
            os.rename(now, now+rand)
            shutil.move(now+rand, deleteDir)
            log.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " [-] delete file {}!\n".format(now+rand))
            print("[-] delete file {}!".format(now))
    
# 恢复文件
def recoverFiles(path, oldList, hashList, log):
    newList = getResList(path)[0]
    for now in oldList:
        if newList.count(now) == 0:
            backupDir = "./bacck" + now[1:]
            shutil.copy(backupDir, now)
            log.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "[+] recover file {}!\n".format(now))
            print("[+] recover file {}!".format(now))
    newHashList = getHash(newList)
    for now in hashList:
        # if newHashList.count(now) == 0 and now[0] != "./.DS_Store":
        if newHashList.count(now) == 0:
            backupDir = "./bacck" + now[0][1:]
            os.remove(now[0])
            shutil.copy(backupDir, now[0])
            log.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " [+] recover file {}!\n".format(now[0]))
            print("[+] recover file {}!".format(now[0]))

def main():
    path = r"./"
    log = open("filelog.log", "a")
    (fileList, dirList) = getResList(path)
    hashList = getHash(fileList)
    backup(fileList, dirList, hashList, log)
    while True:
        check(path, fileList, log)
        recoverFiles(path, fileList, hashList, log)
        # time.sleep(2)

if __name__ == "__main__":
    main()

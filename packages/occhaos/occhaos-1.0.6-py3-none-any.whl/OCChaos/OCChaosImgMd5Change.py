# -*- coding: utf-8 -*-

import hashlib
import os

from OCChaos.OCChaosConfig import OCChaosConfig


class OCChaosImgMd5Change(object):
    def __init__(self,config):
        self.config = config

    # 获取MD5
    def GetFileMd5(self, filename):
        if not os.path.isfile(filename):
            return
        myhash = hashlib.md5()
        f = open(filename, 'rb')
        while True:
            b = f.read(8096)
            if not b:
                break
            myhash.update(b)
        f.close()
        return myhash.hexdigest()

    # 给文件添加末尾，改变md5
    def fileAppend(self, filename):
        myfile = open(filename, 'a')
        # 添加一个自定义内容，并不影响文件
        myfile.write("jneth")
        myfile.close

    # 遍历文件，符合规则的进行重命名
    # 项目路径   （找到自己的项目路径）
    def start_change_img_md5(self):

        for (root, dirs, files) in os.walk(self.config.getProject_path()):
            for file_name in files:
                if file_name.endswith(self.config.getImg_suf_set()):
                    short_name = os.path.splitext(file_name)[0]
                    realpath = os.path.join(root, file_name)
                    print(short_name + ' ==> ' + realpath)
                    oldMd5 = os.GetFileMd5(realpath)
                    os.fileAppend(realpath)
                    newMd5 = os.GetFileMd5(realpath)
                    print(oldMd5 + '-->' + newMd5)


if __name__ == "__main__":
    md5 = OCChaosImgMd5Change()
    md5.start_change_img_md5()

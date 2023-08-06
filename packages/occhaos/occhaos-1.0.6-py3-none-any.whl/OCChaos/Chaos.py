# -*- coding: utf-8 -*-

from OCChaos.OCChaosImgMd5Change import OCChaosImgMd5Change
from OCChaos.OCChaosPrefixRe import OCChaosPrefixRe
from OCChaos.OCChaosUselessClassfile import OCChaosUselessClassfile
from OCChaos.OCChaosUselessCode import OCChaosUselessCode
from OCChaos.OCChaosConfig import OCChaosConfig


import json
import os,sys

keys=["pre_str","pre_to_str","suf_set","project_path","pbxpro_path","img_suf_set","file_floadPath","classArray","h_file_mark_arr","m_file_mark_arr","output_path"]

class OCChaos(object):

    def __init__(self,path=sys.path[0]+"/config.json"):
        self.path_config = OCChaosConfig(path=path)
        pass


    def changePrefixCallBack(self):
        pre = self.path_config.getPre_str()
        pre_to = self.path_config.getPre_to_str()
        if len(pre_to) == 0  and len(pre) == 0:
            print("类名旧前缀与新前缀没有设置")
            return
        OCChaosPrefixRe(config=self.path_config).start_rename()
        # print(self.path_config.get())

    def changeMd5CallBack(self):
        project_path = self.path_config.getProject_path()
        img_suf = self.path_config.getImg_suf_set()
        if len(project_path) == 0 or len(img_suf) == 0:
            print("工程路径与图片文件后缀没有设置")
            return
        OCChaosImgMd5Change(config=self.path_config).start_change_img_md5()

    def createUselessClassCallBack(self):
        project_path = self.path_config.getProject_path()
        output_path = self.path_config.getOutput_path()
        if len(project_path) == 0 or len(output_path) == 0:
            print("工程路径与输出路径没有设置")
            return
        OCChaosUselessClassfile(config=self.path_config).start_create_files(fileCount=20,output_path=output_path)

    def insertUselessCodeCallBack(self):
        project_path = self.path_config.getProject_path()
        if len(project_path)==0:
            print("工程路径没有设置")
            return
        OCChaosUselessCode(config=self.path_config).start_create_useless_code(project_path)


def check_file():
    print("请输入配置文件路径(请严格按照配置示例进行配置):")
    file_check_flag = True
    config_path = input()

    if len(config_path.replace(" ","")) == 0:
        print("需要输入正确的配置文件路径！")
        return(check_file())
    else:
        if config_path.endswith(".json"):
            with open(config_path, 'r') as f:
                temp = json.loads(f.read())
                print("读取json")
                for k in keys:
                    if k not in temp:
                        print(k+"键值不存在或者错误,请检查配置文件\n")
                        file_check_flag = False
                print("读取json校验完成")
                if file_check_flag:

                    return config_path,os.path.exists(config_path)
                else:
                    return(check_file())#python中递归调用 要使用return
        else:
            print("需要输入正确的配置文件路径！")
            return(check_file())


def select_funtion(config_path):

    print("请选择要执行的功能:\n1.更换文件前缀;\n2.生成无用的.h .m文件;\n3.更改资源图片的md5值;\n4.已有.h .m添加废弃代码\n\n请输入序号，按回车")

    cmd_str = input()
    if cmd_str is "1":
        print("更换文件前缀")
        OCChaos(path=config_path).changePrefixCallBack()
    elif cmd_str is "2":
        print("生成无用的.h .m文件")
        OCChaos(path=config_path).createUselessClassCallBack()
    elif cmd_str is "3":
        print("更改资源图片的md5值")
        OCChaos(path=config_path).changeMd5CallBack()
    elif cmd_str is "4":
        print("已有.h .m添加废弃代码")
        OCChaos(path=config_path).insertUselessCodeCallBack()
    else:
        print("请输入正确序号！")
        select_funtion()

def start_action():

    config_path,file_check_result = check_file()

    if file_check_result:
        while True:
            select_funtion(config_path)


if __name__ == '__main__':
    start_action()
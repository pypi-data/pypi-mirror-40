# -*- coding: utf-8 -*-

import json
import os,sys

class OCChaosConfig(object):

    def __init__(self,path):
        self.jsonData = self.get_json_data(path)

    def getPre_str(self):
        return self.jsonData['pre_str']

    def getPre_to_str(self):
        return self.jsonData['pre_to_str']

    def getSuf_set(self):
        return tuple(self.jsonData['suf_set'])

    def getProject_path(self):
        return self.jsonData['project_path']

    def getPbxpro_path(self):
        return self.jsonData['pbxpro_path']

    def getImg_suf_set(self):
        return tuple(self.jsonData['img_suf_set'])

    def getFile_floadPath(self):
        return self.jsonData['file_floadPath']

    def getClassArray(self):
        return self.jsonData['classArray']

    def getH_file_mark_arr(self):
        return self.jsonData['h_file_mark_arr']

    def getM_file_mark_arr(self):
        return self.jsonData['m_file_mark_arr']

    def getOutput_path(self):
        return self.jsonData['output_path']

    def get_json_data(self,path=sys.path[0]+"/config.json"):
        with open(path, 'r') as f:
            temp = json.loads(f.read())
            return temp


# if __name__ == "__main__":
#
#     config = OCChaos_Config()
#     print(config.getImg_suf_set())

'''
一些参数的说明
#需要修改的类名前缀 （需替换）
pre_str = 'ZTY'
# 新的类名前缀 （需替换）
pre_to_str = 'TY'
# 搜寻以下文件类型 （根据自己需求替换）
suf_set = ('.h', '.m', '.xib', '.storyboard', '.mm')
# 项目路径   （找到自己的项目路径）
project_path = '/Volumes/Files/Document/LionMobi/TestIpa/TestIpa'
# 项目project.pbxproj文件路径 需要更新配置文件中的类名 （找到自己的项目project.pbxproj路径）
pbxpro_path = '/Volumes/Files/Document/LionMobi/TestIpa/TestIpa.xcodeproj/project.pbxproj'

# 设置以这些结尾的
img_suf_set = ('.png', '.jpg')

# 在目标.h  .m 文件所在的路径
file_floadPath = '/Volumes/Files/Document/LionMobi/TestIpa/TestIpa'

# .h文件里属性的类型从这个数组里随机选(按需修改)
classArray = ['NSString', 'UILabel', 'NSDictionary', 'NSData', 'UIScrollView', 'UIView', 'UITextView', 'UITableView',
              'UIImageView']

# .h   .m  文件中 需要在哪种标识后面添加废弃代码(按需修改)
h_file_mark_arr = ["l;", "m;", "n;", "q;", "y;"] # 往凡是以"l;", "m;","n;","q;","y;"这些中的某一个结尾的oc语句后添加废弃代码
m_file_mark_arr = ["n];", "w];", "m];", "c];", "p];", "q];", "l];"] # 往凡是以"n];", "w];","m];","c];","p];","q];","l];"这些中的某一个结尾的oc语句后添加废弃代码
'''


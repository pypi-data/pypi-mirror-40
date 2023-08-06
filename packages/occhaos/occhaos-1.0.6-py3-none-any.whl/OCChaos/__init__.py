# -*- coding:utf-8 -*-

import json

import OCChaos.Chaos

# keys=["pre_str","pre_to_str","suf_set","project_path","pbxpro_path","img_suf_set","file_floadPath","classArray","h_file_mark_arr","m_file_mark_arr"]
#
# def check_file():
#     print("请输入配置文件路径(请严格按照配置示例进行配置):")
#     file_check_flag = True
#     config_path = input()
#     if config_path.endswith(".json"):
#         with open(config_path, 'r') as f:
#             temp = json.loads(f.read())
#             for k in keys:
#                 if k not in temp:
#                     print(k+"键值不存在或者错误,请检查配置文件\n")
#                     file_check_flag = False
#
#         if file_check_flag:
#             return config_path,os.path.exists(config_path)
#         else:
#             check_file()
#     else:
#         print("需要输入正确的配置文件路径！")
#         check_file()
#
# def select_funtion(config_path:str):
#
#     print("请选择要执行的功能:\n1.更换文件前缀;\n2.生成无用的.h .m文件;\n3.更改资源图片的md5值;\n4.已有.h .m添加废弃代码\n\n请输入序号，按回车")
#     chaos = OCChaos(path=config_path)
#     cmd_str = input()
#     if cmd_str is "1":
#         print("更换文件前缀")
#
#         chaos.changePrefixCallBack()
#     elif cmd_str is "2":
#         print("生成无用的.h .m文件")
#         chaos.createUselessClassCallBack()
#     elif cmd_str is "3":
#         print("更改资源图片的md5值")
#         chaos.changeMd5CallBack()
#     elif cmd_str is "4":
#         print("已有.h .m添加废弃代码")
#         chaos.insertUselessCodeCallBack()
#     else:
#         print("请输入正确序号！")
#         start_action()
#
# def start_action():
#
#     config_path,file_check_result = check_file()
#     if file_check_result == False:
#         check_file()
#         return
#     while True:
#         select_funtion(config_path)

# if __name__ == '__main__':
#     OCChaos.Chaos.start_action()
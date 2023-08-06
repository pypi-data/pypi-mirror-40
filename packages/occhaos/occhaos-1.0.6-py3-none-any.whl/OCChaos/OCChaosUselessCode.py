# -*- coding: utf-8 -*-

import random

import os

from OCChaos.OCChaosConfig import OCChaosConfig


class OCChaosUselessCode(object):
    second = "abcdefghijklmnopqrstuvwxyz"

    first = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    third = "1234567890"

    number = "345"

    index = 0

    viewArray = ['UILabel', 'UIScrollView', 'UIView', 'UITextView', 'UITableView',
                 'UIImageView']  # .m文件里创建的元素的类型从这个数组里随机选
    name_array = []

    def __init__(self,config):
        self.config = config

    def getNameArray(self):
        for i in range(500):

            final = (random.choice(self.first))

            index = random.randint(3, 5)

            for i in range(index):
                final += (random.choice(self.first))

            final += (random.choice(self.second))

            for i in range(index):
                final += (random.choice(self.third))

            self.name_array.append(final)

    # .h文件添加废代码

    def HFileAddMj(self, file_path, old_str_arr):
        file_data = ""

        Ropen = open(file_path, 'r')

        for line in Ropen:

            nameStr = random.choice(self.name_array)

            className = random.choice(self.config.getClassArray())

            for old_str in old_str_arr:

                if old_str in line:
                    line += '\n\n/*********FQ代码**********/\n' \
                            '@property(nonatomic,strong) ' + className + ' * ' + nameStr + ';' + \
                            '\n/*********FQ代码**********/\n\n'
                    self.name_array.remove(nameStr)  # 防止创建的属性名重复(创建一个从数组中删除一个)
                    break;

            file_data += line

        Ropen.close()

        Wopen = open(file_path, 'w')

        Wopen.write(file_data)

        Wopen.close()

        print(file_data)

    # .m文件添加废代码

    def MFileAddMj(self, file_path, old_str_arr):
        file_data = ""

        Ropen = open(file_path, 'r')  # 读取文件

        for line in Ropen:

            nameStr = random.choice(self.name_array)

            className = random.choice(self.viewArray)

            for old_str in old_str_arr:

                if old_str in line:  # 如果.h文件中的某一行里包含old_str,则往这一行添加一下语句

                    line += '\n\n\t/*********FQ代码**********/\n\t' \
                            + className + ' * ' + nameStr + ' = ' + '[[' + className + ' alloc]initWithFrame:CGRectMake(' + str(
                        random.randint(0, 100)) + ',' + str(random.randint(0, 100)) + ',' + str(
                        random.randint(0, 100)) + ',' + str(
                        random.randint(0, 100)) + ')];\n' + \
                            '\t' + nameStr + '.layer.cornerRadius =' + str(random.randint(5, 10)) + ';\n\t' \
                            + nameStr + '.userInteractionEnabled = YES;\n\t' \
                            + nameStr + '.layer.masksToBounds = YES;' + \
                            '\n\t/*********FQ代码**********/\n\n'

                    # file_data += line

                    self.name_array.remove(nameStr)  # 防止创建的元素名重复(创建一个从数组中删除一个)
                    break;
            file_data += line

        Ropen.close()

        Wopen = open(file_path, 'w')

        Wopen.write(file_data)

        Wopen.close()

        print(file_data)

    def file_name(self, file_dir):
        for root, dirs, files in os.walk(file_dir):

            # print(root) #当前目录路径

            # print(dirs) #当前路径下所有子目录

            print(files)  # 当前路径下所有非目录子文件

            fileNameArray = files

            # 遍历文件夹下的.h和.m文件并添加废代码

            for file in fileNameArray:

                if '.h' in file:  # file_dir+'/'+file含义是file_dir文件夹下的file文件

                    self.HFileAddMj(file_dir + '/' + file, self.config.getH_file_mark_arr())

                if '.m' in file:
                    self.MFileAddMj(file_dir + '/' + file, self.config.getM_file_mark_arr())

    def start_create_useless_code(self,file_load_path):
        self.getNameArray()
        # 要修改的文件所在的文件夹路径
        self.file_name(file_load_path)


if __name__ == "__main__":
    useless_code = OCChaosUselessCode()
    useless_code.start_create_useless_code()

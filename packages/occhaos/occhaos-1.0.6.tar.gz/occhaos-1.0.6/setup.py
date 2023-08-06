#-*- encoding: UTF-8 -*-
from setuptools import setup, find_packages
"""
打包的用的setup必须引入，
"""

VERSION = '1.0.6'

packages = find_packages('OCChaos'),  # 包含所有src中的包
package_dir = {'':'OCChaos'},   # 告诉distutils包都在src下

setup(name='occhaos',
      version=VERSION,
      description="iOS中  OC马甲包制作中，前缀、后缀、垃圾代码生成、加入垃圾代码方案",
      long_description='iOS中  OC马甲包制作中，前缀、后缀、垃圾代码生成、加入垃圾代码方案',
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='iOS 马甲包 垃圾代码 混淆',
      author='tywin',
      author_email='tywinzhang2017@gmail.com',
      url='https://github.com/ilioner/OCChaos',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=True,
      entry_points={
        'console_scripts':[
            'occhaos = OCChaos.Chaos:start_action'
        ]
      }
)
from distutils.core import setup #如果没有需要先安装
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

setup(
      name='Telecontrol',  #打包后的包文件名 
      version='1.2',  #版本
      description='a Telecontrol',   
      author=' Mr.yan',   
      license="Apache-2.0",
      author_email=' mryan050415@gmail.com',   
      url=' https://github.com/SuperSystemStudio/TelecontrolCodeRepairwoman',   
      py_modules=['TelecontrolCodeRepairwoman'],  #与前面的新建文件名一致 
      entry_points={
        'console_scripts': [
            'ssh start = TelecontrolCodeRepairwoman:main',#pip安装完成后可使用demo命令调用demo下的main方法
        ],
      },
)
#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 都君丨大魔王
import re
import time
from PyQt5 import QtCore

file_content = "/** -1：教学版, 0: 基础版, 1: 高级版, 2: 高级联网版, 3: 专家版 */\n" \
               "module.exports = {topLevel: 2,debug: 1,devTools: 0};"


class FileOperate(QtCore.QThread):
    text = QtCore.pyqtSignal(str)

    def __init__(self, client_value):
        super().__init__()
        self.edition = client_value.get('edition')
        self.model = client_value.get('model')
        self.save_path = client_value.get('save_path')

    def create_file(self):
        """"""
        edition_dict = {'教学版': -1, '基础版': 0, '高级版': 1, '高级联网版': 2, '专家版': 3}
        edition_value = edition_dict.get(self.edition)
        model_list = ['关闭', '打开']
        model_value = model_list[self.model]
        new_content = re.sub(r'topLevel: (.*?),debug: (.*?),',
                             f'topLevel: {edition_value},debug: {self.model},',
                             file_content)
        try:
            with open(f"{self.save_path}\\locConf.js", 'w', encoding='utf-8') as file:
                file.write(new_content)
            wait_time = 3
            while wait_time > 0:
                info = f"当前版本为【{self.edition}】，开发者模式【{model_value}】，需要重启鉴定系统生效！！！ {wait_time}"
                self.text.emit(info)
                time.sleep(1)
                wait_time = wait_time - 1
            self.text.emit('')
        except IOError:
            self.text.emit(f'{self.save_path}目录不存在，请正确选择鉴定系统安装目录！')

    def run(self) -> None:
        self.create_file()

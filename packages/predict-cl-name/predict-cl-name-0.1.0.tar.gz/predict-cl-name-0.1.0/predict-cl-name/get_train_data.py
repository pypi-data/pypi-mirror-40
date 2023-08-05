from settings import config
from settings.config import MergeLog
import time


class ReadName(object):
    def __init__(self):
        self.word_list = []
        self.file_person_name = [config.filename["ancient_name"],
                                 config.filename["chinese_name"],
                                 config.filename["english_name_cn"],
                                 config.filename["english_name"],
                                 config.filename["japanese_name"]]
        self.file_company = [config.filename["company_name"],
                             config.filename["organization"]]
        self.n = 50000

    def read_person_name(self):
        MergeLog.info("开始读取人名数据............")
        start_time = time.time()
        for file in self.file_person_name:
            with open(file, "r", encoding="utf-8", errors="ignore") as f:
                i = 0
                while i < self.n:
                    text = f.readline()
                    if not text:
                        break
                    word_dict = {}
                    text = text.replace("\n", "")
                    if text not in ["\ufeffBy@萌名", "2018.12.03", " ", "By@萌名"]:
                        word_dict[text] = "人名"
                        self.word_list.append(word_dict)
                    i += 1
        MergeLog.info("人名数据读取完毕...............")
        MergeLog.info("读取人名数据耗时：{} s".format(time.time() - start_time))

    def read_company_name(self):
        MergeLog.info("开始读取公司或机构数据............")
        start_time = time.time()
        for file in self.file_company:
            with open(file, "r", encoding="utf-8", errors="ignore") as f:
                i = 0
                while i < self.n:
                    text = f.readline()
                    if not text:
                        break
                    word_dict = {}
                    text = text.replace("\n", "")
                    if text not in ["\ufeffBy@萌名", "2018.12.03", "\n", "By@萌名"]:
                        word_dict[text] = "公司或机构"
                        self.word_list.append(word_dict)
                    i += 1
        MergeLog.info("公司或机构数据读取完毕...............")
        MergeLog.info("读取公司或机构数据耗时：{} s".format(time.time() - start_time))

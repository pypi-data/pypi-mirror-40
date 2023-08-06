from enum import Enum, unique
from .config import ConfigManager
from .indexes import IndexManager, Index
from .processer import character_filter, character_cn_filter, word_segment

import logging
import re

logger = logging.getLogger(ConfigManager.logger_name)


@unique
class SearchQueryObjectType(Enum):
    FullMatch = 1,
    WordMatch = 2,
    RegexMatch = 3


class SearchQueryObject:
    index = None  # Index对象
    raw = ''  # 输入的原始关键词
    keyword_count = 0  # 输入的关键词数量
    matching_type = None  # 匹配的类型
    matching_count = 0  # 匹配到的词数量
    matching_score = 0  # 匹配度，全匹配则为1；词匹配：输入的关键词在索引中出现的次数 / 总关键词数量

    def __init__(self, index: Index, raw: str, keyword_count: int, matching_type: SearchQueryObjectType):
        """
        SearchQueryObject 初始化
        :param index: 索引对象
        :param raw: 输入的匹配内容
        :param keyword_count: 关键词数量，用于计算词模式的匹配度
        :param matching_type: 匹配的类型
        """
        self.index = index
        self.raw = raw
        self.keyword_count = keyword_count
        self.matching_type = matching_type

    @property
    def __id__(self):
        return self.index.__id__

    def __repr__(self):
        return '<SearchQueryObject {}:{} index:{} raw:{} matching_score:{}>'. \
            format(self.index.model_name,
                   self.index.primary_key,
                   self.index,
                   self.raw,
                   self.matching_score)

    @property
    def __dict__(self):
        model_dict = self.index.get_model_instance().__dict__
        # 删掉无法序列化的字段
        if '_state' in model_dict:
            del model_dict['_state']

        data_dict = {
            'model_name': self.index.model_name,
            'primary_key': self.index.primary_key,
            'model_data': model_dict
        }
        return data_dict


class SearchQuerySet:
    objects = []  # SearchQueryObject 对象列表

    def __init__(self):
        self.objects = list()

    def add(self, obj: SearchQueryObject):
        self.objects.append(obj)

    def extend(self, query_set):
        self.objects.extend(query_set.objects)

    @property
    def all(self):
        self.objects.sort(key=lambda elem: elem.matching_score, reverse=True)
        return self.objects

    def remove_duplicates(self):
        temp_list = []
        new_objects = self.objects.copy()
        for item in self.objects:
            if item.__id__ in temp_list:
                new_objects.remove(item)
            else:
                temp_list.append(item.__id__)
        self.objects = new_objects

    def print(self):
        print('{} 匹配度 {}'.format(item.index.model_name, item.matching_score) for item in self.all)


class SearchQuery:
    @classmethod
    def query(cls, raw) -> SearchQuerySet:
        all_set = SearchQuerySet()

        full_set = cls.full_match(raw)
        all_set.extend(full_set)

        word_set = cls.word_match(raw)
        all_set.extend(word_set)

        # 当输入的搜索关键词长度小于符合正则匹配规则的时候启用正则匹配
        if len(raw) <= 2:
            pattern = r'\w'.join(raw)
            regex_set = cls.regex_match(pattern)
            all_set.extend(regex_set)

        # 去除重复结果
        all_set.remove_duplicates()

        return all_set

    @classmethod
    def full_match(cls, raw) -> SearchQuerySet:
        """全匹配搜索"""
        data = character_filter(raw)
        data = character_cn_filter(data)
        # 搜索结果集
        search_set = SearchQuerySet()
        for index in IndexManager.get_instance().indexes:
            search_obj = SearchQueryObject(index, raw, 1, SearchQueryObjectType.FullMatch)
            # 全匹配的匹配度为1
            search_obj.matching_score = 1
            for field_name, clean_data in index.clean_data.items():
                if data in clean_data:
                    search_set.add(search_obj)
                    logger.debug('full_match: {}'.format(search_obj.__dict__))
                    break
        return search_set

    @classmethod
    def word_match(cls, raw) -> SearchQuerySet:
        """词匹配搜索"""
        # 先对输入的搜索语分词处理
        keywords = word_segment(raw)
        # 搜索结果集
        search_set = SearchQuerySet()
        for index in IndexManager.get_instance().indexes:
            search_obj = SearchQueryObject(index, raw, len(keywords), SearchQueryObjectType.WordMatch)
            for word in keywords:
                # 统计匹配词数量，输入的关键词有多少个出现在索引数据里面
                for field_name, words_list in index.keywords.items():
                    if word in words_list:
                        # 检测到这个关键词的出现，记录下，跳出循环，测试下个关键词
                        search_obj.matching_count += 1
                        break
                # 计算匹配度：匹配词数量 / 总输入关键词数
                search_obj.matching_score = search_obj.matching_count / search_obj.keyword_count
            if search_obj.matching_score > 0:
                # 匹配度大于0才添加到结果集中
                search_set.add(search_obj)

        return search_set

    @classmethod
    def regex_match(cls, pattern):
        search_set = SearchQuerySet()
        for index in IndexManager.get_instance().indexes:
            search_obj = SearchQueryObject(index, pattern, 1, SearchQueryObjectType.RegexMatch)
            # 正则匹配的匹配度接近于0，所以这里取0
            search_obj.matching_score = 0
            for field_name, clean_data in index.clean_data.items():
                match_result = re.search(pattern, clean_data)
                if match_result is not None:
                    search_set.add(search_obj)
                    logger.debug('regex_match: {}'.format(search_obj.__dict__))
                    break
        return search_set


# if __name__ == '__main__':
#     result = SearchQuery.query('想的念')
#     print(result.objects)

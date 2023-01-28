import numpy as np
import pandas as pd

import re
from collections import Counter, defaultdict
from functools import partial
from tqdm import tqdm

from difflib import get_close_matches
from jamo import j2hcj, h2j
from kiwipiepy import Kiwi
# from module.collection import Crawling


class WordDict:
    def __init__(self) -> None:
        # 불용어 리스트
        self.StopwordList = []
        
        # 옵션처리 리스트
        self.OptionList = []
        
        # 단위 리스트
        self.UnitList = []
        
        # 표준화 사전
        self.StandardDict = defaultdict(dict)
        self.JamoToStandard = {}
        self.WordToStandard = {}
    
    def __del__(self):
        # 파일로 저장
        pass
    
    def updateDictonary(self, standard:str, word:str, idx:int=None, type:str='n'):
        if type == 'n':
            token = TokenKiwi('s')
            token.dictionary_add(standard)
            
            try:
                self.StandardDict[standard]['wordList'].add(word)
            except:
                self.StandardDict[standard]['wordList'] = {word}
            self.StandardDict[standard]['jamo'] = j2hcj(h2j(standard))
            
            self.WordToStandard[word] = standard
            self.JamoToStandard[j2hcj(h2j(standard))] = standard
            
        # print(standard, word, idx)
        if idx:
            try:
                self.StandardDict[standard]['idxList'].append(idx)
            except:
                self.StandardDict[standard]['idxList']= [idx]
            self.StandardDict[standard]['mean'] = np.mean(self.StandardDict[standard]['idxList'])
    
    # 유사도를 파악
    def ratioTop(self, word:str, stdWordList:list, n:int=5) -> str:
        stdJamoList = [j2hcj(h2j(w)) for w in stdWordList]
        jamo = j2hcj(h2j(word))
        if len(jamo) >= 8:
            cutoff = 0.8
        elif len(jamo) >= 6:
            cutoff = 0.75
        else:
            cutoff = 0.7
        close_matches = get_close_matches(jamo, stdJamoList, n, cutoff)
        # print(close_matches)
        if close_matches:
            close_matches = [self.JamoToStandard[j] for j in close_matches]
            if word not in close_matches:
                # print(close_matches)
                # 생크림 -크림
                if word == close_matches[1:]:
                    std = close_matches[i]
                    return std
                    
                # i = int(input(f'''{close_matches}- \n \"{word}\"의표준값이라고 생각하는 인덱스 적어주세요. 다 아니면 9'''))
                i = 9
                if i != 9:
                    std = close_matches[i]
                    return std
                return word
            return word
        else:
            return word
        
    
    def thisIsStandard(self, word:str, idx:int=None):
        try:    # 예전에 나온 단어인가요?
            self.updateDictonary(self.WordToStandard[word], word, idx, type='a')
            # print('idx add')
        except: # 처음 나오는데요
            stdWordList = self.StandardDict.keys()
            res = self.ratioTop(word, stdWordList)
            # print('thisIsStandard',res)
            if res:
                # print('update')
                self.updateDictonary(res, word, idx)
            else:
                # print('not update')
                pass


    def check_word(self, word:str) -> bool:
        """word_dict_map 안에 해당 word가 존재하는지 체크하는 함수

        Args:
            word (str): 단어

        Returns:
            bool: True, False
        """
        if word in self.word_dict_map.keys():
            return True
        return False

class Algorithm:
    def __init__(self) -> None:
        pass
    
    
    

class TokenKiwi:
    def __init__(self, path) -> None:
        self.path = "C:/Users/user/Desktop/PinkWink_NLK_NLP_hackerthon/FINAL/data/word_dictionary.txt"
        self.kiwi = Kiwi(model_type='sbg')
        self.setting()

    def setting(self):
        self.kiwi.load_user_dictionary(self.path)
        self.kiwi.prepare()
        
    def reset(self):
        self.kiwi.load_user_dictionary(self.path)
        self.kiwi.prepare()
        
    def dictionary_add(self, data, morph:str = 'NNG', weight:int = 100, mode:str = 'a'):
        with open(self.path, mode=mode, encoding='utf8') as o:
            if isinstance(data, str):
                o.write(f'{data}\t{morph}\t{weight}\n')
            elif isinstance(data, list):
                for d in data:
                    o.write(f'{d}\t{morph}\t{weight}\n')
        self.setting()
    
    def lambda_kiwi_spacing(self, menu):
        result = self.kiwi.tokenize(menu)
        txt = []
        for token in result:
            if token.tag[0] == 'N':
                # print(f"{token.form}\t{token.tag}")
                txt.append(token.form)
        return ' '.join(txt)
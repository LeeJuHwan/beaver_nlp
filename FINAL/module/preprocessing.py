import numpy as np
import pandas as pd

import re
from collections import Counter
from tqdm import tqdm

from kiwipiepy import Kiwi


class PreProcessing:
    def __init__(self) -> None:
        self.option_words = ['추가', '없음', '있음', '변경', '포장', '매장' ,'없음', '배달비', '배달', '배달료', '초',
                             '테스트', '사이즈', '기본', '조금만', '많이', '나무젓가락' ,'리뷰']
    
    def text_clean(self, text):
        try:
            # pattern = r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)' # E-mail제거
            # text = re.sub(pattern, '', text)
            # pattern = r'(http|ftp|https)://(?:[-\w.]|(?:%[\da-fA-F]{2}))+' # URL제거
            # text = re.sub(pattern, '', text)
            # pattern = r'<[^>]*>'         # HTML 태그 제거
            # text = re.sub(pattern, '', text)
            
            # pattern = r'\([^)]*\)'
            # text = re.sub(pattern, '', text) # 괄호 제거
            
            # pattern = r'[0-9]'    # 숫자 -> 빈칸으로 대체
            # text = re.sub(pattern, ' ', text)
            
            pattern = r'[a-zA-Z]'    # 알파벳 제거
            text = re.sub(pattern, '', text)
            pattern = r'([ㄱ-ㅎㅏ-ㅣ]+)'  # 한글 자음, 모음 제거
            text = re.sub(pattern, '', text)
            pattern = r'[^\w\s]'         # 특수기호제거
            text = re.sub(pattern, '', text)
            text = text.strip(' ')
            text = text.strip('\n')
            return text
        except:
            return '에러'
    
    def lambda_option_menu(self, text):
        try:
            for word in self.option_words:
                if word in text:
                    return '옵션'
        except:
            print(text, type(text))
            return ""


class TokenKiwi:
    def __init__(self, path) -> None:
        self.path = r"C:\Users\user\Desktop\workbench\started_from_the_bottom\FINAL\data\word_dictionary.txt"
        self.kiwi = Kiwi(model_type='sbg')
        self.setting()

    def setting(self):
        self.kiwi.load_user_dictionary(self.path)
        self.kiwi.prepare()
        
    def reset(self):
        self.kiwi.load_user_dictionary(self.path)
        self.kiwi.prepare()
        
    def dictionary_add(self, data, morph:str = 'NNG', type:str = 'a'):
        with open(self.path, type, encoding='utf8') as o:
            if isinstance(data, str):
                o.write(f'{data}\t{morph}\t{3}\n')
            elif isinstance(data, list):
                for d in data:
                    o.write(f'{d}\t{morph}\t{3}\n')
        self.setting()
    
    def lambda_kiwi_spacing(self, menu):
        result = self.kiwi.tokenize(menu)
        txt = []
        for token in result:
            if token.tag[0] == 'N':
                # print(f"{token.form}\t{token.tag}")
                txt.append(token.form)
        return ' '.join(txt)
    
if __name__ == "__main__":
    preprocessing = PreProcessing()
    tokenkiwi = TokenKiwi()
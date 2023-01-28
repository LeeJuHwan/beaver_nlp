import pandas as pd 
from kiwipiepy import Kiwi
from module.jh import JH
import numpy as np
import re
import pickle

jh = JH()
with open(r"module/nnp_list.pkl", "rb") as r :
    nnp_list = pickle.load(r)

with open(r"module/WD.StandardDict.p", "rb") as r :
    StandradDict = pickle.load(r)

with open(r"module/WD.WordToStandard.p", "rb") as r :
    WordToStandard = pickle.load(r)

class Algorithm:
    def __init__(self) -> None:
        self.stop_words = ["정식","안주"] 
        self.option_list = ["추가","선택", "많이", "적게", "조금","빼고", "리필"]


    # stop words algorithm / Step 1 #
    def is_stop_words(self, stop_word_text:str, stop_words_param:list) -> str:
        """_summary_

        Args:
            stop_word_text (str): _description_
            stop_words_param (list): _description_

        Returns:
            str: _description_
        """
        result = jh.kiwi.space(stop_word_text).split(" ")
        for i in result :
            if i in stop_words_param :
                pat = re.compile(f"{i}")
                text = re.sub(pat, "", stop_word_text)
        return text.strip()
    # apply 선언 함수
    stop_words_func = lambda self, txt : self.is_stop_words(txt, self.stop_words)
    
    # option check algorithm / Step 2 #
    def is_option(self, option_text:str, option_li:list) ->str:
        """_summary_

        Args:
            option_text (str): _description_
            option_li (list): _description_

        Returns:
            str: _description_
        """
        result = jh.kiwi.space(option_text).split(" ")
        for i in result :
            if i in option_li :
                pat = re.compile(f"{i}")
                valiable = "".join(pat.findall(option_text))
                return " ".join(result), f"옵션 {valiable}"
    # apply 선언 함수
    option_func = lambda self, txt : self.is_option(txt, self.option_list)

    # special_character algorithm / Step 3 #
    def special_char(self, special_text:str) -> str: 
        """_summary_

        Args:
            special_text (str): _description_

        Returns:
            str: _description_
        """
        split_result = re.split(r"\+|\&|\/|\,", special_text)
        if len(split_result) >= 2 :
            combine_text = [split_result[split_result.index(i)].strip() for i in split_result]
            pattern = re.compile(r"[^\w\s]+")
            return [pattern.sub("", i ) for i in combine_text]
        else : 
            pattern = re.compile(r"[^\w\s]+")
            return jh.kiwi.space(pattern.sub("", special_text))

    # unit algorithm / Step 4 #
    extract_morph = lambda self, x : jh.morph(x)

    # space algorithm / Step 5 #
    spacing_text = lambda self, x : jh.kiwi.space(x)

    # remove_nnp/ Step 6 #
    def nnp_extract(self, text:str, nnp_list:list) -> str :
        """_summary_

        Args:
            text (str): _description_
            nnp_list (list): _description_

        Returns:
            str: _description_
        """
        res = []
        for i in text.split() :      
            if i not in nnp_list :
                res.append(i)
        return " ".join(res)

    nnp_remove = lambda self, x: self.nnp_extract(x, nnp_list)


    # std words / Step 7 #
    def word_standard(self,txt:str) -> str :
        """_summary_

        Args:
            txt (str): _description_

        Returns:
            str: _description_
        """
        res = []
        for word in txt.split(' '):
            try:
                res.append(WordToStandard[word])
            except :
                res.append(word)
        return " ".join(res)
        
    # data standard / Step 8 #
    def member_menu(self, txt:str) -> str :
        """_summary_

        Args:
            txt (str): _description_

        Returns:
            str: _description_
        """
        score_ls = []
        word_ls = txt.split(' ')
        for word in word_ls:
            try:
                score_ls.append(StandradDict[word]['mean'])
            except:
                score_ls.append(10)
        return word_ls[np.array(score_ls).argmax()], word_ls[np.array(score_ls).argmin()]
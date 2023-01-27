import numpy as np
import pandas as pd

import re
from collections import Counter, defaultdict
from functools import partial
from tqdm import tqdm

from kiwipiepy import Kiwi
from FINAL.module.preprocessing import TokenKiwi
from FINAL.module.tg import Dictionary


class JH:
    def __init__(self) -> None:
        kw = TokenKiwi('s')
        self.kiwi = kw.kiwi
        self.dic = Dictionary()

    def lambda_check_dict(self, txt):
        return self.check_dict(txt, self.dic.check_word(txt))


    def check_dict(self, text, func) :
            """
            파라미터(함수, 데이터프레임)
            함수 리턴 값이 True인 경우 괄호만 제거, False인 경우 괄호 포함 괄호 속 단어까지 제거
            """ 
            if func == True : 
                # print("if True")
                pat = re.compile(r"[\(|\)|\[|\]]")
                return re.sub(pat, "", str(text).lower())

            else :
                pat = re.compile(r"\([^)]*\)|\[[^)]*\]|\n")
                return re.sub(pat, "", str(text).lower())
            

    # 숫자 뒤에 의존명사가 아닌 다른 형태소가 오는 경우
    def morph(self, text) :
        result = self.kiwi.analyze(str(text).lower()) 
        for i in range(len(result[0][0])) : 
            if len([index.form for index in result[0][0] if index.tag == "SN"]) == 0 :
                return str(text), ""
            
            if (result[0][0][-1].tag == "SN") and (len([index.form for index in result[0][0] if index.tag == "SN"]) < 2):
                last_sn = result[0][0][-1].form
                front_position_morph = result[0][0][0].form
                
                if front_position_morph == last_sn :
                    pat = re.compile(rf"[{last_sn}]")
                    return (re.sub(pat, "", str(text)), "")
                
                else :
                    front_position_morph2 = result[0][0][-2].form
                    pat = re.compile(rf"[{front_position_morph2}]+[{last_sn}]+")
                    return (re.sub(pat, "", str(text)), "")

            else  : # 2개 이상이거나 인덱스 중간 중간에 숫자가 위치 해 있는 경우
                if (result[0][0][i].tag == "SN") :
                    if (result[0][0][i+1].tag == "NNB") : # 숫자 뒤에 의존명사가 오는 경우
                        true_sn = result[0][0][i].form 
                        nnb = result[0][0][i+1].form 
                        pat = re.compile(rf"({true_sn}+{nnb})")
                        word = pat.findall(text.lower())
                        first_result = re.sub(pat, "", text.lower())
                        if len([j for j in result[0][0][i+1:] if j.tag == "SN"]) >= 1 :
                            none_list = lambda x : x[0]
                            true_sn2, nnb2 = none_list([(k.form, result[0][0][i+1:][h+1].form) for h,k in enumerate(result[0][0][i+1:]) if k.tag == "SN"])
                            pat2 = re.compile(rf"({true_sn2}+{nnb2})")
                            word.append("".join(pat2.findall(first_result.lower())))
                            second_result = re.sub(pat2, "", first_result.lower())
                            return (second_result, word)
                        return (first_result, word)
                    
                    else :  # 숫자 뒤에 의존명사가 아닌 다른 형태소가 오는 경우
                        false_sn = result[0][0][i].form
                        another = result[0][0][i+1].form 
                        if result[0][0][i+1].len < 5 : # 숫자 뒤에 오는 다른 형태소 길이가 5글자 미만인 경우 전체 제거
                            else_pat = re.compile(rf"([{false_sn}]+[{another}]+|[{false_sn}]+ [{another}]+)")
                            result_word = re.sub(else_pat, "", text.lower())
                            if len([j for j in result[0][0][i+1:] if j.tag == "SN"]) >= 1 :
                                none_list = lambda x : x[0]
                                false_sn2, another2, another_tag = none_list([(k.form, result[0][0][i+1:][h+1].form, result[0][0][i+1:][h+1].tag) for h,k in enumerate(result[0][0][i+1:]) if k.tag == "SN"])
                                if another_tag == "NNB" :
                                    else_pat2 = re.compile(rf"([{false_sn2}]+[{another2}]+|[{false_sn2}]+ [{another2}]+)")
                                    result_word2 = re.sub(else_pat2, "", result_word.lower())
                                    find_word =  else_pat2.findall(result_word.lower())
                                    return (result_word2, find_word)
                                else :
                                    else_pat3 = re.compile(rf"([{false_sn2}]+[{another2}]+|[{false_sn2}]+ [{another2}]+)")
                                    result_word3 = re.sub(else_pat3, "", result_word.lower())
                                    return (result_word3, "")
                            return (result_word, "")
                        else : # 5글자 이상인 경우는 숫자만 제거(아메리카노 처럼 의미 있는 단어 일 확률이 높음)
                            pat = re.compile(rf"({false_sn}+|[{false_sn}]+ )")
                            return (re.sub(pat, "", text.lower()), "")
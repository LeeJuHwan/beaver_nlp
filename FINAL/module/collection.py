import requests
import time
import pandas as pd
from tqdm import tqdm


import warnings
warnings.filterwarnings('ignore')


class Crawling :
    def __init__(self, client_id, client_secret) :
        self.dic = {}
        self.client_id = 'IxoDXd61MLLXilnc4isn'
        self.client_secret = 'cOI0sLIbAF'
    
    def running(self, datas):
        for i in tqdm(datas) :
            try : 
                self.search(i)
            except : 
                self.dic[i] = None
        self.fix_errors()
    
    def search(self, query) :
        naver_open_api = f"https://openapi.naver.com/v1/search/local.json?query={query}"
        header_params = {"X-Naver-Client-Id":self.client_id, "X-Naver-Client-Secret":self.client_secret}
        res = requests.get(naver_open_api, headers=header_params)

        data = res.json()
        if data["items"] :
            self.dic[query] = data["items"][0]["category"]
            time.sleep(0.4)
            return self.dic
        else :
            self.dic[query] = "error"
            pass
    
    # 예외처리 된 내용 중 검색이 가능한 데이터였지만 다른 에러로 예외 됐을 때를 대비 하여 수정하는 로직 작성
    def fix_errors(self) :
        for key, value in tqdm(self.dic.items()) :
            if value == "error" :
                query2 = key
                naver_open_api = f"https://openapi.naver.com/v1/search/local.json?query={query2}"
                header_params = {"X-Naver-Client-Id":self.client_id, "X-Naver-Client-Secret":self.client_secret}
                res2 = requests.get(naver_open_api, headers=header_params)
                data2 = res2.json()
                
                try : 
                    time.sleep(0.5)
                    self.dic[key] = data2["items"][0]["category"]
                except :
                    self.dic[key] = "None"
        return self.dic
    
if __name__ == "__main__":
    crawling = Crawling()
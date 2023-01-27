import numpy as np
import pandas as pd

import re
from collections import Counter, defaultdict
from functools import partial
from tqdm import tqdm

from module.collection import Crawling

class ss:
    def __init__(self) -> None:
        pass
    
    def process(self, df:pd.DataFrame, train:bool) -> pd.DataFrame:
        if train:
            df.columns = ['STORE', 'MENU', 'PRICE', 'STANDARD']
        else:
            df.columns = ['STORE', 'MENU', 'PRICE']
            df['STANDARD'] = np.NaN
        
        df['PRICE'] = df['PRICE'].apply(self.lambda_price_str_to_int).astype(int)
        
        client_id = 'IxoDXd61MLLXilnc4isn'
        client_secret = 'cOI0sLIbAF'
        df = self.store_to_sector(df, client_id, client_secret)
        return df
    
    def lambda_price_str_to_int(self, price:str) -> str:
        """ 2,000 -> 2000

        Args:
            price (str): price

        Returns:
            int: price
        """
        pattern = r'([^0-9])+'
        price = re.sub(pattern, '', price)
        return price
    
    def store_to_sector(self, df:pd.DataFrame, client_id:str, client_secret:str) -> pd.DataFrame:
        """스타벅스 -> 커피

        Args:
            df (pd.DataFrame): df.columns = ['STORE', 'MENU', 'PRICE']
            client_id (str): naver_client_id
            client_secret (str): naver_client_secret

        Returns:
            pd.DataFrame: _description_
        """
        print('store_to_sector')
        crawling = Crawling(client_id, client_secret)
        storeList = df['STORE'].unique().tolist()
        crawling.running(storeList)
        df['Sector'] = df['STORE'].map(crawling.dic)
        df = self.crawling_to_sector(df)
        return df
        
    def crawling_to_sector(self, df:pd.DataFrame) -> pd.DataFrame:
        """_summary_

        Args:
            df (pd.DataFrame): df.columns = ['STORE', 'MENU', 'PRICE', 'Sector']

        Returns:
            pd.DataFrame: df.columns = ['STORE', 'MENU', 'PRICE', 'SECTOR']
        """
        print('crawling_to_sector')
        ls = []
        for sectors in df['Sector'].unique():
            for sector in sectors.split(','):
                if '음식점' in sector:
                    t = sector.split('>')
                    ls.append(t[t.index('음식점') + 1])

        sectorsList = []
        for sectors in df['Sector'].unique():
            for sector in sectors.split(','):
                sectorsList.append(sector)

        ls = set(ls)
        sector_dict = defaultdict(list)
        for sector in set(sectorsList):
            for l in ls:
                if l in sector:
                    sector_dict[sector].append(l)
                    break
            if not sector_dict[sector]:
                sector_dict[sector].append(sector.split('>')[0])

        k = []
        for sectors in df['Sector']:
            kk = []
            for sector in sectors.split(','):
                kk.append(sector_dict[sector])
            k.append(kk[0][0])
            
        df['SECTOR'] = k
        del df['Sector']
        
        return df
    
class Dictionary:
    standard_dict = defaultdict(set)
    standard_dict_map = {}
    
    stop_words = []
    
    word_dict = defaultdict(set)
    word_dict_map = {}
    
    category_dict = defaultdict(set)
    option_dict = defaultdict(set)
    forbidden_dict = defaultdict(set)
    
    def __init__(self) -> None:
        pass
    
    def __del__(self):
        # 파일로 저장
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

# if __name__ == "__main__":
#     preprocessing = PreProcessing()
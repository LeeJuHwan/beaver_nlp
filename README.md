# 비버웍스 키오스크 음식 메뉴 표준화 해커톤

#### 1.27 ~ 1.29

#### 팀원 

|이름|협업|깃허브|
|:---|:---:|:---:|
|김택관|최초 사전 구축 알고리즘 구현, 단어간 유사도 및 우선 순위 알고리즘 구현|https://github.com/KimTaekGwan|
|이주환|전처리 알고리즘 구현, 불용어 데이터, 옵션 데이터, 고유명사 데이터 수집|https://github.com/LeeJuHwan|

---
<img width="1201" alt="image" src="https://user-images.githubusercontent.com/118493627/215301191-933f308b-7798-40a9-b6b7-30e3092c433d.png">

## Process 
<img width="972" alt="image" src="https://user-images.githubusercontent.com/118493627/215301223-9cf0a09f-9f58-460b-8c50-352b95ecbf28.png">

### Model Algorithm
<img width="1155" alt="image" src="https://user-images.githubusercontent.com/118493627/215301272-36692d0a-1909-4c74-afdc-733ae038823f.png">

#### Architecture
<img width="1137" alt="image" src="https://user-images.githubusercontent.com/118493627/215301305-fdc9548e-00b8-4c83-9965-22256afed9d4.png">

### principle
<img width="534" alt="image" src="https://user-images.githubusercontent.com/118493627/215302502-304a8cf6-0ea8-4ce6-ace2-9ac4178414ba.png">

#### Algorithm to function
```
algo = Algorithm()

def preprocessing(text) :
    res = {'메뉴':None, '맛/재료':None, 
        '단위':None, '세트/옵션':None}

    x = algo.bascket_remove(text)
    x = algo.stop_words_func(x)
    x = algo.bascket_remove(x)
    x = algo.option_func(x)
    if x[-1] :
        res["세트/옵션"] = "옵션"
        res["메뉴"] = x[0]
        return {"menu" : x,
                "std" : res}
        
    x = algo.special_char(x[0]) 
    if type(x) == list  : 
        res["세트/옵션"] = "세트"
        return {"menu" : " ".join(x),
                "std" : res}
    rs = jh.morph(x)
    try : 
        if rs[-1] :
            res["단위"] = "".join(rs[-1]) 
        x = algo.spacing_text(rs[0])
    except TypeError as e:
        pass

    x = algo.nnp_remove(x)
    x = algo.word_standard(x)
    output = algo.member_menu(x)
    res["맛/재료"] = ",".join(output[0]); res["메뉴"] = output[1]

    token_result = jh.kiwi.tokenize(x)
    ls = [i.form for i in token_result if i.tag[0] == "N"]
    return {"menu" : " ".join(ls),
            "std" : res}
```
- return 

<img width="1044" alt="image" src="https://user-images.githubusercontent.com/118493627/215302573-422ceb2b-63db-484a-971b-be66fa4105b1.png">


### Keyword
- 사용자 사전 포맷

- 형태소 분석을 통한 알고리즘 구현

- 단어의 우선 순위

### TIL
> 트라이(Trie) 구조

- 문자열을 저장하고 효율적으로 탐색하기 위한 트리 형태의 자료구조

- 자동완성 기능, 사전 검색 등 문자열을 탐색하는데 특화되어있는 자료구조

- 래딕스 트리(radix tree) or 접두사 트리(prefix tree) or 탐색 트리(retrieval tree)라고도 한다. 트라이는 retrieval tree에서 나온 단어


<img width="650" alt="image" src="https://user-images.githubusercontent.com/118493627/215302131-f9d726e0-dd02-43af-a40d-40f6be55e812.png">


### 해커톤 수료

<img width="200" height = "150" alt="image" src="https://user-images.githubusercontent.com/118493627/215800235-edca3fd7-6886-4287-be5e-3901c18d6529.png">



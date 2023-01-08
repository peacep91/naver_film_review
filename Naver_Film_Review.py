#pip install beautifulsoup4
#참고자료: https://hyemin-kim.github.io/2020/08/29/E-Python-TextMining-2/
#참고자료: https://wikidocs.net/172863

import random
import numpy as np
import pandas as pd
import requests
import time
from bs4 import BeautifulSoup


comment_list = []
#header ={"User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36"}
for code in [74977, 62266]:

    for no in range(1, 2):
        url = 'https://movie.naver.com/movie/point/af/list.naver?st=mcode&sword=' + str(code)+'&page=%d' % no
        r = requests.get(url)
        bs = BeautifulSoup(r.text, "lxml")

        trs = bs.select("table.list_netizen > tbody > tr")
        #print(trs)

        for tr in trs:
            tds = tr.select("td")
            if len(tds) == 3:
                number = tds[0]
                review_number = number.text
                title = tds[1]
                movie_title = title.select_one("a.movie").text
                point = title.select_one("div.list_netizen_score > em").text
                for a in title.select("a"):
                    a.decompose()
                title.select_one("div").decompose()
                review = title.text.strip()
                #print(movie_title, point, review, sep="\t")
                comment_list.append((movie_title, review_number, point, review))
                #print(comment_list)
                interval = round(random.uniform(0.2, 1.2), 2)
                time.sleep(interval)

df = pd.DataFrame(comment_list,
                  columns=['MovieTitle', 'Review_Number', 'Point', 'Review'])
df = df.apply(lambda x: x.str.strip()).replace('', np.nan)
df = df[df.Review.notnull()]

from konlpy.tag import Okt
from collections import Counter

import re
# def apply_reqular_expression(text):
#     hangul = re.compile('[^ ㄱ-ㅣ 가-힣]')
#     result = hangul.sub('',text)
#     return result

okt = Okt()

df['Tokenized'] = df['Review'].apply(okt.nouns)


df = pd.DataFrame(df, columns = ['MovieTitle', 'Review_Number', 'Point', 'Review', 'Tokenized']).explode('Tokenized', ignore_index=True)



# counter = Counter(nouns)
# available_counter = Counter({x: counter[x] for x in counter if len(x) > 1})

# df2 = pd.DataFrame.from_dict(available_counter, orient='index').reset_index()
# print(df2)

#태블로 테이블익스텐션에서 추가
#return df.to_dict(orient='list')






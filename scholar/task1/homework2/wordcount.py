with open('curpos.txt','r',encoding='utf-8') as file:
    content=file.read()
result=''
content=content.lower()
for char in content:
    if 'a'<=char<='z' or '0'<=char<='9' or char==' ':
        result+=char

with open('stopwords.txt','r',encoding='utf-8') as ban:
    banwords=ban.read()
result_ban=''
banwords=banwords.lower()
for char in banwords:
    if 'a'<=char<='z' or '0'<=char<='9' or char==' ':
        result_ban+=char

def my_split(text):
    words=[]
    s=''
    for char in text:
        if char==' ':
            if s!='':
                words.append(s)
                s=''
        else:
            s+=char
    if s!='':
        words.append(s)
    return words

def freq_count(words):
    freq={}
    for word in words:
        if word in freq:
            freq[word]+=1
        else:
            freq[word]=1
    return freq

def quick_sort(lst):
    if len(lst)<=1:
        return lst
    mid=lst[len(lst)//2]
    left=[]
    mid_list=[]
    right=[]
    for x in lst:
        if x[1]>mid[1]:
            left.append(x)
        elif x[1]<mid[1]:
            right.append(x)
        else:
            mid_list.append(x)
    return quick_sort(left)+mid_list+quick_sort(right)

def quick_sort_dict(dict):
    words=list(dict.items())
    res=quick_sort(words)
    return res

def pure_dict(stopwords,dict):
    for word in stopwords:
        if word in dict:
            del dict[word]
    return dict

def bigram_count(words):
    bigrams=[]
    for i in range(len(words)-1):
        bigram=words[i]+' '+words[i+1]
        bigrams.append(bigram)
    freq={}
    for bigram in bigrams:
        if bigram in freq:
            freq[bigram]+=1
        else:
            freq[bigram]=1
    return freq

if __name__=='__main__':
    words=my_split(result)
    stopwords=my_split(result_ban)
    freq=freq_count(words)
    sorted_freq=quick_sort_dict(freq)
    print("词频前20：")
    for word,count in sorted_freq[:20]:
        print(f"{word}: {count}")
    freq=pure_dict(stopwords,freq)
    sorted_pure=quick_sort_dict(freq)
    print("\n纯净词频前20：")
    for word,count in sorted_pure[:20]:
        print(f"{word}: {count}")
    print("\n二元词组频率前10：")
    bigram_freq=bigram_count(words)
    sorted_bigrams=quick_sort_dict(bigram_freq)
    for bigram,count in sorted_bigrams[:10]:
        print(f"{bigram}: {count}")
    with open('resultt.csv','w',encoding='utf-8') as f:
        for word,count in sorted_freq:
            f.write(f"{word}:{count}\n")
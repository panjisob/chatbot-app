import requests as req

from nltk.chunk import conlltags2tree, tree2conlltags
from nltk import word_tokenize,ne_chunk, pos_tag

def check(a):
        ne_tree = ne_chunk(pos_tag(word_tokenize(a)))
        
        iob_tagged = tree2conlltags(ne_tree)
        print (iob_tagged)
        for x in iob_tagged:
                if x[1] == "CD":
                        return x[0]

tgl = check("gue pesan 2019/10/09 kosong gaj")
a = tgl.replace("/","-")
z = "http://127.0.0.1:5000/cek_jadwal/"+a
print(req)
resp = req.get(z).json()

try:
    print(resp["data"][0])
except :
    print('error ')


# if len(resp["data"][0])==0:
#     print("kosong")
# else:
#     print("ada")
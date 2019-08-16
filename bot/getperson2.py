# from nltk.chunk import conlltags2tree, tree2conlltags
# from nltk import word_tokenize,ne_chunk, pos_tag

# def response(a):
#         ne_tree = ne_chunk(pos_tag(word_tokenize(a)))

#         iob_tagged = tree2conlltags(ne_tree)
#         print (iob_tagged)
#         for x in iob_tagged:
#                 if x[1] == "NNP":
#                         print(x[0])

# response("nama saya adalah Panji Sobari Soeriawidjaya | alamat saya adalah jl.baguntapan | email saya adalah")

def extract_number(documents):
        res = [int(i) for i in test_string.split() if i.isdigit()]
        return res
  
# print result 
test_string = "There are 2 apples for 4 persons"
res = extract_number(test_string)
print("The numbers list is : " + str(res[0]))
import re
import nltk
from nltk.corpus import stopwords
stop = stopwords.words('indonesia')

string = """
Hey,
This week has been crazy. Attached is my report on IBM. Can you give it a quick read and provide some feedback.
Also, make sure you reach out to Claire (panji.sobari@xyz.com).
You're the best.
Cheers,
Panji Sobari Soeriawidjaya
212-555-1234
"""

s = "Nama saya adalah Panji Sobari Soeriawidjaya"
n = "Nomor hp saya adalah 08990834799"
e = "email saya adalah panjisob@mail.com"

def extract_phone_numbers(string):
    r = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
    phone_numbers = r.findall(string)
    return [re.sub(r'\D', '', number) for number in phone_numbers]

def extract_email_addresses(string):
    r = re.compile(r'[\w\.-]+@[\w\.-]+')
    return r.findall(string)

def ie_preprocess(document):
    document = ' '.join([i for i in document.split() if i not in stop])
    sentences = nltk.sent_tokenize(document)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    print(sentences)
    return sentences

def extract_names(document):
    names = []
    sentences = ie_preprocess(document)
    # sentences = document
    for tagged_sentence in sentences:
        for chunk in nltk.ne_chunk(tagged_sentence):
            if type(chunk) == nltk.tree.Tree:
                if chunk.label() == 'PERSON':
                    names.append(' '.join([c[0] for c in chunk]))
    return names

if __name__ == '__main__':
    numbers = extract_phone_numbers(n)
    emails = extract_email_addresses(e)
    names = extract_names(s)

    nama = extract_names(s)

    print(numbers)
    print(emails)
    print(names)
    # print(nama)
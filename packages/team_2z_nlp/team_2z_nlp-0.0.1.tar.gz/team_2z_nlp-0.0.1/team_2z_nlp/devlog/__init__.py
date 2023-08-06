from konlpy.tag import Okt
from nltk.tag import pos_tag

okt = Okt()
result = []



def pos(text):
    alpha_list = []
    sentence = okt.pos(text, norm=True, stem=True)
    print(sentence)
    for morp in sentence:
        if morp[1] == 'Alpha':
            alpha_list.append(morp[0])
        elif morp[1] == 'Noun':
            result.append(morp[0])

    print(alpha_list)
    tagged = pos_tag(alpha_list)
    print(tagged)
    return result

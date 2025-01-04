# text = "article 1 machine learning"
# print(text[0:7])
# print(text[text.find(text.split(" ")[2]):])

def split_topic(articles):
    topics = list()
    art = list()
    for idx, item in enumerate(articles):
        if item[0:7] == "article" and articles[idx+1] !="article":
            topics.append(item[item.find(item.split(" ")[2]):])
            art.append(articles[idx+1])
    return topics, art

lst = ['article 1 machine learning', 'machine learning field artificial intelligence that uses statistical techniques give computers ability learn from data it widely used various domains including healthcare finance marketing', '', 'article 2 natural language processing', 'natural language processing nlp subfield artificial intelligence that deals with interaction between computers humans using natural language applications include text analysis translation chatbots', '', 'article 3 generative ai', 'generative ai refers algorithms such as gpt4 that can generate new content like text images videos it plays significant role modern ai applications including creative writing design', '', 'article 3 python', 'it slow language but widely used']

topics, articles = split_topic(lst)
print(topics)
print(articles)
import requests

# NOTE incomplete
# TODO figure out why 400


def insult(text):
    url = "https://7006.lnsigo.mipt.ru/answer"
    r = requests.session()
    r.options(url)
    headers = {"Content-Type": "application/json",
               "Origin": "https://demo.ipavlov.ai",
               "Referer": "https://demo.ipavlov.ai/"}
    data = {"text1": text, "text2": None}
    a = r.post(url, data, headers=headers)
    print(a.text)
    return a.json()


def odqa(text):
    url = "https://7011.lnsigo.mipt.ru/answer"
    r = requests.session()
    r.options(url)
    headers = {"Content-Type": "application/json",
               "Referer": "https://demo.ipavlov.ai/"}
    data = {"text1": text, "text2": None}
    a = r.post(url, data, headers=headers)
    print(a.text)
    return a.json()


def textqa(corpus, question):
    url = "https://7008.lnsigo.mipt.ru/answer"
    r = requests.session()
    r.options(url)
    headers = {"Content-Type": "application/json",
               "Referer": "https://demo.ipavlov.ai/"}
    data = {"text1": corpus, "text2": question}
    a = r.post(url, data, headers=headers)
    return a.json()


if __name__ == "__main__":
    #print(odqa("Who piloted the original Gundam?"))
    print(insult("go fuck yourself"))

import requests
from bs4 import BeautifulSoup
import telebot  # pyTelegramBotAPI library

bot_token = 'pasteTokenHere'
chat_tag = 'pasteChannelTagHere'
msg = 'join @pvxtechnews for daily tech news!'
# variables={"lastNews":"Google at Odds With US Over Protective Order for Firms Tied to Lawsuit"}

lastNews = variables["lastNews"]
# lastNews = ["47% find WhatsApp's updated privacy policy unacceptable: Inshorts poll", "Army officer develops 'microcopter' for tracking terrorists inside buildings",'Intel CEO Bob Swan to step down in Feb, VMware CEO to replace him: Report', 'TikTok to make accounts private by default for users aged under 16', "As promised: Elon Musk on Tesla's India entry",'Parler may not return, hard to keep track of people cutting ties with us: CEO', "Deeply sorry for below-quality 'Cyberpunk 2077': CD Projekt Co-founder", "Bengaluru world's fastest growing tech hub, Mumbai 6th: Report", "Aakash Educational confirms it is in talks with BYJU'S for reported $1 bn deal"]
NewNews = []


def ndtv():
    global NewNews
    print("Getting news from gadgets ndtv!")
    url = 'https://gadgets.ndtv.com/news'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    headings = soup.findAll(class_='news_listing')
    List = []
    count = 0  # to get only top 14 news
    for heading in headings:
        count = count+1

        if count >= 14:
            break
        # if count==11:
            # List.append("\n\n🌐 Join @pvxtechnews for daily tech news !")

        List.append("\n\n🌐")
        headline = heading.text

        # cropping headings having this text in the end
        if headline[-23:] == ": Price, Specifications":
            heading = headline[:-23]

        List.append(headline)

    NewNews = lastNews
    return List


def getNews():
    print("Getting news from news-api!")
    global NewNews
    url = 'http://news-pvx.herokuapp.com'
    page = requests.get(url)
    dict = eval(page.text)

    List = []
    count = 0  # to get only top 14 news
    for heading in dict["inshorts"]:
        if heading[-1] == '?':
            continue

        if heading in lastNews:
            continue

        count += 1
        if count >= 14:
            break
        # if count==11:
            # List.append("\n\n🌐 Join @pvxtechnews for daily tech news !")
        List.append("\n\n🌐")

        List.append(heading)
        NewNews.append(heading)

    if count >= 10:
        return List
    else:
        print("\nNOT ENOUGH NEW NEWS IN INSHORTS !!!\nTRYING NDTV GADGETS!\n\n")
        return ndtv()


bot = telebot.TeleBot(token=bot_token)

List = getNews()
List.insert(0, '☆☆☆☆☆💥 Tech News 💥☆☆☆☆☆')
# print(List)

variables["lastNews"] = NewNews
# print(lastNews)

List.append("\n\n"+msg)

text = " ".join(List)
# print(text)

try:
    bot.send_message(chat_tag, text)
    print("\nTECH NEWS POSTED :) !!")
except:
    print("\nSOMETHING IS WRONG ! PROPBABLY TOKEN OR CHAT ID IS NOT RIGHT")

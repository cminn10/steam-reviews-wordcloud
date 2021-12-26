#Libraries used: urllib, bs4, wordcloud, matplotlib

import sys
from bs4 import BeautifulSoup
from urllib.request import urlopen
cloudPicSave = './steam/'
stopWordsPath = './stopwords.txt'

#The following code came from 'https://stackoverflow.com/questions/32442608/ucs-2-codec-cant-encode-characters-in-position-1050-1050'
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
#End of code from 'https://stackoverflow.com/questions/32442608/ucs-2-codec-cant-encode-characters-in-position-1050-1050'

#A function to convert the user-input title to match the format of the urls


def titleConvert(title, use):
    title = title.split(' ')
    #The search result page's url connects each word with '+'
    titleSearch = '+'.join(title).lower()
    #The url of the review page on Steam Community connects each word with '_'
    titleComment = '_'.join(title).lower()
    if use == 'search':
        return titleSearch
    if use == 'comment':
        return titleComment


#The 1st layer of loop:
while True:
    #The 2nd layer of loop: 1. locating the game's review page on Steam Community 2. Extract the comments
    while True:
        #The 3rd layer of loop: searching for the game
        while True:
            gameTitle = input('What\'s the game?\n>>')
            gameTitle2 = titleConvert(gameTitle, 'search')
            print('Searching...')
            #Example search result page's url: 'https://store.steampowered.com/search/?term=valkyria+chronicles'
            url = 'https://store.steampowered.com/search/?term={}'.format(
                gameTitle2)
            try:
                searchPage = urlopen(url)
                break
            except Exception:
                print(
                    'Something went wrong. Please try checking your Internet connection.')

        soup = BeautifulSoup(searchPage, 'html.parser')
        links = soup.find_all('a')
        gameTitle3 = titleConvert(gameTitle, 'comment')
        gamePages = []
        for each in links:
            link = each['href']
            if 'https://store.steampowered.com/app/' in link and gameTitle3 in link.lower():
                gamePages.append(link)
        if gamePages == []:
            print('Sorry, we cannot find the game you\'re looking for.')
        else:
            gameId = gamePages[0].split('/')[4]
            break

    commentList = []
    '''
    The below loop is to locate each page of comments.
    The comment page on Steam Community applies swipe-down-loading. Each time the user swipes down on the bottom of the page,
    the page loads 10 more comments. The swipe-down does not change the url. The urls of different pages were found in:
    [Chrome--Inspect--Network--XHR and Fetch]
    '''
    for i in range(1, 11):  # The range determines the pages. A range of (1, 11) returns from the 1st page to the 10th page.
        commentUrl = 'https://steamcommunity.com/app/{}\
    /homecontent/?userreviewsoffset={}&p={}&workshopitemspage={}&readytouseitemspage={}\
    &mtxitemspage={}&itemspage={}&screenshotspage={}&videospage={}&artpage={}&allguidepage={}\
    &webguidepage={}&integratedguidepage={}&discussionspage={}\
    &numperpage=10&browsefilter=trendweek&browsefilter=trendweek&appid={}\
    &appHubSubSection=10&appHubSubSection=10&l=english&filterLanguage=default&searchText=&forceanon=1'.format(gameId, i*10, (i+1), (i+1), (i+1), (i+1), (i+1), (i+1), (i+1), (i+1), (i+1), (i+1), (i+1), (i+1), gameId)
        commentUrl = commentUrl.replace(' ', '')
        commentPage = urlopen(commentUrl)
        comSoup = BeautifulSoup(commentPage, 'html.parser')
        reviewCards = comSoup.find_all('div', {'class': 'apphub_Card'})

        for eachrev in reviewCards:
            comment = eachrev.find(
                'div', {'class': 'apphub_CardTextContent'}).get_text()
            #The original comment text block includes 'Date posted' and other info. The below code is to extract only the comment.
            #No_bmp_map is used to transfer emoji characters
            comment = comment.translate(non_bmp_map).split('\n')[2]
            #Comment text processing: the original comment text includes chunks of spaces. The below code is to clean the text.
            comment = comment.strip('\t').strip(' ').strip('\n')
            commentList.append(comment)

    from wordcloud import WordCloud
    import matplotlib.pyplot as plt

    #The stopwords contains universal stopwords and some words frequently appear in game reviews, like "play", "characters", "good", etc.
    with open(stopWordsPath, 'r') as stpw:
        wordset = set()
        for i in stpw:
            word = i.strip('\n')
            wordset.add(word)
    text = ' '.join(commentList)
    wordcloud = WordCloud(width=800, height=600,
                          stopwords=wordset).generate(text)
    ifsave = input('Word cloud generated! \
    Do you want your cloud to be shown now or downloaded to your computer? \
    S to show, D to download\n>>').lower()
    if ifsave == 's':
        plt.imshow(wordcloud)
        plt.axis('off')
        plt.show()
        input('Press any key to close.')
        plt.close()
    if ifsave == 'd' and ifsave != 's':
        wordcloud.to_file(cloudPicSave+'comments.jpg')
        print('Downloaded!')

    anotherGame = input(
        'Press Enter to search for another game. Press E to exit\n>>')
    if anotherGame.lower() == 'e':
        break

Steam Games Review-evaluation Tool

Program Design:
Most video game players should once question that how I could know if a minor independent game suits my taste without taking time to go through different passages of long reviews. Hence, as one of the players, I built a tool that can show a visualized overview of a certain game that contains most frequent keywords in comments. 
For now, Steam is the largest digital distribution platform for purchasing and playing video games. The Steam Community masses the world’s biggest group of PC game players that continuously contribute new reviews and short comments on games every day. So, I based my tool on the Steam Community.

How it works:
The user inputs the title of the game he/she is searching for. With no case sensitivity, the tool will locate the game whose title contains all words that the user entered. Then the tool will crawl the first 100 comments and generate a simple word cloud based on the comments crawled. (The parameter of the number of comments can be adjusted. For speed and efficiency, here I set it to 100.) The user has an option to show the word cloud picture once or save it to his/her computer. Once done this step, the user has an option to continue to search for another game or exit the tool.

Attachment:
[stopwords.txt]
A set of stop words containing the universal stop words and some additional frequent words in game reviews.

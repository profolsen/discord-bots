# discord-bots
some useful bots for discord.
I relied on many tutorials, this one was particularly useful in getting me started:
https://discordpy.readthedocs.io/en/stable/quickstart.html

##Florence (/bots/florence/florence.py)
A bot for some basic event logging and reporting
###Recognized Messages
+ `update category [word [words]]` Send an update.  Words are important aspects of the event being logged.
+ `report daily category days [word [words]]` Request daily averages for the events that are in category and are sub-labeled with words.
+ `report diff cause effect` Gets a histogram for each hour after an event of category cause and the number of events of category effect that happen within a given number of hours of cause.
+ `report now` diagnostic value. Reports the sum of the number of times each category and word appear in the table of events.

###Further goals of the project:
+ get the bot to send csv files of results of reports
+ get the bot to send images of plots of reports

##Simon Says (/bots/simon-says/simon-says.py)
An echo bot

###Recognized messages
+ `$Simon says` responds with whatever is after simon-says.

###Further goals of the project
+ None. This was the first bot I sort of wrote "myself" (compare with tutorial code).

##Further bots to be developed:
+ Yes.

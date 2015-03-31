import csv
import os

import praw
from imgurlink import ImgurLink

username = '' #enter your own user name
password = '' #enter your own password
subreddit = '' #enter your own subreddit

magic_word = '%s, post:' % username

r = praw.Reddit(user_agent='imgur bot')
r.login(username, password)

s = r.get_subreddit(subreddit)

def levenshtein(seq1, seq2):
    oneago = None
    thisrow = range(1, len(seq2) + 1) + [0]
    for x in xrange(len(seq1)):
        twoago, oneago, thisrow = oneago, thisrow, [0] * len(seq2) + [x + 1]
        for y in xrange(len(seq2)):
            delcost = oneago[y] + 1
            addcost = thisrow[y - 1] + 1
            subcost = oneago[y - 1] + (seq1[x] != seq2[y])
            thisrow[y] = min(delcost, addcost, subcost)
    return thisrow[len(seq2) - 1]
	
def string_or_unicode(possible_string):
    if (isinstance(possible_string, unicode)):
        return possible_string.encode('utf-8')
    else:
        return possible_string

previously_found = []
with open('readFile.csv', 'rb') as f:
    l = csv.reader(f)
    for line in l:
        previously_found = previously_found + line


#change list to set to improve search to O(1)
comments = []
submissions = s.get_hot(limit = 100)
for submission in submissions:
    submission.replace_more_comments(limit = None, threshold = 0)
    flat_comments = praw.helpers.flatten_tree(submission.comments)
    comments = comments + [comment for comment in flat_comments if hasattr(comment, 'body') and comment.id not in previously_found]
		
imgur = ImgurLink()
for comment in comments:
    request_list = str.split(string_or_unicode(comment.body),':')
    #check if request does not contain colons
    if levenshtein(magic_word, request_list[0]) < 5:
        imgur_result = imgur.return_link(request_list[1])
		#catch error if list is empty since content does not exist in imgur
        comment.reply(imgur_result)
    previously_found.append(string_or_unicode(comment.id))
	
	
with open("writeFile.csv",'wb') as cw:
    a = csv.writer(cw)
    a.writerow(previously_found)

	
os.remove('readFile.csv')
os.rename('writeFile.csv', 'readFile.csv')

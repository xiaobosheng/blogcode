# -*- coding: utf-8 -*-

import praw
from pync import Notifier
import time


class RedditBot(object):
    #Initialize Reddit object
    def __init__(self, username, password, subreddits):
        self.username = username
        self.password = password
        self.post_ids = {}
        self.sub_reddit = subreddits
        self.r = praw.Reddit(user_agent='User-Agent: reddit bot by /u/xiaobosheng')

    #Login
    def login(self):
        self.r.login(self.username, self.password)

    def init_ids(self):
        print('init ids')
        for sub in self.sub_reddit:
            init_post = self.get_new_post(sub)
            self.post_ids[sub] = init_post.id
        print self.post_ids

    #Get new post from subreddit, return post ids
    def get_new_post(self, subreddit):
        posts = self.r.get_subreddit(subreddit).get_new(limit=1)
        print 'getting new post id'
        return next(posts)

    def sync(self):
        while True:
            #Check back in 30 mins
            time.sleep(1800)
            for sub in self.sub_reddit:
                new_post = self.get_new_post(sub)
                print("new post id {}".format(new_post.id))
                if new_post.id != self.post_ids[sub]:
                    self.post_ids[sub] = new_post.id
                    Notifier.notify(new_post.title, title='New post on /r/'+sub, open='http://www.reddit.com/r/'+sub+'/new/')



if __name__ == '__main__':
    #Put in your favorite subreddits in a list
    bot = RedditBot('username', 'password', ['python', 'learnpython'])
    bot.login()
    bot.init_ids()
    bot.sync()

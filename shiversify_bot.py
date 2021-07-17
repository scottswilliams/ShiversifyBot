import re
import numpy as np
from configparser import ConfigParser, ParsingError, NoSectionError
import logging
import pickle
import re
import string
import signal
import collections
from urllib.parse import quote
from time import sleep, time
from typing import Deque, List, Optional, Callable, Dict, Tuple

import praw
import emoji

contractions = {
    "ain't": "am not",
    "aren't": "are not",
    "can't": "cannot",
    "can't've": "cannot have",
    "'cause": "because",
    "could've": "could have",
    "couldn't": "could not",
    "couldn't've": "could not have",
    "didn't": "did not",
    "doesn't": "does not",
    "don't": "do not",
    "hadn't": "had not",
    "hadn't've": "had not have",
    "hasn't": "has not",
    "haven't": "have not",
    "he'd": "he had",
    "he'd've": "he would have",
    "he'll": "he will",
    "he'll've": "he will have",
    "he's": "he is",
    "how'd": "how did",
    "how'd'y": "how do you",
    "how'll": "how will",
    "how's": "how is",
    "i'd": "I had / I would",
    "i'd've": "I would have",
    "i'll": "I will",
    "i'll've": "I will have",
    "i'm": "I am",
    "i've": "I have",
    "isn't": "is not",
    "it'd": "it had",
    "it'd've": "it would have",
    "it'll": "it will",
    "it'll've": "it will have",
    "it's": "it is",
    "let's": "let us",
    "ma'am": "madam",
    "mayn't": "may not",
    "might've": "might have",
    "mightn't": "might not",
    "mightn't've": "might not have",
    "must've": "must have",
    "mustn't": "must not",
    "mustn't've": "must not have",
    "needn't": "need not",
    "needn't've": "need not have",
    "o'clock": "of the clock",
    "oughtn't": "ought not",
    "oughtn't've": "ought not have",
    "shan't": "shall not",
    "sha'n't": "shall not",
    "shan't've": "shall not have",
    "she'd": "she would",
    "she'd've": "she would have",
    "she'll": "she will",
    "she'll've": "she will have",
    "she's": "she is",
    "should've": "should have",
    "shouldn't": "should not",
    "shouldn't've": "should not have",
    "so've": "so have",
    "so's": "so is",
    "that'd": "that had",
    "that'd've": "that would have",
    "that's": "that is",
    "there'd": "there had",
    "there'd've": "there would have",
    "there's": "there is",
    "they'd": "they had",
    "they'd've": "they would have",
    "they'll": "they will",
    "they'll've": "they will have",
    "they're": "they are",
    "they've": "they have",
    "to've": "to have",
    "wasn't": "was not",
    "we'd": "we would",
    "we'd've": "we would have",
    "we'll": "we will",
    "we'll've": "we will have",
    "we're": "we are",
    "we've": "we have",
    "weren't": "were not",
    "what'll": "what will",
    "what'll've": "what will have",
    "what're": "what are",
    "what's": "what is",
    "what've": "what have",
    "when's": "hen is",
    "when've": "when have",
    "where'd": "where did",
    "where's": "where is",
    "where've": "where have",
    "who'll": "who will",
    "who'll've": "who will have",
    "who's": "who is",
    "who've": "who have",
    "why's": "why is",
    "why've": "why have",
    "will've": "will have",
    "won't": "will not",
    "won't've": "will not have",
    "would've": "would have",
    "wouldn't": "would not",
    "wouldn't've": "would not have",
    "y'all": "you all",
    "y'all'd": "you all would",
    "y'all'd've": "you all would have",
    "y'all're": "you all are",
    "y'all've": "you all have",
    "you'd": "you would",
    "you'd've": "you would have",
    "you'll": "you will",
    "you'll've": "you will have",
    "you're": "you are",
    "you've": "you have"
    }

def give_emoji_free_text(text):
    new_text = re.sub(emoji.get_emoji_regexp(), r"", text)
    return new_text

def decontraction(text : str) -> str:
    for word in text.split():
        if word.lower() in contractions:
            text = text.replace(word, contractions[word.lower()])
    return text

def shiversify(data: str) -> str:
    cooldown = np.random.choice(8, p=[0.45, 0.12, 0.12, 0.095, 0.075, 0.05, 0.05, 0.04])
    length = 0
    max_dist = 30
    bin_p = 0.25
    if(not data.strip("""!#$%&'+,-./:;<=>?@\^_`{|}~ )""")):
        return "🐊"
    pattern = re.compile('\[(.*?)\]\(.*?\)')
    data = pattern.sub(r'\1', data)
    data = list(map(lambda x: decontraction(x.strip().replace(u"\u2018", "'").replace(u"\u2019", "'")), re.split(r'(?<=[.!?]) +', data)))
    strip_again = []
    for lines in data:
        strip_again += lines.split("\n\n")
    data = strip_again
    msg = []
    for lines in data:
        if not lines.strip("""!#$%&'+,-./:;<=>?@\^_`{|}~ )"""):
            continue
        words = lines.replace("why", "wherefore").replace("Why", "Wherefore").replace("WHY", "WHEREFORE").split()
        hasShiverified = False
        length = 0
        cooldown = np.random.choice(8, p=[0.45, 0.12, 0.12, 0.095, 0.075, 0.05, 0.05, 0.04])
        for index, word in enumerate(words):
            if not word.strip("""!#$%&'+,-./:;<=>?@\^_`{|}~ )"""):
                continue
            if index == (len(words) - 1):
                word = word.rstrip("!#$%&'+,-./:;=?@\^_`{|}~")
            if (len(word) > 1 and word == word.upper() and word.lower() != word.upper()):
                words[index] = ("**" + word.upper().strip() + "**")
                if cooldown:
                    cooldown -= 1
                if length:
                    length -= 1
                else:
                    length = 1 + np.random.poisson(1)
                continue
            if (word == "HAHA" and words[index+1] == "YES"):
                words[index] = ("**" + word.upper().strip() + "**")
                hasShiverified = True
                if length:
                    length -= 1
                if cooldown:
                    cooldown -= 1
                continue
            if (index > 0 and (word == "YES" or word == "NO") and words[index-1] == "**HAHA**"):
                words[index] = ("**" + word.upper().strip() + "**")
                hasShiverified = True
                if length:
                    length -= 1
                if cooldown:
                    cooldown -= 1
                continue
            if length:
                length -= 1
                hasShiverified = True
                words[index] = ("**" + word.upper().strip() + "**")
                continue
            if cooldown == 0:
                length = 2 + np.random.poisson(1)
                if (len(words) > 1) and (len(words) - (index)) <= 1:
                    length = 0
                    continue
                hasShiverified = True
                words[index] = "**" + word.upper().strip() + "**"
                cooldown = np.random.binomial(max_dist, bin_p) + 1
            else:
                cooldown -= 1
                continue
        if hasShiverified == False:
            for index, word in enumerate(words):
                if index == (len(words) - 1):
                    word = word.rstrip("!#$%&'+,-./:;=?@\^_`{|}~")
                words[index] = ("**" + word.upper().strip() + "**")
                words[index] = words[index].replace("****","**")
        if words and words[0].startswith("**>"):
            if words[0].startswith("**>!"):
                try:
                    words[0] = (">!**" + words[0][4:]).replace("****","")
                    if words[0].endswith("!<**"):
                        try:
                            words[0] = (words[0][-4:] + "**!<").replace("****","")
                        except IndexError:
                            pass
                except IndexError:
                    pass
            else:
                try:
                    words[0] = (">**" + words[0][3:]).replace("****","")
                except IndexError:
                    pass

        msg.append(" ".join(words).rstrip("!#$%&'+, -./:;=?@\^_`{|}~") + " 🐊\n\n")

    return msg


class ShiversifyBot(object):
    __slots__ = [
        "reddit", "primary_subreddit", "subreddits", "config", "logger", "parsed", "start_time"
    ]
    submissioncount = collections.Counter()
    def __init__(self, reddit: praw.Reddit, subreddit: str) -> None:
        """initialize"""

        def register_signals() -> None:
            """registers signals"""
            signal.signal(signal.SIGTERM, self.exit)
        self.logger = logging.getLogger("shiversify_bot")
        self.logger.setLevel("INFO")
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.debug("Initializing")
        self.reddit: praw.Reddit = reddit
        self.primary_subreddit: praw.models.Subreddit = self.reddit.subreddit(
            subreddit.split("+")[0]
        )
        self.subreddits: praw.models.Subreddit = self.reddit.subreddit(
            subreddit
        )
        self.parsed: Deque[str] = Deque(maxlen=10000)
        self.start_time: float = time()
        register_signals()
        self.logger.info("Successfully initialized")

    def exit(self, signum: int, frame) -> None:
        """defines exit function"""
        import os
        _ = frame
        self.save()
        self.logger.info("Exited gracefully with signal %s", signum)
        os._exit(os.EX_OK)
        return

    def save(self) -> None:
        """pickles tracked comments after shutdown"""
        self.logger.debug("Saving file")
        with open("parsed.pkl", 'wb') as parsed_file:
            parsed_file.write(pickle.dumps(self.parsed))
            self.logger.debug("Saved file")
            return
        return
    def listen(self) -> None:
        """lists to subreddit's comments for pings"""
        import prawcore
        try:
            for comment in self.subreddits.stream.comments(pause_after=1):
                if comment is None:
                    break
                if comment.banned_by is not None:
                    # Don't trigger on removed comments
                    continue
                if comment.created_utc < self.start_time:
                    # Don't trigger on comments posted prior to startup
                    continue
                if str(comment) in self.parsed:
                    continue
                self.handle_comment(comment)
        except prawcore.exceptions.ServerError:
            self.logger.error("Server error: Sleeping for 30s.")
            sleep(30)
        except prawcore.exceptions.ResponseException:
            self.logger.error("Response error: Sleeping for 30s.")
            sleep(30)
        except prawcore.exceptions.RequestException:
            self.logger.error("Request error: Sleeping for 30s.")
            sleep(30)
    def handle_comment(self, comment: praw.models.Comment) -> None:
        self.logger.debug("Handling comment")
        body = comment.body
        data = comment.body.upper().split()
        self.parsed.append(str(comment))
        if (isinstance(comment.parent(), praw.models.Comment)):
            if (comment.parent().author is not None) and (comment.parent().author.name.upper() == "SHIVERSIFYBOT"):
                return
        if (comment.author is not None) and (comment.author.name.upper() == "SHIVERSIFYBOT"):
            return
        if "!SHIVERSIFY" in body.upper():
            if (isinstance(comment.parent(), praw.models.Submission)):
                return
            if (comment.parent() is not None and isinstance(comment.parent(), praw.models.Comment) and (comment.parent().author is not None) and (comment.parent().author.name.lower() == "sir_shivers")):
                try:
                    return comment.reply(comment.parent().body)
                except praw.exceptions.APIException:
                    return
            return self.handle_shiversify(comment, give_emoji_free_text(comment.parent().body.replace("*","").replace('\u200c', '')))
        if "SHIVERS TAKE" in body.upper().replace("""!#$%&'+,-./:;<=>?@\^_`{|}~ )""", ""):
            self.handle_shiverslevel(comment)
    def handle_shiversify(self, comment: praw.models.Comment, data: str):
        self.logger.info(f"Handling shiversify: {data}")
        try:
           return comment.reply(f"""{"".join(shiversify(data))[0:9999]}""") 
        except praw.exceptions.APIException:
            return
    def handle_shiverslevel(self, comment):
        self.logger.info("Handling ShiversLevel")
        rndm = np.random.randint(0,101) 
        if (rndm == 0 or rndm == 1):
            try:
                comment.reply("""**HAHA YES**
                                \n
                                \n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣶⠶⠛⣭⣭⠛⠛⠓⡳⣶⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                                \n⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⠟⢋⠁⠀⣤⡄⠀⣀⣀⠈⠙⡧⠉⠻⢧⣄⠀⠀⠀⠀⠀⠀⠀⠀
                                \n⠀⠀⠀⠀⠀⠀⠀⠀⢠⡿⠃⠸⠛⠁⠀⠀⠀⠀⠉⠙⠇⠀⠀⠀⢀⣀⠙⣧⡀⠀⠀⠀⠀⠀⠀
                                \n⠀⠀⠀⠀⠀⠀⠀⣰⡟⠗⠀⠀⣠⣶⠟⠛⠛⠻⢶⡄⠀⢰⣆⠀⠈⢿⠀⠈⢻⡆⠀⠀⠀⠀⠀
                                \n⠀⠀⠀⠀⠀⣀⣴⠟⠁⠀⣠⡾⠋⠀⠀⠀⠀⠀⠀⣿⠀⠈⠋⠀⠀⠀⠀⠀⠀⣿⡀⠀⠀⠀⠀
                                \n⠀⠀⢰⣟⣛⣋⣁⣠⣴⠟⠋⠀⠀⠀⠀⠀⢀⣀⣴⠟⠀⣰⡇⠀⠀⢀⣶⠀⠀⢸⣇⠀⠀⠀⠀
                                \n⠀⠀⠈⠉⠉⠉⠉⠉⠀⠀⠀⠀⠀⢀⣤⡾⠛⠉⠁⠀⠀⠉⠀⠀⠀⠈⠿⠀⠀⠀⣿⠀⠀⠀⠀
                                \n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡿⠁⠀⠀⠀⠀⣴⡾⠀⠀⠀⠀⢀⡀⠀⠀⠀⠙⢷⣆⠀⠀
                                \n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⢀⡀⠀⠿⠀⠀⠀⠀⠀⣾⠃⠀⢀⡀⠀⠀⢻⡆⠀
                                \n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣧⠀⠀⣸⠇⠀⡀⠀⠀⠀⠀⠀⠛⠀⠀⣾⠇⠀⠀⢸⡇⠀
                                \n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡿⠀⢰⡟⢠⡿⠋⠀⠀⠀⠀⣠⡀⠀⠀⣿⠀⠀⠀⢸⡇⠀
                                \n⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣤⣤⣬⣻⡷⣾⠀⠈⠃⠀⠀⠀⠀⢰⣿⠀⠀⠀⢿⡄⠀⠀⠘⣧⡀
                                \n⠀⠀⠀⠀⠀⠀⠀⣼⠟⠉⠁⠀⠉⠉⠛⠋⢰⡾⠂⠀⠀⠀⠀⠀⠁⠀⠀⠀⢈⣿⣦⠀⠀⠉⣷
                                \n⠀⠀⠀⠀⠀⠀⣰⡟⠀⣠⣤⣤⣤⣤⡀⠀⠸⠇⠀⠀⠀⢠⡾⠇⠀⠀⠀⠀⣾⠃⣿⠀⠀⣠⡿
                                \n⠀⠀⠀⢀⣤⡾⠋⠀⣼⠏⠀⠀⠀⠈⠁⠀⠀⠀⠀⠀⠀⠘⠃⠀⠀⠀⠀⠘⣿⣤⣼⣛⠛⠛⠁
                                \n⠀⠀⠀⠸⣧⡀⠀⣰⡟⠀⠀⠀⠀⠀⢠⣶⣦⡀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠉⢹⡇⠀⠀
                                \n⠀⣀⣀⣀⣸⡷⠾⠋⠀⠀⠀⠀⠀⠀⠘⠻⠟⠁⠀⠀⠀⠀⠀⠘⣷⠀⠀⠀⠀⠀⠀⠈⣿⠀⠀
                                \n⣾⢫⣭⠉⢉⣀⠀⠀⠀⣀⣠⣤⣴⣶⣿⡷⠀⠀⠀⠀⢀⣠⣴⠟⠙⠛⠛⢷⡄⠀⠀⢠⡿⠀⠀
                                \n⢻⣤⣤⣤⣬⣿⠶⠾⠛⠋⣛⣯⡶⠟⠁⠀⠀⠀⣀⣾⠛⠉⠀⠀⠀⠀⠀⣼⠇⠀⠀⢸⡇⠀⠀
                                \n⠀⢸⣷⣿⣆⣀⣼⣷⡶⠟⢋⣡⣤⣤⣤⣤⣶⠾⠋⠁⠀⠀⠀⠀⠀⠀⠸⣯⣤⣤⡶⠾⠁⠀⠀
                                \n⠀⠈⠻⢿⣭⣭⣥⣤⣴⠾⠟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀""")
            except praw.exceptions.APIException:
                return
        elif (rndm == 2 or rndm == 3):
            try:
                comment.reply("""**HAHA NO**
                                \n
                                \n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣶⠶⠛⣭⣭⠛⠛⠓⡳⣶⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                                \n⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⠟⢋⠁⠀⣤⡄⠀⣀⣀⠈⠙⡧⠉⠻⢧⣄⠀⠀⠀⠀⠀⠀⠀⠀
                                \n⠀⠀⠀⠀⠀⠀⠀⠀⢠⡿⠃⠸⠛⠁⠀⠀⠀⠀⠉⠙⠇⠀⠀⠀⢀⣀⠙⣧⡀⠀⠀⠀⠀⠀⠀
                                \n⠀⠀⠀⠀⠀⠀⠀⣰⡟⠗⠀⠀⣠⣶⠟⠛⠛⠻⢶⡄⠀⢰⣆⠀⠈⢿⠀⠈⢻⡆⠀⠀⠀⠀⠀
                                \n⠀⠀⠀⠀⠀⣀⣴⠟⠁⠀⣠⡾⠋⠀⠀⠀⠀⠀⠀⣿⠀⠈⠋⠀⠀⠀⠀⠀⠀⣿⡀⠀⠀⠀⠀
                                \n⠀⠀⢰⣟⣛⣋⣁⣠⣴⠟⠋⠀⠀⠀⠀⠀⢀⣀⣴⠟⠀⣰⡇⠀⠀⢀⣶⠀⠀⢸⣇⠀⠀⠀⠀
                                \n⠀⠀⠈⠉⠉⠉⠉⠉⠀⠀⠀⠀⠀⢀⣤⡾⠛⠉⠁⠀⠀⠉⠀⠀⠀⠈⠿⠀⠀⠀⣿⠀⠀⠀⠀
                                \n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡿⠁⠀⠀⠀⠀⣴⡾⠀⠀⠀⠀⢀⡀⠀⠀⠀⠙⢷⣆⠀⠀
                                \n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⢀⡀⠀⠿⠀⠀⠀⠀⠀⣾⠃⠀⢀⡀⠀⠀⢻⡆⠀
                                \n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣧⠀⠀⣸⠇⠀⡀⠀⠀⠀⠀⠀⠛⠀⠀⣾⠇⠀⠀⢸⡇⠀
                                \n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡿⠀⢰⡟⢠⡿⠋⠀⠀⠀⠀⣠⡀⠀⠀⣿⠀⠀⠀⢸⡇⠀
                                \n⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣤⣤⣬⣻⡷⣾⠀⠈⠃⠀⠀⠀⠀⢰⣿⠀⠀⠀⢿⡄⠀⠀⠘⣧⡀
                                \n⠀⠀⠀⠀⠀⠀⠀⣼⠟⠉⠁⠀⠉⠉⠛⠋⢰⡾⠂⠀⠀⠀⠀⠀⠁⠀⠀⠀⢈⣿⣦⠀⠀⠉⣷
                                \n⠀⠀⠀⠀⠀⠀⣰⡟⠀⣠⣤⣤⣤⣤⡀⠀⠸⠇⠀⠀⠀⢠⡾⠇⠀⠀⠀⠀⣾⠃⣿⠀⠀⣠⡿
                                \n⠀⠀⠀⢀⣤⡾⠋⠀⣼⠏⠀⠀⠀⠈⠁⠀⠀⠀⠀⠀⠀⠘⠃⠀⠀⠀⠀⠘⣿⣤⣼⣛⠛⠛⠁
                                \n⠀⠀⠀⠸⣧⡀⠀⣰⡟⠀⠀⠀⠀⠀⢠⣶⣦⡀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠉⢹⡇⠀⠀
                                \n⠀⣀⣀⣀⣸⡷⠾⠋⠀⠀⠀⠀⠀⠀⠘⠻⠟⠁⠀⠀⠀⠀⠀⠘⣷⠀⠀⠀⠀⠀⠀⠈⣿⠀⠀
                                \n⣾⢫⣭⠉⢉⣀⠀⠀⠀⣀⣠⣤⣴⣶⣿⡷⠀⠀⠀⠀⢀⣠⣴⠟⠙⠛⠛⢷⡄⠀⠀⢠⡿⠀⠀
                                \n⢻⣤⣤⣤⣬⣿⠶⠾⠛⠋⣛⣯⡶⠟⠁⠀⠀⠀⣀⣾⠛⠉⠀⠀⠀⠀⠀⣼⠇⠀⠀⢸⡇⠀⠀
                                \n⠀⢸⣷⣿⣆⣀⣼⣷⡶⠟⢋⣡⣤⣤⣤⣤⣶⠾⠋⠁⠀⠀⠀⠀⠀⠀⠸⣯⣤⣤⡶⠾⠁⠀⠀
                                \n⠀⠈⠻⢿⣭⣭⣥⣤⣴⠾⠟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀""")
            except praw.exceptions.APIException:
                return
        elif (rndm == 4 or rndm == 5):
            try:
                comment.reply("""‼️‼️HOLY FUCKING SHIT‼️‼️‼️‼️ IS THAT A MOTHERFUCKING SIR SHIVERS REFERENCE??????!!!!!!!!!!11!1!1!1!1!1!1! 😱😱😱😱😱😱😱 SIR SHIVERS IS THE BEST FUCKING USER 🔥🔥🔥🔥💯💯💯💯 MAMMALS ARE SO DUMBBBB 🕵️🕵️🕵️🕵️🕵️🕵️🕵️🟥🟥🟥🟥🟥 COME TO THE DT AND WATCH ME POST 🏥🏥🏥🏥🏥🏥🏥🏥 🏥🏥🏥🏥 WHY IS NO ONE FIXING THEIR TAKES 🤬😡🤬😡🤬😡🤬🤬😡🤬🤬😡 OH YOUR A REPTILE? NAME EVERY SCALE🔫😠🔫😠🔫😠🔫😠🔫😠HAHA YES🐊 🐊 🐊 🐊  HAHA YES🐊  🐊 HAHA YES🐊 🐊 HAHA YES 🐊 🐊 🐊 🐊  HAHA YES🐊  🐊 🐊 🐊 HAHA YES 🐊 🐊 🐊 🐊 🐊 🐊  🐊  🐊 HAHA YES🐊 🐊 🐊 🐊 HAHA YES 🐊 🐊 🐊 HAHA YES 🐊 🐊 🐊 🐊  🐊  🐊 🐊 🐊 🐊 🐊 🐊 🐊 HAHA YES🐊 🐊 🐊 HAHA YES🐊 🐊 🐊 🐊  🐊  HAHA YES  🐊 🐊 🐊 🐊 🐊 🐊 I think it was sir shivers!👀👀👀👀👀👀👀👀👀👀It wasnt me I was in DT !!!!!!!!!!!!!!😂🤣😂🤣😂🤣😂😂😂🤣🤣🤣😂😂😂 r/sirshiversmemes r/unexpectedsirshivers r/expectedsirshivers perfectly reptilian as all things should be""")
            except praw.exceptions.APIException:
                return
        elif ((rndm % 2) == 0):
            try:
                comment.reply("**HAHA YES** 🐊")
            except praw.exceptions.APIException:
                return
        else:
            try:
                comment.reply("**HAHA NO** 🐊")
            except praw.exceptions.APIException as e:
                return

 
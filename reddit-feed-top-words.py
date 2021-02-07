import praw
import collections
import string
import pretty_errors #do not delete
import time
from csv import reader
from itertools import islice

#--- Pre-Reqs ---#
#panda
import pandas as pd
def print_full(x):
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 2000)
    pd.set_option('display.float_format', '{:20,.2f}'.format)
    pd.set_option('display.max_colwidth', None)
    print(x)
    pd.reset_option('display.max_rows')
    pd.reset_option('display.max_columns')
    pd.reset_option('display.width')
    pd.reset_option('display.float_format')
    pd.reset_option('display.max_colwidth')

#stopwords
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

#login
from login_creds import client_id
from login_creds import client_secret
from login_creds import username
from login_creds import password
from login_creds import user_agent

reddit = praw.Reddit(
    client_id= client_id,  # my client id
    client_secret= client_secret,  # your client secret
    user_agent= user_agent,  # user agent name
    username= username,  # your reddit username
    password= password)  # your reddit password

#--- Choose Function ---#
def user_choice():
    message = ''
    while message != 'quit':
        choice = int(input(f'\nWelcome! Please choose a mode to use?'
            f'\n1) Submit reddit post URL for csv output.'
            f'\n2) Submit reddit post URL for streaming output.'     
            f'\n3) Find post comments in a subreddit using a search term.'
            f'\n99) Quit'
            f'\n>>: '))
        if choice == 1:
            url = input('\nWhat is the URL of the Reddit thread?: ')
            pages = input(f"\nLet's set a limit on pages to scrape..."
                          f'\nHow many pages should the program scrape before stopping? (Type "None" if you want every page)'
                          f"\n>>: ")
            url_method(url, pages)
        if choice == 2:
            url = input('\nWhat is the URL of the Reddit thread?: ')
            pages = input(f"\nLet's set a limit on pages to scrape..."
                          f'\nHow many pages should the program scrape before stopping? (Type "None" if you want every page)'
                          f"\n>>: ")
            url_streaming(url, pages)
        if choice == 3:
            query_method()
        else:
            message = 'quit'

#--- URL to CSV Function ---#
def url_method(url, pages):
    reddit_to_csv(url, pages)
    print("\n***--- DONE! Check the program's directory! ---***")

    time.sleep(1)
    return

#--- Streaming Function ---#
def url_streaming(url, pages):
    message = ''
    while message != 'quit':
        reddit_to_csv(url, pages)
        try:
            # iterate over each line as a ordered dictionary and print only few column by column name
            with open('WORD_Count_RESULTS_from_URL.csv', 'r', encoding="utf8") as read_obj:
                csv_reader = reader(read_obj)
                for row in islice(csv_reader, 1, 51):
                    print(f'Rank: {row[0]}      Word: {row[1]} : {row[2]}')
                    time.sleep(1)
            print('*** Recalculating... ***')
        except KeyboardInterrupt:
            break

#--- Search Term Function ---#
def query_method():
    sub_input = input(f'\nWhat is the name of the subreddit?'
                f'\n>>: r/')
    sub = [sub_input]
    #sub = ['wallstreetbets']  # make a list of subreddits you want to scrape the data from
    for s in sub:
        subreddit = reddit.subreddit(s)

        # SCRAPING CAN BE DONE VIA VARIOUS STRATEGIES {HOT,TOP,etc} we will go with keyword strategy i.e using search a keyword
        query_input = input(f'\nWhat keyword would you like to search for?'
                      f'\n >>: ')
        query = [query_input]
        #query = ['calm']

        for item in query:
            post_dict = {
                "title": [],  # title of the post
                "score": [],  # score of the post
                "id": [],  # unique id of the post
                "url": [],  # url of the post
                "comms_num": [],  # the number of comments on the post
                "created": [],  # timestamp of the post
                "body": []  # the descriptionof post
            }
            comments_dict = {
                "comment_id": [],  # unique comm id
                "comment_parent_id": [],  # comment parent id
                "comment_body": [],  # text in comment
                "comment_link_id": []  # link to the comment
            }
            for submission in subreddit.search(query, sort="top", limit=2):
                post_dict["title"].append(submission.title)
                post_dict["score"].append(submission.title)
                post_dict["id"].append(submission.title)
                post_dict["url"].append(submission.title)
                post_dict["comms_num"].append(submission.title)
                post_dict["created"].append(submission.title)
                post_dict["body"].append(submission.title)

                ##### Acessing comments on the post
                submission.comments.replace_more(limit=1)
                for comment in submission.comments.list():
                    comments_dict["comment_id"].append(comment.id)
                    comments_dict["comment_parent_id"].append(comment.parent_id)
                    comments_dict["comment_body"].append(comment.body)
                    comments_dict["comment_link_id"].append(comment.link_id)

            post_comments = pd.DataFrame(comments_dict)
            post_comments.to_csv("RESULTS_Comments_from_URL.csv")
            post_data = pd.DataFrame(post_dict)
            post_data.to_csv(s + "_" + item + "subreddit.csv")
            print("***Two CSV files have been created. Check the program's directory!***")

            # --- Word Counter ---#
            allcommentslist = (comments_dict.get('comment_body'))
            allcomments = word_counter(allcommentslist)  # Uses created word counter function
            allcomments.to_csv("WORD_Count_RESULTS_from_URL.csv")

#--- Shared Functions ---#
def reddit_to_csv(url, pages):
    # url = input('\nWhat is the URL of the Reddit thread?: ')
    submission = reddit.submission(url=url)

    # CSV Storage
    for item in url:
        comments_dict = {
            "comment_id": [],  # unique comm id
            "comment_parent_id": [],  # comment parent id
            "comment_body": [],  # text in comment
            "comment_link_id": []  # link to the comment
        }

        # pages = input(f"\nLet's set a limit on pages to scrape..."
        #               f'\nHow many pages should the program scrape before stopping? (Type "None" if you want every page)'
        #               f"\n>>: ")
        if pages.isnumeric():
            pages = int(pages)

        else:
            pages = None

        submission.comments.replace_more(limit=pages)
        for comment in submission.comments.list():
            comments_dict["comment_id"].append(comment.id)
            comments_dict["comment_parent_id"].append(comment.parent_id)
            comments_dict["comment_body"].append(comment.body)
            comments_dict["comment_link_id"].append(comment.link_id)

        post_comments = pd.DataFrame(comments_dict)
        post_comments.to_csv("RESULTS_Comments_from_URL.csv")

        # Word Counter
        allcommentslist = (comments_dict.get('comment_body'))
        allcomments = word_counter(allcommentslist)  # Uses created word counter function
        allcomments.to_csv("WORD_Count_RESULTS_from_URL.csv")
        return

def word_counter(allcommentslist): #Next task is to add stopwords
    allcommentsstr = ''.join(allcommentslist)
    allcomments_split = allcommentsstr.split()

    filtered_sentence = stopwordmachine(allcomments_split)
    filtered_sentence_split = filtered_sentence.split()

    allcomments_count = collections.Counter(filtered_sentence_split)
    allcomments_count_sorted = allcomments_count.most_common()
    allcomments = pd.DataFrame(allcomments_count_sorted)
    return allcomments

def stopwordmachine(allcomments_split):
    all_stopwords = stopwords.words('english')
    all_stopwords.append("’")
    all_stopwords.append('“')
    all_stopwords.append('”')

    allcomments_split = str(allcomments_split)
    allcomments_split = allcomments_split.lower()
    allcomments_split_nopunc = allcomments_split.translate(str.maketrans('', '', string.punctuation))
    text_tokens = word_tokenize(allcomments_split_nopunc)
    tokens_without_sw = [word for word in text_tokens if not word in all_stopwords]
    filtered_sentence = (" ").join(tokens_without_sw)
    return(filtered_sentence)

# --- Main Function --- #
if __name__ == '__main__':
    user_choice()






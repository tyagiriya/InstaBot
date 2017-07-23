import requests, urllib
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
#from matplotlitb import pyplot as plt
# import numpy as np
import re

'''
GLOBAL VARIABLE TO STORE BASE URL AND ACCESS TOKEN OF THE USER 
'''

ACCESS_TOKEN = '3131506344.bf81073.3236628840fb4cee9581afe5952280e1'
# BASE_URL = "https://a...content-available-to-author-only...m.com/v1/"
BASE_URL = "https://api.instagram.com/v1/"


################################################# SELF INFO #############################################################
'''
FUNCTION DECLERATION TO GET YOUR OWN INFO
'''
def self_info():

    request_url = (BASE_URL + 'users/self/?access_token=%s') % (ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'User does not exist!'
    else:
        print 'Status code other than 200 received!'


############################################ GET_USER_ID ######################################################################
'''
FUNCTION DECLERATION TO GET THE ID OF A USER BY USERNAME
'''
def get_user_id(insta_username):
    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s')%(insta_username, ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            return user_info['data'][0]['id']
           # print user_info['data']
        else:
            return None
    else:
        print 'Status code other than 200 received!'
        exit


############################################ GET_USER_INFO #########################################################################

'''
FUNCTION DECLERATION TO GET THE INFO OF A USER BY USERNAME
'''
def get_user_info(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/?access_token=%s') % (user_id, ACCESS_TOKEN)
    # https: // api.instagram.com / v1 /cc users / {user - id} /?access_token = ACCESS - TOKEN
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'There is no data for this user!'
    else:
        print 'The profile is private'


################################################## GET_OWN_POST ############################################################

'''
FUNCTION OF DECLARATION TO GET YOUR RECENT POST
'''
def get_own_post():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    own_media = requests.get(request_url).json()

    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            image_name = own_media['data'][0]['id'] + '.jpeg'
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'


############################################# GET_USER_POST ############################################################

'''
FUNCTION DECLERATION TO GET THE RECENT POST BY USERNAME
'''

def get_user_post(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'


######################################## GET_POST _ID#######################################################
'''
FUNCTION DECLERATION TO GET THE ID OF THE RECENT POST OF A USER BY USERNAME 
'''
def get_post_id(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            return user_media['data'][0]['id']
        else:
            print 'There is no recent post of the user!'
            exit()
    else:
        print 'Status code other than 200 received!'
        exit()


############################################ LIKE_A_POST ########################################################
'''
 FUNCTION  DECLERTAION TO  LIKE THE  RECENT  POST OF A USER
'''

def like_a_post(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes') % (media_id)
    payload = {"access_token": ACCESS_TOKEN}
    print 'POST request url : %s' % (request_url)
    post_a_like = requests.post(request_url, payload).json()
    if post_a_like['meta']['code'] == 200:
        print 'Like was successful!'
    else:
        print 'Your like was unsuccessful. Try again!'


############################################### GET_LIKE_LIST ##################################
    '''
    FUNCTION TO GET THE LIST OF USERS LIKED THE RECENT POST OF THE USER
    '''

def get_like_list(insta_username):
        media_id = get_post_id(insta_username)
        request_url = (BASE_URL + 'media/%s/likes?access_token=%s') % (media_id, ACCESS_TOKEN)
        print 'GET request url : %s' % (request_url)
        like_list = requests.get(request_url).json()
        if like_list['meta']['code'] == 200:
            if len(like_list['data']):
                print "Post liked by :"
                for i in range(len(like_list['data'])):
                    print "%d)" % (i + 1) + like_list['data'][i]['username']
            else:
                print "No one liked the recent post of user"
        else:
            print 'Status code other than 200 received!'


##################################### POST_A_COMMENT #####################################################################
'''
FUNCTION DECLERATION TO MAKE A COMMENT ON THE RECENT POST OF THE USER
'''

def post_a_comment(insta_username):
    media_id = get_post_id(insta_username)
    comment_text = raw_input("Your comment: ")
    payload = {"access_token": ACCESS_TOKEN, "text" : comment_text}
    request_url = (BASE_URL + 'media/%s/comments') % (media_id)
    print 'POST request url : %s' % (request_url)

    make_comment = requests.post(request_url, payload).json()

    if make_comment['meta']['code'] == 200:
        print "Successfully added a new comment!"
    else:
        print "Unable to add comment. Try again!"


############################################# DELETE_NEGATIVE_COMMENT ########################################################

'''
FUNCTION DECLERATION TO MAKE DELETE NEGATIVE COMMENTS FROM THE RECENT POST 
'''

def delete_negative_comment(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()

    if comment_info['meta']['code'] == 200 and len(comment_info['data']):
    #here's a native implementaion of how to delete the negative comment:
        for x in range(0, len(comment_info['data'])):
            comment_id = comment_info['data'][x]['id']
            comment_text = comment_info['data'][x]['text']
            blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
            if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                print 'Negative comment : %s' % (comment_text)
                delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (media_id, comment_id, ACCESS_TOKEN)
                print 'DELETE request url : %s' % (delete_url)
                delete_info = requests.delete(delete_url).json()

                if delete_info['meta']['code'] == 200:
                        print 'Comment successfully deleted!\n'
                else:
                        print 'Unable to delete comment!'
            else:
                    print 'Positive comment : %s\n' % (comment_text)
        else:
            print 'There are no existing comments on the post!'
    else:
      print 'Status code other than 200 received!'


    ############################################# ANALYSE_INTEREST ###########################################
    '''
    FUNCTION DECLERTAION TO ANALYSE THE INTEREST OF  THE USER BY THEIR HASHTAG
    '''
def analyse_interest(insta_username):
        user_id = get_user_id(insta_username)
        media_id = get_post_id(insta_username)
        if user_id == None:
            print 'User does not exist!'
            exit()
        request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s')%(user_id, ACCESS_TOKEN)
        print 'GET request url : %s' % (request_url)
        user_media = requests.get(request_url).json()
        print user_media
        if user_media['meta']['code'] ==200:
            if len(user_media['data']):
                print user_media['data'][0]['caption']
            else:
                print 'There is no recent post of the user!'
                exit()
        else:
            print 'status code other than 200 received!'
            exit()

### Rectified for obtaining caption #####
        hashtags = []
        if user_media['data'][0]['caption'] is None:
            return hashtags
        else:
            for tag in re.findall("#[a-zA-Z0-9]+", str(user_media['data'][0]['caption'])):
                hashtags.append(tag)
            #print hashtags
          

        my_dict={"sports":("cricket", "football","Tennis","vollyball","Badminton"), "Day":("morning","evening","night","dark"),"wheather":("cloudy","rainy","spring","Autum")}
        for item in hashtags:
            for key,value in my_dict.items():

                if item in value:
                    print "interest in:"
                    print key,
        #for Z in range(0, len(user_media.caption['data'])):
         #Z = np.random.uniform(0, 1, 20)
            #plt.pie

################################### GET_COMMENT_LIST #####################################################3
'''
FUNCTION TO GET THE LIST OF COMMENTS ON A POST OF GIVEN USERNAME.
'''
def get_comment_list(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments?access_token=%s') % (media_id, ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_list = requests.get(request_url).json()
    if comment_list['meta']['code'] == 200:
        if len(comment_list['data']):
            print "Post liked by :"
            for i in range(len(comment_list['data'])):
                print "%d)" % (i + 1) + comment_list['data'][i]['text']
        else:
            print "No one commented the recent post of user"
    else:
        print 'Status code other than 200 received!'





######################################################## INSTA_BOT_MENU ##################################################
'''
FUNCTION TO START THE INSTA BOT
'''

def start_bot():
    #global get_like_list()
    #6get_like_list =0
    #global get_like_list

    while True:
        print '\n'
        print 'Hey! Welcome to instaBot!'
        print 'Here are your menu options:'
        print "1.Get your own details\n"
        print "2.Get details of a user by username\n"
        print "3.Get your own recent post\n"
        print "4.Get the recent post of a user by username\n"
        print "5.like post\n"
        print "6.Get a list of people who have liked the recent post of a user\n"
        print "7.Make a comment on the recent post of a user\n"
        print "8.Delete negative comments from the recent post of a user\n"
        print "9.analyse_interest\n"
        print "10.Exit"

        choice = raw_input("Enter you choice: ")
        if choice == "1":
            self_info()

        elif choice == "2":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_info(insta_username)
        elif choice == "3":
            get_own_post()
        elif choice == "4":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_post(insta_username)
        elif choice=="5":
            insta_username = raw_input("Enter the username of the user: ")
            like_a_post(insta_username)
        elif choice=="6":
            insta_username =raw_input("Enter the username of the user: ")
            get_like_list(insta_username)
        elif choice=="7":
            insta_username = raw_input("Enter the username of the user: ")
            post_a_comment(insta_username)
        elif choice=="8":
           insta_username = raw_input("Enter the username of the user: ")
           delete_negative_comment(insta_username)

        elif choice=="9":
            insta_username = raw_input("Enter the username of the user: ")
            analyse_interest(insta_username)


        elif choice == "10":
            exit()
        else:
            print "wrong choice"

start_bot()

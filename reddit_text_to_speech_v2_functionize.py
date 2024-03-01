#!/usr/bin/env python
# coding: utf-8

# In[79]:


import praw
import os
import pandas as pd
import re
import sys
sys.path.append('C:\\Users\\kevin\\Google Drive\\My Drive\\Github\\all-api-keys')


# # Reddit API Setup

# In[80]:


# Save the current directory
original_directory = 'C:\\Users\\kevin\\Google Drive\\My Drive\\Github\\Repos\\reddit_text_to_speech'

# Switch to the new directory
new_directory = 'C:\\Users\\kevin\\Google Drive\\My Drive\\Github\\all-api-keys'
os.chdir(new_directory)

# Your code that operates in the new directory goes here
import secret

# Switch back to the original directory
os.chdir(original_directory)


# In[81]:


reddit = praw.Reddit(client_id = secret.reddit_client_id,
                     client_secret=secret.reddit_secret_key,
                     user_agent=secret.reddit_app_name,
                     username=secret.reddit_username,
                     password=secret.reddit_password)


# # Pull Comments from Reddit Subreddits

# In[82]:


# # Choose the subreddit
# subreddit_name = "askreddit"

# # Access the subreddit
# subreddit = reddit.subreddit(subreddit_name)

# # Of last 24 hours only.
# top_posts = subreddit.top(time_filter='day', limit=10)
# # Fetch the top 10 posts from all time
# # top_posts = subreddit.top(limit=10)

# # Initialize an empty list to store the data
# data = []

# # Iterate over the posts and comments
# for post in top_posts:
#     post_title = post.title
#     post_url = post.url
#     subreddit_name = post.subreddit.display_name

#     post.comment_sort = 'top'  # Sort comments by top votes
#     post.comments.replace_more(limit=0)  # Load all comments, remove 'more comments' links

#     # top_comments = post.comments.list()[:10]
#     # Can't just go for top comments, need to swerve the "[removed]" ones.
#     # Initialize an empty list to hold the top comments
#     top_comments = []
    
#     # Iterate through the list of comments
#     for comment in post.comments.list():
#         # Check if the comment has not been removed
#         if not comment.body == "[removed]":
#             # Add the comment to the list of top comments
#             top_comments.append(comment)
#         # Break the loop if we have collected 10 comments
#         if len(top_comments) == 10:
#             break

#     for comment in top_comments:
#         # Append each comment along with post and subreddit details to the data list
#         data.append([subreddit_name, post_title, post_url, comment.body])

# # Create a DataFrame
# df = pd.DataFrame(data, columns=['Subreddit', 'Post Title', 'Post URL', 'Comment'])
# df


# In[83]:


# def remove_emojis(text):
#     # Define a regular expression pattern for emojis
#     emoji_pattern = re.compile("["
#                                u"\U0001F600-\U0001F64F"  # emoticons
#                                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
#                                u"\U0001F680-\U0001F6FF"  # transport & map symbols
#                                u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
#                                u"\U00002702-\U000027B0"
#                                u"\U000024C2-\U0001F251" 
#                                "]+", flags=re.UNICODE)
#     return emoji_pattern.sub(r'', text)


# In[84]:


# # Apply remove_emojis function to all elements in the DataFrame
# df = df.applymap(remove_emojis)

# # This didnt work i saw an emoji:
# # for column in df.columns:
#     # df[column] = df[column].map(remove_emojis)


# In[85]:


# # Now you can export the DataFrame
# df.to_csv('reddit_data.csv', index=False, encoding='utf-16', sep='\t')


# # Function: Reddit to CSV

# In[86]:


def reddit_to_df(subreddit_name="askreddit", time_filter='day', n_posts=10):
    # Choose the subreddit
    # subreddit_name = "askreddit"
    
    # Access the subreddit
    subreddit = reddit.subreddit(subreddit_name)
    
    # Of last 24 hours only.
    top_posts = subreddit.top(time_filter=time_filter, limit=n_posts)
    
    # Fetch the top 10 posts from all time
    # top_posts = subreddit.top(limit=10)
    
    # Initialize an empty list to store the data
    data = []
    
    # Iterate over the posts and comments
    for post in top_posts:
        post_title = post.title
        post_url = post.url
        subreddit_name = post.subreddit.display_name
    
        post.comment_sort = 'top'  # Sort comments by top votes
        post.comments.replace_more(limit=0)  # Load all comments, remove 'more comments' links
    
        # top_comments = post.comments.list()[:10]
        # Can't just go for top comments, need to swerve the "[removed]" ones.
        # Initialize an empty list to hold the top comments
        top_comments = []
        
        # Iterate through the list of comments
        for comment in post.comments.list():
            # Check if the comment has not been removed
            if not (comment.body == "[removed]" or comment.body == "[deleted]"):
                # Add the comment to the list of top comments
                top_comments.append(comment)
            # Break the loop if we have collected 10 comments
            if len(top_comments) == n_posts:
                break
    
        for comment in top_comments:
            # Append each comment along with post and subreddit details to the data list
            data.append([subreddit_name, post_title, post_url, comment.body])
    
    # Create a DataFrame
    df = pd.DataFrame(data, columns=['Subreddit', 'Post Title', 'Post URL', 'Comment'])

    def remove_emojis(text):
        # Define a regular expression pattern for emojis
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   u"\U00002702-\U000027B0"
                                   u"\U000024C2-\U0001F251" 
                                   "]+", flags=re.UNICODE)
        return emoji_pattern.sub(r'', text)
    # Remove emojis    
    df = df.applymap(remove_emojis)
    return df


# In[87]:


def df_to_csv(df):
    df.to_csv('reddit_data.csv', index=False, encoding='utf-16', sep='\t')
    return 'Complete!'


# In[88]:


df = reddit_to_df(subreddit_name="askreddit", time_filter='day', n_posts=10)
df


# In[89]:


df_to_csv(df)


# # Use ElevenLabs API to text-to-speech your df

# In[90]:


import elevenlabs
elevenlabs.set_api_key(secret.eleven_labs_api_key)


# In[91]:


mp3_file_path = r'C:\Users\kevin\Google Drive\My Drive\Github\Repos\reddit_text_to_speech\elevenlabs_audio'
# Adding an extra '\' to every '\' found in the original path
escaped_path = mp3_file_path.replace("\\", "\\\\")
download_directory = escaped_path
download_directory


# In[92]:


# What voices are available?
from elevenlabs.api import Voices
voices = Voices.from_api()
# print(voices[0])
# Iterate through each voice object
for voice in voices:
    if voice.name == 'Lily':
        print(voice.voice_id)
        print(voice.name)
        if voice.labels:  # Check if labels are not None or empty
            for label, value in voice.labels.items():
                print(f"{label}: {value}")


# In[93]:


# You need to load from csv cuz u havent cleaned the emojis from df above.
csv_file_path = 'reddit_data.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file_path, encoding='utf-16', sep='\t')
df[11:20]


# In[94]:


# Concate all relevant text into 1 variable to output as mp3.
def concatenate_q_and_all_comments(df, n_posts):
    text_list = []  # Initialize as an empty list
    current_list_index = -1  # Initialize a pointer to manage the current inner list
    counter_to_read_outloud = 1
    
    for index, row in df.iterrows():
        if index % n_posts == 0:
            # Create a new string for each new range of indices (0-9, 10-19, ...)
            text_list.append("")  # Start with an empty string
            current_list_index += 1  # Move to the next "inner list" which is actually a string now
            counter_to_read_outloud = 1  # Reset counter for new group
        # Concatenate 'Post Title' and 'Comment' if index is 0 or a multiple of 10
        if index % n_posts == 0:
            text_to_append = row['Post Title'] + " " + str(counter_to_read_outloud) + ". " + row['Comment']
        else:
            # Use only 'Comment' otherwise
            counter_to_read_outloud += 1
            text_to_append = str(counter_to_read_outloud) + ". " + row['Comment']
        # Append the text to the current string, with a space for separation
        text_list[current_list_index] += text_to_append + " "

    return text_list

reddit_list = concatenate_q_and_all_comments(df, 7)
reddit_list[0]


# In[95]:


def generate_ai_reading(text_to_use, index, char_limit, voice_id="pFZP5JQG7iQjIQuC4Bku"):
    # Max char limit of 100 characters
    char_limit = min(char_limit, 100)
    # Call ElevenLabs API to synthesize text
    audio = elevenlabs.generate(text=text_to_use[index][:char_limit], voice=voice_id)
    # Play the audio
    elevenlabs.play(audio)
    # with open('output.mp3', 'wb') as f:
    #     for chunk in audio.iter_content(chunk_size=char_limit):
    #         if chunk:
    #             f.write(chunk)
    # Save the audio
    elevenlabs.save(audio,'audio.mp3')
    # Print its been auto saved.
    print(f"MP3 file auto saved in: {os.getcwd()}")
    return


# In[96]:


# generate_ai_reading(reddit_list, 6, 10)


# In[97]:


# elevenlabs.play(audio)


# In[98]:


# elevenlabs.save(audio,'audio.wav')
# print(f"WAV file saved: {download_directory}")


# # Download Gameplay Videos to use as cover

# In[99]:


# # v1: Download 1 video
# import subprocess

# # Command to download a video
# command = ['yt-dlp', 'https://www.youtube.com/watch?v=YdoLTEZ1bI4']

# # Running the command
# subprocess.run(command)


# In[100]:


# # v2: Go to reddit and download gameplay videos
# # Choose the subreddit
# subreddit_name = "gameplayvideos"

# # Access the subreddit
# subreddit = reddit.subreddit(subreddit_name)

# # Of last 24 hours only.
# # top_posts = subreddit.top(time_filter='day', limit=10)
# # Fetch the top 10 posts from all time
# top_posts = subreddit.top(limit=10)

# # Initialize an empty list to store the data
# data = []

# # Iterate over the posts and comments
# for post in top_posts:
#     post_title = post.title
#     post_url = post.url
#     subreddit_name = post.subreddit.display_name

#     data.append([subreddit_name, post_title, post_url])
#     # post.comment_sort = 'top'  # Sort comments by top votes
#     # post.comments.replace_more(limit=0)  # Load all comments, remove 'more comments' links
#     # top_comments = post.comments.list()[:10]  # Get top 10 comments

#     # for comment in top_comments:
#     #     # Append each comment along with post and subreddit details to the data list
#     #     data.append([subreddit_name, post_title, post_url, comment.body])

# # Create a DataFrame
# df = pd.DataFrame(data, columns=['Subreddit', 'Post Title', 'Post URL'])
# df


# In[101]:


# # Directory where you want to save the downloaded videos
# original_path = r'C:\Users\kevin\Google Drive\My Drive\Github\Repos\reddit_text_to_speech\gameplay_videos'
# # Adding an extra '\' to every '\' found in the original path
# escaped_path = original_path.replace("\\", "\\\\")
# download_directory = escaped_path
# download_directory


# In[102]:


# for url in df['Post URL']:
#     command = [
#         'yt-dlp',
#         url,
#         '-o', os.path.join(download_directory, '%(title)s.%(ext)s')
#     ]
#     try:
#         subprocess.run(command, check=True)
#     except subprocess.CalledProcessError as e:
#         print(f"Failed to download {url}: {e}")


# # [WIP] Use Chatgpt API and Capcut API to generate video

# In[ ]:





#!/usr/bin/env python
# coding: utf-8

# In[1]:


import praw
import os
import pandas as pd
import re
import sys
sys.path.append('C:\\Users\\kevin\\Google Drive\\My Drive\\Github\\all-api-keys')
# Your code that operates in the new directory goes here
import secret

# # Reddit API Setup

# In[2]:



# In[3]:


reddit = praw.Reddit(client_id = secret.reddit_client_id,
                     client_secret=secret.reddit_secret_key,
                     user_agent=secret.reddit_app_name,
                     username=secret.reddit_username,
                     password=secret.reddit_password)


# # Pull Comments from Reddit Subreddits

# In[4]:


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


# In[5]:


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


# In[6]:


# # Apply remove_emojis function to all elements in the DataFrame
# df = df.applymap(remove_emojis)

# # This didnt work i saw an emoji:
# # for column in df.columns:
#     # df[column] = df[column].map(remove_emojis)


# In[7]:


# # Now you can export the DataFrame
# df.to_csv('reddit_data.csv', index=False, encoding='utf-16', sep='\t')


# # Function: Reddit to CSV

# In[8]:


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


# In[9]:


def df_to_csv(df):
    df.to_csv('reddit_data.csv', index=False, encoding='utf-16', sep='\t')
    return 'Complete!'


# In[10]:


df = reddit_to_df(subreddit_name="askreddit", time_filter='day', n_posts=10)
df


# In[11]:


df_to_csv(df)


# # Use ElevenLabs API to text-to-speech your df

# In[12]:


import elevenlabs
elevenlabs.set_api_key(secret.eleven_labs_api_key)


# In[13]:


mp3_file_path = r'C:\Users\kevin\Google Drive\My Drive\Github\Repos\reddit_text_to_speech\elevenlabs_audio'
# Adding an extra '\' to every '\' found in the original path
escaped_path = mp3_file_path.replace("\\", "\\\\")
download_directory = escaped_path
download_directory


# In[14]:


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


# In[15]:


# You need to load from csv cuz u havent cleaned the emojis from df above.
csv_file_path = 'reddit_data.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file_path, encoding='utf-16', sep='\t')
df[11:20]


# In[16]:


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


# In[18]:


import tkinter as tk
from tkinter import filedialog

class AudioHandler:
    def __init__(self):
        self.audio_data = None

    def generate_audio(self, text_to_use, index, char_limit, voice_id="pFZP5JQG7iQjIQuC4Bku"):
        # Generate and store audio data
        self.audio_data = elevenlabs.generate(text=text_to_use[index][:char_limit], voice=voice_id)

    def play_audio(self):
        if self.audio_data is not None:
            elevenlabs.play(self.audio_data)
        else:
            print("Audio data is not available.")

    def save_audio(self):
        """
        Show a save dialog to let the user choose where to save the audio file,
        then save the file as an MP3.
        """
        if self.audio_data is not None:
            root = tk.Tk()
            root.withdraw()  # We don't want a full GUI, so keep the root window from appearing
            # Show a "Save as" dialog and get the path to where the user wants to save the file
            file_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
            if not file_path:
                print("Save operation cancelled.")
                return
            # Save the audio file
            with open(file_path, 'wb') as f:
                f.write(self.audio_data)  # Corrected to use self.audio_data
            print(f"MP3 file saved in: {file_path}")
        else:
            print("Audio data is not available.")


# In[19]:


audio_handler = AudioHandler()
# audio_handler.generate_audio(reddit_list, 6, 10, voice_id="pFZP5JQG7iQjIQuC4Bku")


# In[20]:


# audio_handler.play_audio()


# In[21]:


# audio_handler.save_audio()


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





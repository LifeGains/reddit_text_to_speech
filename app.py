from flask import Flask, request, render_template, redirect, url_for, session, send_file

# We dont need to change this because the notebook increments.
import reddit_text_to_speech_v2_functionize  # This is the script converted from your Jupyter notebook
import pandas as pd
import sys
import os
sys.path.append('C:\\Users\\kevin\\Google Drive\\My Drive\\Github\\all-api-keys')
import secret

app = Flask(__name__)
# For production secret key defined as a environment variable
# Get the secret key from the environment variable
# 'default_secret_key' is only a placeholder value that will be replaced by whatever is in the render environment.
app.secret_key = os.environ.get('secret_key', 'default_secret_key')
# For local secret key
# app.secret_key = secret.flask_secret_key

@app.route('/')
def index():
    # Display the initial form to the user
    return render_template('index.html')

@app.route('/generate_table', methods=['POST'])
def generate_table():
    if request.method == 'POST':
        subreddit_name = request.form['subreddit_name']
        time_filter = request.form['time_filter']
        n_posts = request.form['n_posts']

        # Generate the DataFrame
        df = reddit_text_to_speech_v2_functionize.reddit_to_df(subreddit_name=subreddit_name, time_filter=time_filter, n_posts=int(n_posts))
        
        reddit_list = reddit_text_to_speech_v2_functionize.concatenate_q_and_all_comments(df, n_posts=int(n_posts))
        
        # Creating a DataFrame from the list
        df = pd.DataFrame(reddit_list, columns=['Content'])
        df.reset_index(inplace=True)
        df.rename(columns={'index': 'Index'}, inplace=True)
        
        # Convert the DataFrame to a JSON string and store it in the session
        session['df_json'] = df.to_json(orient='split')

        # Render the DataFrame as an HTML table and provide a way for the user to input an index
        return render_template('table.html', table=df.to_html(classes="table table-responsive"), subreddit_name=subreddit_name)
    else:
        return redirect(url_for('index'))

@app.route('/generate_audio', methods=['POST'])
def generate_audio():
    if request.method == 'POST' and 'df_json' in session:
        # Get the index from the user's input
        index = request.form['index']
        n_characters = request.form['n_characters']
        
        # Convert the JSON string back to a DataFrame
        df_json = session['df_json']
        df = pd.read_json(df_json, orient='split')

        # Convert the 'Content' column of the DataFrame back to a list
        content_list = df['Content'].tolist()
        
        # Generate the audio using the index
        reddit_text_to_speech_v2_functionize.generate_ai_reading(content_list, int(index), int(n_characters))
        return
    
        # Todo: Send to user specified path:
        # file_path = 'C:\\Users\\kevin\\Google Drive\\My Drive\\Github\\Repos\\reddit_text_to_speech\\your_audio_file.mp3'
        # return send_file(file_path, as_attachment=True)

    else:
        return redirect(url_for('index'))


# @app.route('/generate_audio_from_subreddit', methods=['POST'])
# def generate_audio_from_subreddit():
#     if request.method == 'POST':
#         subreddit_name = request.form['subreddit_name']
#         time_filter = request.form['time_filter']
#         n_posts = request.form['n_posts']

#         # Assuming your reddit_text_to_speech.reddit_to_df() function returns a pandas DataFrame
#         df = reddit_text_to_speech_v2_functionize.reddit_to_df(subreddit_name=subreddit_name, time_filter=time_filter, n_posts=int(n_posts))

#         reddit_list = reddit_text_to_speech_v2_functionize.concatenate_q_and_all_comments(df)
#         # Call your generate_ai_reading function with the form inputs
#         return reddit_text_to_speech_v2_functionize.generate_ai_reading(reddit_list, 0)
#     else:
#         # Render the form page again or handle as needed
#         return render_template('index.html')

app.run(host='0.0.0.0', port=5000)

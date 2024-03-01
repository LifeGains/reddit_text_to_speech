from flask import Flask, render_template
import reddit_text_to_speec  # This is the script converted from your Jupyter notebook
import pandas as pd

app = Flask(__name__)

@app.route('/')
# Confirmed to work.
# def index():
#     return "Hello World!"

def index():
    # Assuming your reddit_text_to_speech.reddit_to_df() function returns a pandas DataFrame
    df = reddit_text_to_speech.reddit_to_df(subreddit_name="askreddit", time_filter='day', n_posts=10)

    # Convert the DataFrame into HTML
    df_html = df.to_html()

    # Pass the HTML to your template, marking it as safe to render as HTML
    return render_template('index.html', data=df_html)

app.run(host='0.0.0.0', port=5000)

# if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000)
    # app.run(debug=True)

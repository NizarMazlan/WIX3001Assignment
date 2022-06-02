# Importing the libraries and packages
import streamlit as st  
from textblob import TextBlob
from gingerit.gingerit import GingerIt
import pandas as pd
import altair as alt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


# 
def convert_to_df(sentiment):
    sentiment_dict = {'polarity':sentiment.polarity,'subjectivity':sentiment.subjectivity}
    sentiment_df = pd.DataFrame(sentiment_dict.items(),columns=['metric','value'])
    return sentiment_df

def analyze_token_sentiment(docx):
	analyzer = SentimentIntensityAnalyzer()
	pos_list = []
	neg_list = []
	neu_list = []
	for i in docx.split():
		res = analyzer.polarity_scores(i)['compound']
		if res > 0.1:
			pos_list.append(i)
			pos_list.append(res)

		elif res <= -0.1:
			neg_list.append(i)
			neg_list.append(res)
		else:
			neu_list.append(i)

	result = {'positives':pos_list,'negatives':neg_list,'neutral':neu_list}
	return result 

def main():
    menu = ["Home","Sentiment Analysis", "DIY-Grammarly"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home": # Home page for introduction to the website
        st.title("Nizar's Soft Computing Assignment")
        st.subheader("Hello, in this web app created by Mohamad Nizar Mustaqeem (17206540) for his WIX3001 Individual Assignment")
        st.subheader("Objectives : ")
        st.write("To determine a sentence is positive or negative")
        st.write("To examine whether grammar of the sentence is correct")

    elif choice == "Sentiment Analysis": # for the positive or negative sentence
        st.title("Sentiment Analysis")
        st.write("To clarify some things, Polarity refers to the strength of an opinion. It could be positive or negative. Meanwhile, Subjectivity refers to the degree to which a person is personally involved in an object. What matters the most here are personal connections and individual experiences with that object, which may or may not differ from someone else’s point of view.")
        with st.form(key = 'nlpForm'):
            raw_text = st.text_area("Enter your sentence here")
            submit_button = st.form_submit_button(label = 'Analyze')

            #Layout
            col1,col2 = st.columns(2)
            if submit_button:
                with col1:
                    st.info("Results")
                    sentiment = TextBlob(raw_text).sentiment

                    # Emoji for the results
                    if sentiment.polarity > 0:
                        st.markdown("The sentence is Positive :smiley: ")
                    elif sentiment.polarity < 0:
                        st.markdown("The sentence is Negative :angry: ")
                    else:
                        st.markdown("The sentence is Neutral 😐 ")


                    # Dataframe
                    result_df = convert_to_df(sentiment)
                    st.dataframe(result_df)

                    # Visualization of polarity and subjectivity 
                    c = alt.Chart(result_df).mark_bar().encode(
                        x='metric',
                        y='value',
                        color='metric')
                    st.altair_chart(c,use_container_width=True)

                with col2: 
                    st.info("Token Sentiment")

                    token_sentiments = analyze_token_sentiment(raw_text)
                    st.write(token_sentiments)

    # The grammar corrector
    elif choice == "DIY-Grammarly":
        st.title("DIY-Grammarly")
        st.write("This is where you will enter a text, try to enter a sentence that has a grammatical error. It will tell you whether it is correct and give and output of the corrected sentence")

        text = st.text_area("Enter Text:", value='', height=None, max_chars=None, key=None)
        parser = GingerIt()
        if st.button('Correct Sentence'):
            if text == '':
                st.write('Please enter text for checking') 
            else: 
		result_dict = parser.parse(text)
                if text == str(result_dict["result"]):
                    st.write("The grammar for this sentence is CORRECT ✅")
                else:
                    st.write("The grammar for this sentence in INCORRECT ⛔")
            
                st.markdown('**Corrected Sentence - ** ' + str(result_dict["result"]))

        else: pass

if __name__ == '__main__':
    main()

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from wordcloud import WordCloud

# Load data
rating = 4000
br = pd.read_csv(r"C:\Users\Vincent\Documents\DSA PROJECTS\SENTIMENT\Books_rating.csv")
bd = pd.read_csv(r"C:\Users\Vincent\Documents\DSA PROJECTS\SENTIMENT\books_data.csv")
books = pd.merge(br, bd, on='Title')

# Prepare DataFrame
df = books[['Title', 'review/score', 'review/text', 'authors', 'categories', 'ratingsCount']]
df.drop_duplicates(inplace=True)
df.dropna(inplace=True)

# Sample data
data = df.sample(5000, random_state=1)

# Standardize titles, authors, and categories
data['Title'] = data['Title'].str.strip().str.lower()
data['authors'] = data['authors'].str.extract(r'\'(.*)\'')[0].str.strip().str.lower()
data['categories'] = data['categories'].str.extract(r'\'(.*)\'')[0].str.strip().str.lower()
data['review/text'] = data['review/text'].str.strip()
data['word_count'] = data['review/text'].apply(lambda x: len(x.split(' ')))

# Sentiment Analysis
def sentiment_analysis(data):
    vader = SentimentIntensityAnalyzer()
    data['clean_reviews'] = data['review/text'].str.lower()
    data['score'] = data['clean_reviews'].apply(lambda review: vader.polarity_scores(review))
    data['compound'] = data['score'].apply(lambda score_dict: score_dict['compound'])
    data['Sentiment'] = data['compound'].apply(lambda c: 'positive' if c > 0 else ('negative' if c < 0 else 'neutral'))
    return data

data = sentiment_analysis(data)

# Function to show distribution based on user-selected genres
def show_genre_distribution():
    plt.figure(figsize=(7,7))
    top_categories = data['categories'].value_counts().head(10)
    labels = top_categories.index
    sizes = top_categories.values
    plt.pie(sizes, explode=(0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0), labels=labels, autopct='%1.1f%%', shadow=True)
    plt.title('Distribution of Books Based on Genre', fontsize=20)
    plt.axis('off')
    plt.legend()
    plt.show()

# Function to show most frequent words in reviews for a selected book
def show_most_frequent_words(book_title):
    book_title = book_title.strip().lower()
    book_reviews = data[data['Title'] == book_title]['review/text']
    all_words = ' '.join(book_reviews).split()
    
    if not all_words:
        print(f"No reviews found for the book titled '{book_title}'.")
        return
    
    wordcloud = WordCloud(width=500, height=500, background_color='white').generate(' '.join(all_words))
    plt.figure(figsize=(7, 7))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(f'Most Frequent Words in Reviews for {book_title}', fontsize=20)
    plt.show()

# Function to show 5 better and 5 worse rated books than a current book in its genre
def compare_books_in_genre(book_title):
    book_title = book_title.strip().lower()
    if book_title not in data['Title'].values:
        print(f"No book found with title '{book_title}'")
        return
    
    book_info = data[data['Title'] == book_title].iloc[0]
    genre = book_info['categories']
    book_score = book_info['review/score']
    
    genre_books = data[data['categories'] == genre]
    better_books = genre_books[genre_books['review/score'] > book_score].sort_values(by='review/score').head(5)
    worse_books = genre_books[genre_books['review/score'] < book_score].sort_values(by='review/score', ascending=False).head(5)
    
    print(f"Books better rated than '{book_title}' in '{genre}' genre:")
    print(better_books[['Title', 'review/score']])
    
    print(f"\nBooks worse rated than '{book_title}' in '{genre}' genre:")
    print(worse_books[['Title', 'review/score']])
    
    # Visualization
    plt.figure(figsize=(10, 6))
    plt.barh(better_books['Title'], better_books['review/score'], color='green', label='Better Rated')
    plt.barh(worse_books['Title'], worse_books['review/score'], color='red', label='Worse Rated')
    plt.axvline(x=book_score, color='blue', linestyle='--', label=f'{book_title} Score')
    plt.xlabel('Rating Score')
    plt.title(f'Comparison of Ratings in {genre} Genre for {book_title}')
    plt.legend()
    plt.show()

# Function to show average rating of a selected book and compare it against its genre
def compare_book_rating(book_title):
    book_title = book_title.strip().lower()
    if book_title not in data['Title'].values:
        print(f"No book found with title '{book_title}'")
        return
    
    book_info = data[data['Title'] == book_title].iloc[0]
    genre = book_info['categories']
    book_score = book_info['review/score']
    
    genre_avg_rating = data[data['categories'] == genre]['review/score'].mean()
    
    print(f"Average rating of '{book_title}': {book_score}")
    print(f"Average rating in '{genre}' genre: {genre_avg_rating}")
    
    # Visualization
    plt.figure(figsize=(6, 4))
    plt.bar(['Book Rating', 'Genre Average Rating'], [book_score, genre_avg_rating], color=['blue', 'orange'])
    plt.ylabel('Rating Score')
    plt.title(f'Average Rating Comparison for {book_title}')
    plt.show()

# Function to show 5 better and 5 worse rated authors than the current book's author in its genre
def compare_authors_in_genre(book_title):
    book_title = book_title.strip().lower()
    if book_title not in data['Title'].values:
        print(f"No book found with title '{book_title}'")
        return
    
    book_info = data[data['Title'] == book_title].iloc[0]
    genre = book_info['categories']
    author = book_info['authors']
    
    genre_authors = data[data['categories'] == genre].groupby('authors')['review/score'].mean()
    author_rating = genre_authors.get(author)
    
    if pd.isna(author_rating):
        print(f"No ratings found for author '{author}' in '{genre}' genre")
        return
    
    better_authors = genre_authors[genre_authors > author_rating].sort_values().head(5)
    worse_authors = genre_authors[genre_authors < author_rating].sort_values(ascending=False).head(5)
    
    print(f"Authors better rated than '{author}' in '{genre}' genre:")
    print(better_authors)
    
    print(f"\nAuthors worse rated than '{author}' in '{genre}' genre:")
    print(worse_authors)
    
    # Visualization
    plt.figure(figsize=(10, 6))
    plt.barh(better_authors.index, better_authors.values, color='green', label='Better Rated')
    plt.barh(worse_authors.index, worse_authors.values, color='red', label='Worse Rated')
    plt.axvline(x=author_rating, color='blue', linestyle='--', label=f'{author} Score')
    plt.xlabel('Rating Score')
    plt.title(f'Comparison of Authors in {genre} Genre for {author}')
    plt.legend()
    plt.show()

# Function to show distribution of sentiment in the selected book genre and compare to the book
def compare_sentiment_in_genre(book_title):
    book_title = book_title.strip().lower()
    if book_title not in data['Title'].values:
        print(f"No book found with title '{book_title}'")
        return
    
    book_info = data[data['Title'] == book_title].iloc[0]
    genre = book_info['categories']
    
    genre_data = data[data['categories'] == genre]
    
    # Sentiment distribution in genre
    sentiment_counts = genre_data['Sentiment'].value_counts()
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', shadow=True)
    plt.title(f'Sentiment Distribution in {genre} Genre')
    
    # Sentiment comparison for the book
    book_sentiments = data[data['Title'] == book_title]['Sentiment'].value_counts()
    plt.subplot(1, 2, 2)
    plt.pie(book_sentiments, labels=book_sentiments.index, autopct='%1.1f%%', shadow=True)
    plt.title(f'Sentiment Distribution for {book_title}')
    plt.show()

# Function to show 5 better and 5 worse sentiment rated books in its genre
def compare_sentiment_books_in_genre(book_title):
    book_title = book_title.strip().lower()
    if book_title not in data['Title'].values:
        print(f"No book found with title '{book_title}'")
        return
    
    book_info = data[data['Title'] == book_title].iloc[0]
    genre = book_info['categories']
    book_sentiment = book_info['compound']
    
    genre_books = data[data['categories'] == genre]
    better_books = genre_books[genre_books['compound'] > book_sentiment].sort_values(by='compound').head(5)
    worse_books = genre_books[genre_books['compound'] < book_sentiment].sort_values(by='compound', ascending=False).head(5)
    
    print(f"Books with better sentiment than '{book_title}' in '{genre}' genre:")
    print(better_books[['Title', 'compound']])
    
    print(f"\nBooks with worse sentiment than '{book_title}' in '{genre}' genre:")
    print(worse_books[['Title', 'compound']])
    
    # Visualization
    plt.figure(figsize=(10, 6))
    plt.barh(better_books['Title'], better_books['compound'], color='green', label='Better Sentiment')
    plt.barh(worse_books['Title'], worse_books['compound'], color='red', label='Worse Sentiment')
    plt.axvline(x=book_sentiment, color='blue', linestyle='--', label=f'{book_title} Sentiment')
    plt.xlabel('Sentiment Score')
    plt.title(f'Comparison of Sentiments in {genre} Genre for {book_title}')
    plt.legend()
    plt.show()

# Example usage:
show_genre_distribution()
show_most_frequent_words('harry potter and the sorcerer\'s stone')
compare_books_in_genre('harry potter and the sorcerer\'s stone')
compare_book_rating('harry potter and the sorcerer\'s stone')
compare_authors_in_genre('harry potter and the sorcerer\'s stone')
compare_sentiment_in_genre('harry potter and the sorcerer\'s stone')
compare_sentiment_books_in_genre('harry potter and the sorcerer\'s stone')


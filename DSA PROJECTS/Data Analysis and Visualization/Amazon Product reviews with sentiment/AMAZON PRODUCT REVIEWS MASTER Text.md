# **Book Review Sentiment Analysis - Python Script**

This Python script performs sentiment analysis on book reviews, provides various visualizations, and compares books, authors, and sentiments within different genres. It leverages libraries such as Pandas, NumPy, Seaborn, Matplotlib, VADER Sentiment, and WordCloud for data processing and visualization.

## **Features**

- **Data Preparation**:
  - Merges and processes book rating and book data.
  - Standardizes titles, authors, and categories.
  - Samples data for analysis.

- **Sentiment Analysis**:
  - Uses VADER Sentiment Analysis to analyze the sentiment of book reviews.
  - Classifies reviews as positive, negative, or neutral based on sentiment scores.

- **Visualizations**:
  - Shows distribution of books based on genre.
  - Generates word clouds for the most frequent words in reviews of a selected book.
  - Compares ratings of books and authors within the same genre.
  - Compares sentiment distribution within genres and for specific books.

- **Comparison Functions**:
  - Compares a selected book's rating and sentiment with other books in the same genre.
  - Compares the rating of a book's author with other authors in the same genre.
  - Shows better and worse-rated books and authors in a selected genre.

[!IMPORTANT]
**BEFORE INSTALLATION**
install the libraries, you can use the following command:
pip install pandas numpy seaborn matplotlib vaderSentiment wordcloud

Remember to download books_data.csv from Kaggle from https://www.kaggle.com/datasets/mohamedbakhet/amazon-books-reviews

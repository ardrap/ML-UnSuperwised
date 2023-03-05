# -*- coding: utf-8 -*-
"""Tweet_NLP.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nk_yLo3462gqv9Mj9c2uvq1eSGMMEgqH
"""

# import packages
import numpy as np
import pandas as pd
import re
import seaborn as sns
import matplotlib.pyplot as plt
import nltk
from nltk.stem import WordNetLemmatizer

# data load
df=pd.read_csv("/content/twitter_validation (1).csv",encoding="ISO-8859-1",header=None)
df

# header
df.columns=['Id','Location','Target','Text']
df

df.head()

df.tail()

df.shape

df['Location'].value_counts()

df.isna().sum()

sns.countplot(x='Location',data=df)

df['Target'].value_counts

sns.countplot(x='Target',data=df)

# delete irrelevent from target
# delete id,location
df.drop(df.index[(df['Target']=='Irrelevant')],axis=0,inplace=True)
df

df.shape

df.tail(10)

# reset index
df.reset_index(drop=True,inplace=True)
df

df.tail(10)

df.drop(['Id','Location'],axis=1,inplace=True)
df

# target
# positive - 1
# negative - -1
# neutral - 0

df['Target']=df['Target'].map({'Positive':1,'Negative':-1,'Neutral':0})
df

nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('punkt')

tweets=df.Text
tweets

from nltk import TweetTokenizer
tk=TweetTokenizer()
tweets=tweets.apply(lambda x:tk.tokenize(x)).apply(lambda x:" ".join(x))  #second lambda:to join each x with space
tweets

# RE :  want to skip
str1='Wonderfull @peacock !!!'
str2=re.sub('[^a-z]'," ",str1)
str3=re.sub('[^A-Z]'," ",str1)
str2
# str3

# remove special characters using RE
tweets=tweets.str.replace('[^a-zA-Z0-9]+',' ')  # ^ -> except(ozzhikae) , + -> combinations
tweets

# chara length above >= 3(tokenize)
from nltk.tokenize import word_tokenize
tweets=tweets.apply(lambda x:' '.join([w for w in word_tokenize(x) if len(w)>=3]))
tweets

from nltk.stem import SnowballStemmer
sb=SnowballStemmer('english')
tweets=tweets.apply(lambda x:[sb.stem(i.lower()) for i in tk.tokenize(x)]).apply(lambda x:' '.join(x))
tweets

# for i in tweets:
  # print(sb.stem(i.lower()))

# stopwords
# how to import stopwords
nltk.download('stopwords')
from nltk.corpus import stopwords
stop=stopwords.words('english')
stop

tweets=tweets.apply(lambda x:[i for i in tk.tokenize(x) if i not in stop]).apply(lambda x:' '.join(x))
tweets

# vectorization
from sklearn.feature_extraction.text import TfidfVectorizer
vector=TfidfVectorizer()

train_data=vector.fit_transform(tweets)
train_data

train_data.shape

# input :train_data
# output :target
y=df['Target'].values
y

from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(train_data,y,test_size=0.30,random_state=42)
x_train

x_test

y_train

y_test

# model creation
# SVM classifier Algorithm

from sklearn.svm import SVC
classifier=SVC()
classifier.fit(x_train,y_train)

y_pred1=classifier.predict(x_test)
y_pred1

# accuracy
from sklearn.metrics import classification_report,accuracy_score,confusion_matrix,ConfusionMatrixDisplay
result1=confusion_matrix(y_pred1,y_test)
result1

print(classification_report(y_pred1,y_test))

score1=accuracy_score(y_pred1,y_test)
score1

print(ConfusionMatrixDisplay.from_predictions(y_pred1,y_test))

# naive_bayes
from sklearn.naive_bayes import MultinomialNB
classifier=MultinomialNB()
classifier.fit(x_train,y_train)

y_pred2=classifier.predict(x_test)
y_pred2

# accuracy
from sklearn.metrics import classification_report,accuracy_score,ConfusionMatrixDisplay,confusion_matrix
result2=confusion_matrix(y_pred2,y_test)
result2

print(classification_report(y_pred2,y_test))

score2=accuracy_score(y_pred2,y_test)
score2

print(ConfusionMatrixDisplay.from_predictions(y_pred2,y_test))

# decision_tree
from sklearn.tree import DecisionTreeClassifier
classifier=DecisionTreeClassifier(criterion='entropy')
classifier.fit(x_train,y_train)

y_pred3=classifier.predict(x_test)
y_pred3

# accuracy
from sklearn.metrics import classification_report,accuracy_score,ConfusionMatrixDisplay,confusion_matrix
result3=confusion_matrix(y_pred3,y_test)
result3

print(classification_report(y_pred3,y_test))

score3=accuracy_score(y_pred3,y_test)
score3

print(ConfusionMatrixDisplay.from_predictions(y_pred3,y_test))
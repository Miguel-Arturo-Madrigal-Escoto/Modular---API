import pandas as pd
from rake_nltk import Rake
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from authentication.models import Company
from roles.models import CompanyRoles

# flake8: noqa

class NlpAlgorithm:
    def __init__(self) -> None:
        # Uses stopwords for spanish from NLTK, and all puntuation characters.
        self.r = Rake()
        # self.r = Rake(language='spanish')

    def df_company(self):
        df = pd.DataFrame(list(Company.objects.all().values('id', 'name', 'about', 'mission', 'vision', 'location')))
        df.to_csv('companies.csv', encoding='utf-8')

        # ! Keywords dataframe column
        df['Key_words'] = ''

        # Iterate over the rows of the df
        for index, row in df.iterrows():
            # mission -> columna con toda la data relevante
            # each row is a different company

            print('keywords from text: ', self.r.extract_keywords_from_text(row['mission']))   # to extract key words
            key_words_dict_scores = self.r.get_word_degrees()    # to get dictionary with key words and their similarity scores

            print('scores: ', key_words_dict_scores)
            df.at[index,'Key_words'] = list(key_words_dict_scores.keys())   # to assign it to new column

        # to combine 4 lists (4 columns) of key words into 1 sentence under Bag_of_words column
        df['Bag_of_words'] = ''
        columns = ['about', 'mission',  'vision', 'location']

        for index, row in df.iterrows():
            words = ''
            for col in columns:
                print('xd: ', row[col])
                words += row[col] + ' '
            df.at[index,'Bag_of_words'] = words
            # print('bow: ', row['Bag_of_words'])


        # strip white spaces infront and behind, replace multiple whitespaces (if any)
        df['Bag_of_words'] = df['Bag_of_words'].str.strip().str.replace('   ', ' ').str.replace('  ', ' ')

        df = df[['id', 'name', 'Bag_of_words']]
        #print(df)
        df.to_csv('bag_of_words_3.csv', encoding='utf-8')

        # bag of words (frecuency) of all the rows
        count = CountVectorizer()
        count_matrix = count.fit_transform(df['Bag_of_words'])
        # print('count_matrix', count_matrix.toarray())

        cosine_sim = cosine_similarity(count_matrix, count_matrix)
        # print(cosine_sim)

        indices = pd.Series(df['name'])
        print(indices)



    def df_company_roles(self):
        df = pd.DataFrame(list(CompanyRoles.objects.all().values()))
        df.to_csv('company_roles.csv', encoding='utf-8')
        print(df.describe().T)

    def to_df(self):
        pass

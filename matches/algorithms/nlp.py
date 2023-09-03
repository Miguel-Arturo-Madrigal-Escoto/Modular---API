from collections import OrderedDict

import pandas as pd
from django.db.models import Case, When
from rake_nltk import Rake
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from authentication.models import Company, User
from roles.models import CompanyRoles

# flake8: noqa

class NlpAlgorithm:
    def __init__(self) -> None:
        # Uses stopwords for spanish from NLTK, and all puntuation characters.
        # self.r = Rake()
        self.r = Rake(language='spanish')

    def df_company(self, user, string_to_match: str):
        df = pd.DataFrame(list(Company.objects.all().values('id', 'name', 'about', 'mission', 'vision', 'location')))

        all_roles = {}
        for company in Company.objects.all():
            all_roles[company.id] = ''

        for role in CompanyRoles.objects.all():
            string = f'{ role.name } { role.description } { role.role.position }'
            all_roles[role.company_id] = all_roles.get(role.company_id, '') + string

        all_roles = OrderedDict(sorted(all_roles.items()))
        for i, company in enumerate(Company.objects.all()):
            df.at[i, 'roles'] = all_roles.get(i+1)
        df.to_csv('companies.csv', encoding='utf-8')
        # ! Keywords dataframe column
        df['Key_words'] = ''
        df['new_mission'] = ''
        df['new_vision'] = ''
        df['new_about'] = ''
        df['new_roles'] = ''

        # Iterate over the rows of the df
        for index, row in df.iterrows():
            # mission -> columna con toda la data relevante
            # each row is a different company
            self.r.extract_keywords_from_text(row['mission'])
            df.at[index,'new_mission'] = ' '.join(list(self.r.get_word_degrees().keys()))

            self.r.extract_keywords_from_text(row['vision'])
            df.at[index,'new_vision'] = ' '.join(list(self.r.get_word_degrees().keys()))

            self.r.extract_keywords_from_text(row['about'])
            df.at[index,'new_about'] = ' '.join(list(self.r.get_word_degrees().keys()))

            self.r.extract_keywords_from_text(row['roles'])
            df.at[index,'new_roles'] = ' '.join(list(self.r.get_word_degrees().keys()))
            # print('keywords from text: ', self.r.extract_keywords_from_text(row['mission']))   # to extract key words
            # key_words_dict_scores = self.r.get_word_degrees()    # to get dictionary with key words and their similarity scores

            # df.at[index,'new_vision'] = list(new_vision.keys())
            # df.at[index,'new_about'] = list(new_about.keys())
            # print('scores: ', key_words_dict_scores)
            # df.at[index,'Key_words'] = list(key_words_dict_scores.keys())   # to assign it to new column

        # to combine 4 lists (4 columns) of key words into 1 sentence under Bag_of_words column
        df['Bag_of_words'] = ''
        columns = ['new_about', 'new_mission', 'new_vision', 'new_roles', 'location']

        for index, row in df.iterrows():
            words = ''
            for col in columns:
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

        #user_count_matrix = count.fit_transform(string_to_match.split())
        # print(user_count_matrix) # programmer C++
        # count_matrix = count.fit_transform(df['Bag_of_words'])
        sparse_matrix = count.fit_transform([string_to_match]+df['Bag_of_words'].to_list())
        cos = cosine_similarity(sparse_matrix[0, :], sparse_matrix[1:, :])

        # list of recommended ids
        recommended_company_ids = self.recommend_companies(df, cosine_sim=cos)
        preserved_order = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(recommended_company_ids)])
        recommended_companies = Company.objects.filter(id__in=recommended_company_ids).order_by(preserved_order).values()
        print(recommended_company_ids)
        # 2 3 1



    def recommend_companies(self, df, cosine_sim):
        recommended_companies = []
        score_series = pd.Series(cosine_sim[0]).sort_values(ascending = False)
        top_10_indices = list(score_series.iloc[0:10].index)

        for i in top_10_indices:
            recommended_companies.append(list(df['id'])[i])

        return recommended_companies

    def df_company_roles(self):
        df = pd.DataFrame(list(CompanyRoles.objects.all().values()))
        df.to_csv('company_roles.csv', encoding='utf-8')
        #print(df.describe().T)

    def to_df(self):
        pass

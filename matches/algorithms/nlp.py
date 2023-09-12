from collections import OrderedDict

import pandas as pd
from django.db.models import Case, Q, When
from rake_nltk import Rake
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from authentication.models import BaseUser, Company, User
from experience.models import Experience
from matches.models import Match
from roles.models import CompanyRoles
from skills.models import Skill

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
        df.to_csv('bag_of_words_company.csv', encoding='utf-8')

        # bag of words (frecuency) of all the rows
        count = CountVectorizer()

        #user_count_matrix = count.fit_transform(string_to_match.split())
        # print(user_count_matrix) # programmer C++
        # count_matrix = count.fit_transform(df['Bag_of_words'])
        sparse_matrix = count.fit_transform([string_to_match]+df['Bag_of_words'].to_list())
        cos = cosine_similarity(sparse_matrix[0, :], sparse_matrix[1:, :])

        # list of recommended ids
        recommended_company_ids = self.recommend_companies(df, cosine_sim=cos)
        preserved_order = Case(*[When(company=pk, then=pos) for pos, pk in enumerate(recommended_company_ids)])
        recommended_companies = BaseUser.objects.filter(company__in=recommended_company_ids).order_by(preserved_order)
        return recommended_companies
        # 2 3 1

    def df_user(self, company, string_to_match: str):
        df = pd.DataFrame(list(User.objects.all().values('id', 'name', 'lastname', 'position', 'expected_salary', 'modality', 'location', 'about')))

        all_skills = {}
        for user in Skill.objects.all():
            all_skills[user.id] = ''

        for skill in Skill.objects.all():
            string = f'{ skill.name } { skill.description}'
            all_skills[skill.user_id] = all_skills.get(skill.user_id, '') + string

        all_experiences = {}
        for user in Experience.objects.all():
            all_experiences[user.id] = ''

        for experience in Experience.objects.all():
            string = f'{ experience.description } { experience.role.position  }'
            all_experiences[experience.user_id] = all_experiences.get(experience.user_id, '') + string

        all_skills = OrderedDict(sorted(all_skills.items()))
        all_experiences = OrderedDict(sorted(all_experiences.items()))
        for i, user in enumerate(User.objects.all()):
            df.at[i, 'skills'] = all_skills.get(i+1)
            df.at[i, 'experiences'] = all_experiences.get(i+1)

        df.to_csv('users.csv', encoding='utf-8')
        # ! Keywords dataframe column
        df['Key_words'] = ''
        df['new_position'] = ''
        df['new_about'] = ''
        df['new_experiences'] = ''
        df['new_skills'] = ''


        # Iterate over the rows of the df
        for index, row in df.iterrows():
            # mission -> columna con toda la data relevante
            # each row is a different company
            #self.r.extract_keywords_from_text(row['position'])
            #df.at[index,'new_position'] = ' '.join(list(self.r.get_word_degrees().keys()))
            self.r.extract_keywords_from_text(row['about'])
            df.at[index,'new_about'] = ' '.join(list(self.r.get_word_degrees().keys()))

            self.r.extract_keywords_from_text(row['experiences'] if row['experiences'] else '')
            df.at[index,'new_experiences'] = ' '.join(list(self.r.get_word_degrees().keys()))

            self.r.extract_keywords_from_text(row['skills'] if row['skills'] else '')
            df.at[index,'new_skills'] = ' '.join(list(self.r.get_word_degrees().keys()))

            # print('keywords from text: ', self.r.extract_keywords_from_text(row['mission']))   # to extract key words
            # key_words_dict_scores = self.r.get_word_degrees()    # to get dictionary with key words and their similarity scores

            # df.at[index,'new_vision'] = list(new_vision.keys())
            # df.at[index,'new_about'] = list(new_about.keys())
            # print('scores: ', key_words_dict_scores)
            # df.at[index,'Key_words'] = list(key_words_dict_scores.keys())   # to assign it to new column

        # to combine 4 lists (4 columns) of key words into 1 sentence under Bag_of_words column
        df['Bag_of_words'] = ''
        columns = ['new_about', 'new_experiences', 'new_skills', 'expected_salary', 'modality', 'location']

        for index, row in df.iterrows():
            words = ''
            for col in columns:
                words += str(row[col]) + ' '
            df.at[index,'Bag_of_words'] = words
            # print('bow: ', row['Bag_of_words'])


        # strip white spaces infront and behind, replace multiple whitespaces (if any)
        df['Bag_of_words'] = df['Bag_of_words'].str.strip().str.replace('   ', ' ').str.replace('  ', ' ')

        df = df[['id', 'name', 'lastname', 'Bag_of_words']]
        #print(df)
        df.to_csv('bag_of_words_user.csv', encoding='utf-8')

        # bag of words (frecuency) of all the rows
        count = CountVectorizer()

        #user_count_matrix = count.fit_transform(string_to_match.split())
        # print(user_count_matrix) # programmer C++
        # count_matrix = count.fit_transform(df['Bag_of_words'])
        sparse_matrix = count.fit_transform([string_to_match]+df['Bag_of_words'].to_list())
        cos = cosine_similarity(sparse_matrix[0, :], sparse_matrix[1:, :])

        # list of recommended ids
        recommended_user_ids = self.recommend_users(df, company,cosine_sim=cos)

        preserved_order = Case(*[When(user=pk, then=pos) for pos, pk in enumerate(recommended_user_ids)])

        print(preserved_order)

        recommended_users = BaseUser.objects.filter(user__in=recommended_user_ids).order_by(preserved_order)
        return recommended_users

    def recommend_companies(self, df, cosine_sim):
        recommended_companies = []

        # Quitar perfiles con los que se ha interactuado

        score_series = pd.Series(cosine_sim[0]).sort_values(ascending = False)
        top_10_indices = list(score_series.iloc[0:10].index)

        for i in top_10_indices:
            recommended_companies.append(list(df['id'])[i])

        return recommended_companies

    def recommend_users(self, df, company, cosine_sim):
        recommended_users = []

        # Quitar perfiles con los que se ha interactuado
        interacted_matches = Match.objects.filter(company_like__isnull=False, company=company).values_list('user_id', flat=True).distinct()
        # interacted_matches = [2, 34, 5]

        # con los que no ha interactuado
        df = df[~df['id'].isin(interacted_matches)]

        # iterando fila por fila
        #   id
        #   1 in [2, 34, 5] => False => True
        #   3 in [2, 34, 5] => False => True

        unordered_score_series = pd.Series(cosine_sim[0])
        unordered_score_series_frame = unordered_score_series.to_frame(name='score')
        unordered_score_series_frame.index = unordered_score_series_frame.index + 1

        df = df.merge(unordered_score_series_frame, left_on='id', right_index=True, how='inner')
        df = df.sort_values(by='score', ascending=False)

        if df.empty:
            return []

        recommended_users = df['id'].values.tolist()

        return recommended_users

    def df_company_roles(self):
        df = pd.DataFrame(list(CompanyRoles.objects.all().values()))
        df.to_csv('company_roles.csv', encoding='utf-8')
        #print(df.describe().T)

    def to_df(self):
        pass

import warnings
from collections import OrderedDict

import pandas as pd
from django.db.models import Case, When
from rake_nltk import Rake
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from authentication.models import BaseUser, Company, User
from experience.models import Experience
from matches.models import Match
from roles.models import CompanyRoles
from skills.models import Skill

warnings.simplefilter(action='ignore', category=FutureWarning)

# flake8: noqa

class NlpAlgorithm:
    def __init__(self) -> None:
        # Uses stopwords for spanish from NLTK, and all puntuation characters.
        # self.r = Rake()
        self.r = Rake(language='spanish')


    def generateNLPRecommendations(self, obj, target_str: str):
        """
        Preprocesses user or company profiles for NLP-based recommendation generation by extracting key information, 
        performing keyword analysis, and calculating profile similarity scores to provide personalized recommendations

        Args:
            obj (User or Company): The user or company object for which data is being processed.
            target_str (str): The target string for similarity comparison.

        Returns:
            recommendations (list): A list of recommended user or company profiles based on similarity to the target string.
        """
        user_fields = ('id', 'name', 'lastname', 'position__position', 'expected_salary', 'modality', 'location', 'about')
        company_fields = ('id', 'name', 'about', 'mission', 'vision', 'location')
        is_user = isinstance(obj, User)
        Model = Company if is_user else User

        df = pd.DataFrame(list(Model.objects.all().values(*(company_fields if is_user else (user_fields)))))

        cols_to_extract = []
        base_cols = []

        if is_user:
            cols_to_extract = ['new_mission', 'new_vision', 'new_about', 'new_roles']
            base_cols = ['location', 'bag_of_words']
            self.add_company_data_to_df(df)
            for col in cols_to_extract:
                df[col] = ''
            self.keywords_extraction_from_text(df, cols_to_extract)
        else:
            cols_to_extract = ['new_position__position', 'new_about', 'new_experiences', 'new_skills']
            base_cols = ['expected_salary', 'modality', 'location', 'bag_of_words']
            self.add_user_data_to_df(df)
            for col in cols_to_extract:
                df[col] = ''
            self.keywords_extraction_from_text(df, cols_to_extract)

        df['bag_of_words'] = ''

        self.fill_bag_of_words(df, cols_to_extract+base_cols)
        cosine_sim = self.cosine_similarity_algorithm(df, target_str)
        df.to_csv('current_bag_of_words.csv')

        recommended_ids = self.recommend(df, obj, cosine_sim)

        return self.sorted_recommendations(is_user, recommended_ids)


    def sorted_recommendations(self, is_user, recommended_ids):
        """
        This method sorts recommendations based on cosine similarity. Depending on whether obj is a user (User) or a company (Company), recommendations are sorted appropriately.

        Args:
            is_user (boolean): A boolean indicating whether obj is a user (User).
            recommended_ids (list): A list of recommended IDs (BaseUser ID).

        Returns:
            recommendations (list): List of recommendations sorted by similarity.
        """

        recommendations = []
        if is_user:
            preserved_order_ids = Case(*[When(company=pk, then=pos) for pos, pk in enumerate(recommended_ids)])
            recommendations = BaseUser.objects.filter(company__in=recommended_ids).order_by(preserved_order_ids)
        else:
            preserved_order_ids = Case(*[When(user=pk, then=pos) for pos, pk in enumerate(recommended_ids)])
            recommendations = BaseUser.objects.filter(user__in=recommended_ids).order_by(preserved_order_ids)
        return recommendations


    def cosine_similarity_algorithm(self, df, target_str):
        """
        Constructs the vocabulary (set of unique words) using all of the content
        in count.fit_transform() method. Then, a matrix is built by relying on the
        times that a word appear for every document.

        Args:
            df (pd.DataFrame): the dataframe that contains the users/companies content + bag of words
            target_str (str): the entire user|company string (with all the information in it).

        Returns:
            cosine_sim (pd.ndarray): a pandas array/matrix that contains the result of the comparison
            between the users|company data (dataframe) and the auth user info (target_str).
        """
        # bag of words (frecuency) of all the rows
        count = CountVectorizer()

        sparse_matrix = count.fit_transform([target_str]+df['bag_of_words'].to_list())
        cos = cosine_similarity(sparse_matrix[0, :], sparse_matrix[1:, :])
        return cos


    def fill_bag_of_words(self, df, columns):
        """
        Approach used in NLP to represent documents (ej: a user|company data is a document)
        ignoring the order of the words. This method fills the bag of words column
        for every user|company with the info in the given columns.

        Args:
            df (pd.DataFrame): the dataframe that contains the users/companies content in its columns.
            columns (list): the colums to be used to fill the new bag of words column.

        Returns:
            None.
        """
        for index, row in df.iterrows():
            words = ''
            for col in columns:
                words += str(row[col]) + ' '
            df.at[index, 'bag_of_words'] = words

        # strip white spaces infront and behind, replace multiple whitespaces (if any)
        df['bag_of_words'] = df['bag_of_words'].str.strip().str.replace('   ', ' ').str.replace('  ', ' ')
        df = df[['id', 'name', 'bag_of_words']]


    def keywords_extraction_from_text(self, df, columns):
        """
        This function extracts keywords from text data in the specified columns of the input DataFrame
        using the Rake algorithm and updates the DataFrame in place with the extracted keywords

        Args:
            df (pandas.DataFrame): The DataFrame containing text data.
            columns (list): A list of column names in the DataFrame to extract keywords from

        Returns:
            None
        """
        for index, row in df.iterrows():
            for column in columns:
                self.r.extract_keywords_from_text(f'{row[column[4:]]}')
                df.at[index, column] = ' '.join(list(self.r.get_word_degrees().keys()))


    def add_user_data_to_df(self, df):
        """
        Adds two columns to the dataframe for every user: skills & experiences.
        This is performed by querying to the database relying on these two models.

        Args:
            df (pd.DataFrame): dataframe that stores info about the users (User database model).

        Returns:
            None.
        """
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
            df.at[i, 'skills'] = all_skills.get(i+1, '')
            df.at[i, 'experiences'] = all_experiences.get(i+1, '')



    def add_company_data_to_df(self, df):
        """
        This method adds one column to the dataframe for every company: CompanyRoles.
        This is performed by querying to the database relying on the CompanyRoles model.

        Args:
            df (pd.DataFrame): Dataframe that stores info about the companies (Company database model).

        Returns:
            df (pd.DataFrame): The updated DataFrame with roles column.
        """

        all_roles = {}
        for company in Company.objects.all():
            all_roles[company.id] = ''
        for role in CompanyRoles.objects.all():
            string = f'{ role.name } { role.description } { role.role.position }'
            all_roles[role.company_id] = all_roles.get(role.company_id, '') + string

        all_roles = OrderedDict(sorted(all_roles.items()))
        for i, company in enumerate(Company.objects.all()):
            df.at[i, 'roles'] = all_roles.get(i+1, '')

        return df


    def recommend(self, df, obj, cosine_sim):
        """
        Args:
            df (pandas.DataFrame): A DataFrame containing user or company profiles
            obj (User or Company): The user or company object for which recommendations are generated
            cosine_sim (numpy.ndarray): A cosine similarity matrix representing user or company interactions

        Returns:
            recommendations (list): A list of recommended user or company profiles
        """
        interacted_matches = None

        if isinstance(obj, Company):
            # Quitar perfiles con los que se ha interactuado
            interacted_matches = Match.objects.filter(company_like__isnull=False, company=obj).values_list('user_id', flat=True).distinct()
        else:
            # Quitar perfiles con los que se ha interactuado
            interacted_matches = Match.objects.filter(user_like__isnull=False, user=obj).values_list('company_id', flat=True).distinct()

        # Con los que no ha interactuado
        df = df[~df['id'].isin(interacted_matches)]

        cosine_sim_df = pd.DataFrame(cosine_sim[0], columns=['score'])
        cosine_sim_df.index += 1

        df = df.merge(cosine_sim_df, left_on='id', right_index=True, how='inner')
        df = df.sort_values(by='score', ascending=False)

        if df.empty:
            return []

        recommendations = df['id'].values.tolist()

        return recommendations

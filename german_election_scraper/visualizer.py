import seaborn as sns
import matplotlib.pyplot as plt
import os
import json
import pandas as pd
import matplotlib
matplotlib.use('Qt5Agg')


def load_data():
    data = []
    for state_id in range(1, 17):
        state_dir = f"strukturdaten/{state_id}"
        if os.path.exists(state_dir):
            for filename in os.listdir(state_dir):
                if filename.startswith('strukturdaten_') and filename.endswith('.json'):
                    with open(os.path.join(state_dir, filename), 'r', encoding='utf-8') as f:
                        strukturdaten = json.load(f)
                        wahlkreis_number = filename.split(
                            '_')[-1].split('.')[0]
                        election_filename = f"election_results_{wahlkreis_number}.json"
                        election_filepath = os.path.join(
                            state_dir, election_filename)
                        if os.path.exists(election_filepath):
                            with open(election_filepath, 'r', encoding='utf-8') as ef:
                                election_results = json.load(ef)
                                data.append({
                                    "state_id": state_id,
                                    "wahlkreis_number": wahlkreis_number,
                                    "strukturdaten": strukturdaten,
                                    "election_results": election_results
                                })
    return data


def analyze_data(data):
    # Set display options to show all columns
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 0)
    education_without_degree = []
    education_with_university = []
    unemployment_rates = []
    income = []
    spd_votes = []
    cdu_votes = []
    afd_votes = []
    gruene_votes = []
    linke_votes = []

    age_18_24 = []
    age_25_34 = []
    age_35_59 = []
    age_60_74 = []
    age_75_plus = []

    for entry in data:
        age_distribution = entry['strukturdaten'].get('Population and age', {})
        age_18_24.append(float(age_distribution.get(
            '... 18 - 24', 0).replace('\xa0%', '')))
        age_25_34.append(float(age_distribution.get(
            '... 25 - 34', 0).replace('\xa0%', '')))
        age_35_59.append(float(age_distribution.get(
            '... 35 - 59', 0).replace('\xa0%', '')))
        age_60_74.append(float(age_distribution.get(
            '... 60 - 74', 0).replace('\xa0%', '')))
        age_75_plus.append(float(age_distribution.get(
            '... 75 and over', 0).replace('\xa0%', '')))
        education = entry['strukturdaten'].get('General Education System', {}).get(
            'Graduates an school leavers having completed their education 2022', {})
        education_without_degree.append(float(education.get(
            'Without Secondary School Certificate', 0)))
        education_with_university.append(
            float(education.get('With University Entrance Qualification', 0)))
        unemployment_distribution = entry['strukturdaten'].get(
            'Unemployment rate', {}).get('Unemployment rate at the end of November 2024', {})
        unemployment_rates.append(
            float(unemployment_distribution.get('... total', 0).replace('\xa0%', '')))

        # Extract income data
        income_data = entry['strukturdaten'].get('National accounts', {}).get(
            'Disposable income of households 2021 (EUR per habitant)', '0').replace(',', '')
        income.append(float(income_data))
        # migration percentage?

        partyVotes = entry['election_results']['parties']
        spd_votes.append(partyVotes.get('SPD', {}).get('absolute_votes', 0))
        cdu_votes.append(partyVotes.get('CDU', {}).get('absolute_votes', 0))
        afd_votes.append(partyVotes.get('AfD', {}).get('absolute_votes', 0))
        gruene_votes.append(partyVotes.get(
            'GRÜNE', {}).get('absolute_votes', 0))
        linke_votes.append(partyVotes.get(
            'Die Linke', {}).get('absolute_votes', 0))

    df_no_degree = pd.DataFrame({
        # 'Percentage without a school degree': education_without_degree,
        'no_degree [%]': education_without_degree,
        'Votes SPD': spd_votes,
        'Votes CDU': cdu_votes,
        'Votes AfD': afd_votes,
        'Votes Grüne': gruene_votes,
        'Votes Linke': linke_votes,
    })
    df_with_university = pd.DataFrame({
        # 'Percentage without a school degree': education_without_degree,
        'uni_quali [%]': education_with_university,
        'Votes SPD': spd_votes,
        'Votes CDU': cdu_votes,
        'Votes AfD': afd_votes,
        'Votes Grüne': gruene_votes,
        'Votes Linke': linke_votes,
    })
    df_age = pd.DataFrame({
        'Age 18-24': age_18_24,
        'Age 25-34': age_25_34,
        'Age 35-59': age_35_59,
        'Age 60-74': age_60_74,
        'Age 75+': age_75_plus,
        'Votes SPD': spd_votes,
        'Votes CDU': cdu_votes,
        'Votes AfD': afd_votes,
        'Votes Grüne': gruene_votes,
        'Votes Linke': linke_votes,
    })
    df_income = pd.DataFrame({
        'Disposable Income': income,
        'Votes SPD': spd_votes,
        'Votes CDU': cdu_votes,
        'Votes AfD': afd_votes,
        'Votes Grüne': gruene_votes,
        'Votes Linke': linke_votes,
    })
    
    df_unemployment = pd.DataFrame({
        'Unemployment rate': unemployment_rates,
        'Votes SPD': spd_votes,
        'Votes CDU': cdu_votes,
        'Votes AfD': afd_votes,
        'Votes Grüne': gruene_votes,
        'Votes Linke': linke_votes,
    })

    correlation = df_no_degree.corr()
    print("Correlation between no school degree and votes:")
    print(correlation)

    print()

    correlation = df_with_university.corr()
    print("Correlation between university qualification and votes:")
    print(correlation)

    print()

    correlation_age = df_age.corr()
    print("Correlation between age groups and votes:")
    print(correlation_age)

    print()

    correlation_income = df_income.corr()
    print("Correlation between disposable income and votes:")
    print(correlation_income)

    print()
    print("Correlation between unemployment rates and votes:")
    print(correlation_unemployment)


if __name__ == "__main__":
    data = load_data()
    analyze_data(data)

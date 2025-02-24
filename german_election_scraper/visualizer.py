import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


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
    # Example analysis: Correlation between education level and voting patterns
    education_levels = []
    spd_votes = []
    cdu_votes = []
    afd_votes = []
    gruene_votes = []

    for entry in data:
        education = float(entry['strukturdaten'].get('General Education System', {}).get(
            'Graduates an school leavers having completed their education 2022', {}).get('Without Secondary School Certificate', 0).replace(' %', ''))
        education_levels.append(education)
        partyVotes = entry['election_results']['parties']
        spd_votes.append(partyVotes.get('SPD', {}).get('absolute_votes', 0))
        cdu_votes.append(partyVotes.get('CDU', {}).get('absolute_votes', 0))
        afd_votes.append(partyVotes.get('AfD', {}).get('absolute_votes', 0))
        gruene_votes.append(partyVotes.get(
            'GRÜNE', {}).get('absolute_votes', 0))

    df = pd.DataFrame({
        'Percentage without a school degree': education_levels,
        'Votes for SPD': spd_votes,
        'Votes for CDU': cdu_votes,
        'Votes for AfD': afd_votes,
        'Votes for Grüne': gruene_votes,
    })

    print(f"Number of constituencies considered: {len(data)}")
    correlation = df.corr()
    print("Correlation matrix:")
    print(correlation)

    sns.scatterplot(x='Percentage without a school degree',
                    y='Votes for SPD', data=df)
    plt.title('Correlation between Education Level and Votes for Some Party')
    plt.show()


if __name__ == "__main__":
    data = load_data()
    analyze_data(data)

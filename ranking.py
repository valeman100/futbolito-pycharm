import os
import mysql.connector
import pandas as pd
from dotenv import load_dotenv

load_dotenv('.env')


def calculate_score(diff):
    if diff >= 8:
        return 5
    elif diff >= 6:
        return 4
    elif diff >= 3:
        return 3
    elif diff >= 2:
        return 2
    else:
        return 1


cnx = mysql.connector.connect(user=os.getenv('DB_USERNAME'),
                              password=os.getenv('DB_PASSWORD'),
                              host=os.getenv('DB_HOST'),
                              database='sql7608762',
                              buffered=True)

with cnx.cursor() as cursor:
    table_query = '''SELECT u.*, m.*
FROM users u
inner join matches m on m.user1 = u.name or m.user2 = u.name or m.user3 = u.name or m.user4 = u.name
where m.score1 != 0 and m.score2 != 0
ORDER BY score DESC
'''
    cursor.execute(table_query)
    table = cursor.fetchall()

    df = pd.DataFrame(table, columns=['user_id', 'name', 'surname',
                                      'score', 'coefficient', 'match_id', 'user1', 'user2', 'user3', 'user4', 'score1',
                                      'score2'])

participants = ['Ilaria', 'Jody', 'Valerio', 'Stefania', 'Nicolo\'', 'Egidio', 'Gaia', 'Simone', 'Fabio', 'Davide',
                'Emilia', 'Stefano', 'Vincenzo', 'Gabriele', 'Edel', 'Giuseppe']
score = {}
for name in participants:
    score_name = df[df.name == name]
    score[name] = 0
    for line in score_name.iterrows():
        line = line[1]
        if name in line.user1 or name in line.user2:
            diff = abs(line.score2 - line.score1)
            if line.score1 >= 10:
                score[name] += calculate_score(diff)
            else:
                score[name] -= calculate_score(diff) * line.coefficient
        else:
            diff = abs(line.score2 - line.score1)
            if line.score2 >= 10:
                score[name] += calculate_score(diff)
            else:
                score[name] -= calculate_score(diff) * line.coefficient
# sort the score using values
score = {k: v for k, v in sorted(score.items(), key=lambda item: item[1], reverse=True)}

# create a dataframe with the final score
final_scores = pd.DataFrame(score.items(), columns=['name', 'score'])
final_scores['score'] = final_scores['score'].apply(lambda x: round(x, 2))
print(final_scores)
print('done')

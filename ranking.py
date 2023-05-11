import mysql.connector
import pandas as pd


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


cnx = mysql.connector.connect(user='sql7608762',
                              password='QYfSvVEVZ3',
                              host='sql7.freemysqlhosting.net',
                              database='sql7608762',
                              buffered=True)

with cnx.cursor() as cursor:
    table_query = '''SELECT u.*, m.*
FROM users u
inner join matches m on m.user1 = u.name or m.user2 = u.name or m.user3 = u.name or m.user4 = u.name
where m.score1 != 0 and m.score2 != 0
ORDER BY score DESC
'''

    total_matches_query = '''SELECT count(*) FROM matches m
where m.score1 != 0 or m.score2 != 0
'''

    cursor.execute(table_query)
    table = cursor.fetchall()

    cursor.execute(total_matches_query)
    total_matches = cursor.fetchone()[0]

    df = pd.DataFrame(table, columns=['user_id', 'name', 'surname',
                                      'score', 'coefficient', 'match_id', 'user1', 'user2', 'user3', 'user4', 'score1',
                                      'score2'])

participants = ['Ilaria', 'Jody', 'Valerio', 'Stefania', 'Nicolo', 'Egidio', 'Gaia', 'Simone', 'Fabio', 'Davide',
                'Emilia', 'Stefano', 'Vincenzo', 'Gabriele', 'Edel', 'Giuseppe']
score = {}
match_played = {}
matches_won = {}
for name in participants:
    score_name = df[df.name == name]
    score[name] = 0
    matches_won[name] = 0
    match_played[name] = len(score_name)
    for line in score_name.iterrows():
        line = line[1]
        if name in line.user1 or name in line.user2:
            diff = abs(line.score2 - line.score1)
            if line.score1 >= 10:
                score[name] += calculate_score(diff)
                matches_won[name] += 1
            else:
                score[name] -= calculate_score(diff) * line.coefficient
        else:
            diff = abs(line.score2 - line.score1)
            if line.score2 >= 10:
                score[name] += calculate_score(diff)
                matches_won[name] += 1
            else:
                score[name] -= calculate_score(diff) * line.coefficient

# sort the score using values
score = {k: v for k, v in sorted(score.items(), key=lambda item: item[1], reverse=True)}

# create a dataframe with the number of matches played
matches_played = pd.DataFrame(match_played.items(), columns=['name', 'matches_played'])
won = pd.DataFrame(matches_won.items(), columns=['name', 'matches_won'])

# create a dataframe with the final score
final_scores = pd.DataFrame(score.items(), columns=['name', 'score'])
final_scores['score'] = final_scores['score'].apply(lambda x: round(x, 2))

# merge the two dataframes
final_scores = pd.merge(final_scores, matches_played, on='name')
final_scores = pd.merge(final_scores, won, on='name')

# add column with points per match
final_scores['points_per_match'] = final_scores['score'] / final_scores['matches_played']
final_scores['points_per_match'] = final_scores['points_per_match'].apply(lambda x: round(x, 2))

print("Total matches played: " + str(total_matches))
print(final_scores)

cnx.close()

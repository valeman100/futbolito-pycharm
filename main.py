import random
import pandas as pd


participants = ['Ilaria', 'Jody', 'Valerio', 'Stefania', 'Nicolo\'', 'Egidio', 'Gaia', 'Simone', 'Fabio', 'Davide',
                'Emilia', 'Stefano', 'Vincenzo', 'Gabriele', 'Edel', 'Giuseppe']

df = pd.DataFrame(participants)
df.to_csv('participants.csv', index=False)

# crate all the possible pairs
teams = []
for i in range(len(participants)):
    for j in range(i + 1, len(participants)):
        teams.append((participants[i], participants[j]))

# shuffle the pairs
random.shuffle(teams)
matches = []

i = 1
while len(teams) >= 1:
    team1 = teams[0]
    team2 = teams[i]
    if team1[0] in team2 or team1[1] in team2:
        # print('Error')
        i += 1
    else:
        matches.append((team1, team2))
        if len(matches)==68:
            break
        teams.pop(0)
        teams.pop(i-1)
        i = 1

matches.sort(key=lambda x: x[0][0])

for i, match in enumerate(matches):
    print(i, match)


df = pd.DataFrame(matches)
df.to_csv('matches_final.csv', index=False)

# print the matches
for i, match in enumerate(matches):
    print(i, match)


print('Hello, World!')


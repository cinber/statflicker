#--------------------------------------------#
#                  Setup
#--------------------------------------------#

# Import Packages/Functions
import requests
import pandas as pd
import re
import sys
from bs4 import BeautifulSoup
from time import sleep

# -----------SET CONSTANTS---------

week_id = ["6", "13", "20", "22"]
#  "28", "35", "42", "49", "56", "63", "70", "77", "84", "91", "98", "105", "112", "119", "126", "133", "140", "147", "154", "161"]

# --------DEFINE FUNCTIONS---------


def reqPage(url):

    # Define local variables
    headers = {'user-agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleW'
                              'ebKit/537.36 (KHTML, like Gecko) Chrome/62.0.320'
                              '2.94 Safari/537.36')}
    req = ''
    attempt = 1
    attempt_max = 10  # Max attempts
    attempt_delay = 5

    # Try multiple attemps until succesful, with increasing delay
    while (req == '') and (attempt <= attempt_max):
        try:
            req = requests.get(url, headers=headers)
            break
        except:
            print("\n")
            print("Connection Error. Trying again in 15 seconds...")
            print("\n")
            attempt = attempt + 1
            sleep(attempt*attempt_delay)
            continue

    return req


def getCurrent(league_id):

    # Concatenate league id to form league url
    league_url = ('https://www.fleaflicker.com/nba/leagues/' + str(league_id) +
                  '/scores')

    # Request page and create soup
    req = reqPage(league_url)

    # Create Soup
    soup = BeautifulSoup(req.text, 'html.parser')
    if type(soup) is type(None):
        return ''

    # Find Season Menu
    try:
        seasons = soup.find(
            'ul', attrs={'class': 'dropdown-menu pull-right'}).find_all('li')
        end_season = seasons[0].text.strip()
        start_season = seasons[-1].text.strip()
    except:
        print('Could not extract seasons')

    start_season = start_season[1:]
    end_season = end_season[1:]

    # Look for drop-down menu to select week
    weeks = soup.find('ul', attrs={'class': 'dropdown-menu pull-left'})
    current_week = weeks.find('li', attrs={'class': 'active'})
    menu_items = weeks.find_all('li')
    for i in list(range(0, len(menu_items))):
        item = menu_items[i]
        if item == current_week:
            start_week = i

    return start_week, start_season, end_season


def getTeams(league_id, season):

    # Create list to store team data
    team_data = []

    # Concatenate league id to form league url
    league_url = ('https://www.fleaflicker.com/nba/leagues/' + str(league_id) +
                  '?season=' + str(season))

    # Request page and create soup
    req = reqPage(league_url)

    # Create Soup
    soup = BeautifulSoup(req.text, 'html.parser')
    if type(soup) is type(None):
        return ''

    # Loop through rows to find teams
    rows = soup.find_all('tr')
    for row in rows:

        # Team ID
        try:
            target = row.find(
                'div', attrs={'class': 'league-name'}).a.get('href')
            team_id = re.findall('(?<=teams/)[0-9]{1,}', target)[0]
        except:
            continue

        # Team Name
        key = 'team'
        try:
            val = row.find(
                'div', attrs={'class': 'league-name'}).text.strip()
            team_data.append([team_id, key, val])
        except:
            print('    -Could not find attribute: %s' % (key))

        # Manager Name
        key = 'manager_name'
        try:
            val = row.find('a', attrs={'class': 'user-name'}).text.strip()
            team_data.append([team_id, key, val])
        except:
            print('    -Could not find attribute: %s' % (key))

        # Manager User ID
        key = 'manager_id'
        try:
            target = row.find(
                'a', attrs={'class': 'user-name'}).get('href')
            val = target.rpartition('/')[-1]
            team_data.append([team_id, key, val])
        except:
            print('    -Could not find attribute: %s' % (key))

    # Save as pandas dataframe
    df = pd.DataFrame.from_records(
        team_data, columns=['team_id', 'Key', 'Value'])
    df = df.pivot(index='team_id', columns='Key', values='Value')
    df.reset_index(inplace=True)

    return df


def getPoints(league_id, weeks_new, week_id):
    
    # Check if weeks_new is length zero
    if len(weeks_new) == 0:
        print('No new data')
        return

    # Create list to store team data
    point_data = []
    week_nr = 1
    season = []
    # seasons_new = [item[0] for item in weeks_new]
    # seasons_new = list(set(seasons_new))
    # print(seasons_new)

    for week in weeks_new:
        # week_nr += [week[1]]
        season += [week[0]]
    # week_nr = list(reversed(week_nr))
    # print(week_nr)
    c = 0
    for weeks in week_id:
        # Gather team information

        df_teams = getTeams(league_id, season)

        print('----------------------------------------------------------------')
        print(week_nr)
        print('----------------------------------------------------------------')

        for i in list(range(0, df_teams.shape[0])):
            # Set team information
            team_id = df_teams.team_id[i]
            manager_id = df_teams.manager_id[i]
            manager_name = df_teams.manager_name[i]
            team = df_teams.team[i]

            # Concatenate league id to form league url
            url = ('https://www.fleaflicker.com/nba/leagues/' +
                   league_id + '/teams/' + str(team_id) + '?season='
                   + str(season[i]) + '&week=' + str(weeks))

            # Sleep 2 sec before loading page
            sleep(2)

            # Print Status
            print(url)

            # Request page and create soup
            req = reqPage(url)

            # Create Soup
            soup = BeautifulSoup(req.text, 'html.parser')
            if type(soup) is type(None):
                print('No soup for you...  ', url)
                continue

            # Find Primary Table
            table = soup.find('table',
                              attrs={'class': ('table-group table table-striped table-bordered table-hover')})

            # Find rows in table
            rows = table.find_all('tr')

            for row in rows:
                # Player Name

                key = 'player_name'
                try:
                    target = row.find('div', attrs={'class': 'player'})
                    player_name = target.find(
                        'a', attrs={'class': 'player-text'}).text.strip()
                except:
                    continue

                # Player ID
                key = 'player_id'
                try:
                    target = row.find('div', attrs={'class': 'player'})
                    target = target.find('a', attrs={'class': 'player-text'})
                    target = target.get('href')
                    val = re.findall('(?<=-)[0-9]{1,}', target)[0]
                    point_data.append([team_id,  manager_id,  manager_name,
                                       team, season[i], week_nr, player_name,
                                       key, val])
                except:
                    print('    -Could not find attribute: %s' % (key))

                # Player Position
                key = 'position'
                try:
                    target = row.find('div', attrs={'class': 'player'})
                    val = target.find(
                        'span', attrs={'class': 'position'}).text.strip()
                    point_data.append([team_id,  manager_id,  manager_name,
                                       team, season[i], week_nr, player_name,
                                       key, val])
                except:
                    print('    -Could not find attribute: %s' % (key))

                # Player Team
                key = 'team'
                try:
                    target = row.find('div', attrs={'class': 'player'})
                    val = target.find(
                        'span', attrs={'class': 'player-team'}).text.strip()
                    point_data.append([team_id,  manager_id,  manager_name,
                                       team, season[i], week_nr, player_name,
                                       key, val])
                except:
                    print('    -Could not find attribute: %s' % (key))

                # Set Position
                key = 'set_pos'
                try:
                    target = row.find_all('td')[-1]
                    val = target.text.strip()
                    point_data.append([team_id,  manager_id,  manager_name,
                                       team, season[i], week_nr, player_name,
                                       key, val])
                except:
                    print('    -Could not find attribute: %s' % (key))

                # Fantasy Points
                key = 'points'
                try:
                    target = row.find('span', attrs={'class': 'fp'})
                    val = target.find('span', attrs={'class': 'tt-content'}).text.strip()
                    point_data.append([team_id,  manager_id,  manager_name,
                                       team, season[i], week_nr, player_name,
                                       key, val])
                    print(point_data)
                except:
                    print('    -Could not find attribute: %s' % (key))
        c += 1
        week_nr += 1

    # Save as pandas dataframe
    df = pd.DataFrame.from_records(point_data,
                                   columns=['team_id',  'manager_id',
                                            'manager_name', 'team',
                                            'season', 'week', 'player_name',
                                            'key', 'val'])
    # print(df)
    # Find Duplicates (troubleshooting only)
    # df[df.duplicated()]

    # Create ID column for pivoting
    df['ID'] = (df['team_id'] + ',' + df['manager_id'].astype(str) + ',' +
                df['manager_name'].astype(str) + ',' +
                df['team'].astype(str) + ',' + df['season'].astype(str) +
                ',' + df['week'].astype(str) + ',' + df['player_name'])

    df.drop(columns=['team_id', 'manager_id', 'manager_name', 'team',
                     'season', 'week', 'player_name'], inplace=True)

    # # Pivot Key/Value Columns
    df = df.pivot(index='ID', columns='key', values='val')
    df.reset_index(inplace=True)

    # Split ID back into individual columns
    df[['team_id', 'manager_id', 'manager_name', 'team', 'season',
        'week', 'player_name']] = df.ID.str.split(',', expand=True)
    df = df[['team_id', 'manager_id', 'manager_name', 'team', 'season', 'week',
             'player_name', 'player_id', 'team', 'position', 'set_pos', 'points']]

    # Replace NA points with 0
    df['points'] = df['points'].fillna(value='0')

    return df


def checkNew(league_id, filepath):

    # Load file, flag if missing
    file_missing = False
    try:
        df_old = pd.read_csv(filepath, encoding="utf-8")
    except:
        print('File not found, defaulting to all available weeks')
        file_missing = True

    # List out available weeks

    weeks_avl = []
    start_week, start_season, end_season = getCurrent(league_id)
    for season in list(reversed(range(int(end_season[3:]), int(start_season[3:])+1))):
        # print(start_season, end_season)
        for week in list(reversed(range(1, 24))):
            # Skip future weeks if current season
            if (season == start_season) and (week > start_week):
                continue
            weeks_avl.append([season, week])

    # Return available weeks if there is no existing file
    if file_missing:
        # print(weeks_avl)
        return weeks_avl

    # If file does exist, extract week values
    weeks_old = df_old[['season', 'week']].drop_duplicates().values.tolist()

    # Find new available weeks not already stored in file
    weeks_new = [x for x in weeks_avl if x not in weeks_old]

    return weeks_new


def saveNew(df_new, filepath):

    # Load file, flag if missing
    try:
        df_old = pd.read_csv(filepath, encoding="utf-8")
    except:
        print('File not found, saving only new data')
        df_new.to_csv(filepath, index=False, encoding="utf-8")
        return
    
    # TODO
    # Combine new/old and remove duplicates
    df_comb = df_old.append(df_new, ignore_index=True)
    df_comb.drop_duplicates(inplace=True)

    # Save Data
    df_comb.to_csv(filepath, index=False, encoding="utf-8")

# ------------SCRIPT------------

league_id = input('Enter your league ID: ')
filepath_points = '~/Documents/#berichte/points.csv'

start_week, start_season, end_season = getCurrent(league_id)
new_week = checkNew(league_id, filepath_points)

# Get League Data
print('Get League Data: ...')
print('----------------------------------------------------------------')
df_teams = getTeams(league_id, end_season)
print(df_teams)

print('----------------------------------------------------------------')
df_points = getPoints(league_id, new_week, week_id)
print(df_points)

# Save Data
saveNew(df_points, filepath_points)

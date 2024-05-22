import pandas as pd
import numpy as np
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import re
# import requests
# import sys
import time


url_dict = {"NWSL": "182/NWSL-Stats"}
player_file_dict = {"NWSL": "playerstats_nwsl.csv"}
goalkeeper_file_dict = {"NWSL": "goalkeeperstats_nwsl.csv"}

# Taken from https://github.com/hoyishian/footballwebscraper
season = '2023-2024'

NWSL_dict = {
    "Angel City": "https://fbref.com/en/squads/ae38d267/Angel-City-FC-Stats",
}


def extract_goalkeeper_stats(league_name, player_link, goalkeeper_file_name):
    name = extract_name(player_link)

    try:
        df = pd.read_html(player_link, header=1)[0]
        if len(df.columns) < 36:
            print("Invalid length of columns", player_link)
            return
        df = df.drop(columns=['Match Report'])
        df = df[df['Comp'] == league_name]
        df = df.drop(columns=['Comp'], errors='ignore')
        df = df.rename(columns={"Day": "Name"})
        df.dropna(subset=["Date"], inplace=True)
        df['Name'] = df['Name'].replace(
            ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], name)

        if "PSxG" not in df.columns:
            df["Post-Shot Expected Goals"] = np.nan
        df = df.rename(columns={"Att": "PassAttemptedLong"})

        df = df.rename(columns={"Att.1": "PassAtt"})
        df = df.rename(columns={"Att.2": "GoalKickAtt"})
        df = df.rename(columns={"Launch%.1": "GKLaunch%"})
        df = df.rename(columns={"AvgLen.1": "GKAvgLen"})
        df.drop(
            df[df["Pos"] == "On matchday squad, but did not play"].index, inplace=True)
        df = df[df.Round != "Round"]
        df['sort'] = df['Round'].str.extract('(\d+)', expand=False).astype(int)
        df.sort_values('sort', inplace=True)
        df = df.drop('sort', axis=1)
        df.fillna(0, inplace=True)

        if len(df.columns) != 35:
            print("Invalid Number of Columns", player_link)
            return

        try:
            f = open(goalkeeper_file_name)
            df.to_csv(goalkeeper_file_name, index=False,
                      header=False, mode='a')
            f.close()
        except:
            df.to_csv(goalkeeper_file_name, index=False)
    except Exception:
        print(Exception)
        print("Invalid Goalkeeper", player_link)
        return


def extract_player_stats(league_name, player_link, player_file_name):
    print(player_link, player_file_name)
    name = extract_name(player_link)
    new_player_link = player_link.replace("keeper", "passing")
    try:
        print(new_player_link)
        df = pd.read_html(new_player_link, header=1)[0]
        print(df)
        df = df.drop(columns=['Match Report'])
        df = df[df['Comp'] == league_name]
        df = df.drop(columns=['Comp'], errors='ignore')
        df = df.rename(columns={"Day": "Name"})
        df.dropna(subset=["Date"], inplace=True)
        df['Name'] = df['Name'].replace(
            ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], name)
        df = df.rename(columns={"Att": "PassAtt"})
        df = df.rename(
            columns={"TotDist": "PassTotDist"})
        df = df.rename(columns={"PrgDist": "PassPrgDist"})
        df = df.rename(columns={"1/3": "PassFinThird"})
        df = df.rename(columns={"Prog": "PassProg"})
        df.fillna(0, inplace=True)

        time.sleep(2)
        new_player_link = player_link.replace("keeper", "gca")
        df_2 = pd.read_html(new_player_link, header=1)[0]
        df_2 = df_2.drop(columns=['Match Report'])
        df_2 = df_2.drop(columns=['Comp'], errors='ignore')
        df_2 = df_2.rename(columns={"Day": "Name"})
        df_2.dropna(subset=["Date"], inplace=True)
        df_2['Name'] = df_2['Name'].replace(
            ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], name)
        df_2 = df_2.drop(['Date', 'Name', 'Round', 'Venue', 'Result',
                          'Squad', 'Opponent', 'Start', 'Pos', 'Min'], axis=1)
        df_2 = df_2.rename(
            columns={"PassLive": "PassLiveShot"})
        df_2 = df_2.rename(
            columns={"PassDead": "PassDeadShot"})
        df_2 = df_2.rename(
            columns={"Drib": "DribShot"})
        df_2 = df_2.rename(
            columns={"Sh": "ShLSh"})
        df_2 = df_2.rename(
            columns={"Def": "DefShot"})
        df_2 = df_2.rename(
            columns={"PassLive.1": "PassLiveGoal"})
        df_2 = df_2.rename(
            columns={"PassDead.1": "PassDeadGoal"})
        df_2 = df_2.rename(
            columns={"Drib.1": "DribGoal"})
        df_2 = df_2.rename(columns={"Sh.1": "ShGoal"})
        df_2 = df_2.rename(columns={"Fld.1": "FldGoal"})
        df_2 = df_2.rename(
            columns={"Def.1": "DefGoal"})
        df_2.fillna(0, inplace=True)

        time.sleep(1)
        new_player_link = player_link.replace("keeper", "defense")
        df_3 = pd.read_html(new_player_link, header=1)[0]
        df_3 = df_3.drop(columns=['Match Report'])
        df_3 = df_3.drop(columns=['Comp'], errors='ignore')
        df_3 = df_3.rename(columns={"Day": "Name"})
        df_3.dropna(subset=["Date"], inplace=True)
        df_3['Name'] = df_3['Name'].replace(
            ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], name)
        df_3 = df_3.drop(['Date', 'Name', 'Round', 'Venue', 'Result',
                          'Squad', 'Opponent', 'Start', 'Pos', 'Min'], axis=1)
        df_3 = df_3.rename(
            columns={"Def 3rd": "TacklesDef3rd"})
        df_3 = df_3.rename(
            columns={"Mid 3rd": "TacklesMid3rd"})
        df_3 = df_3.rename(columns={"Att 3rd": "TacklesAtt3rd"})
        df_3 = df_3.rename(columns={"Tkl.1": "DribTackled"})
        df_3 = df_3.rename(columns={"Att": "DribContest"})
        df_3 = df_3.rename(columns={"Tkl%": "DribTackled%"})
        df_3 = df_3.rename(columns={"Succ": "SuccPress"})
        df_3 = df_3.rename(columns={"%": "SuccPress%"})
        df_3 = df_3.rename(
            columns={"Def 3rd.1": "PressDef3rd"})
        df_3 = df_3.rename(
            columns={"Mid 3rd.1": "PressMid3rd"})
        df_3 = df_3.rename(
            columns={"Att 3rd.1": "PressAtt3rd"})
        df_3 = df_3.rename(
            columns={"Sh": "BlockSh"})
        df_3.fillna(0, inplace=True)

        time.sleep(3)
        new_player_link = player_link.replace("keeper", "possession")
        df_4 = pd.read_html(new_player_link, header=1)[0]
        df_4 = df_4.drop(columns=['Match Report'])
        df_4 = df_4.drop(columns=['Comp'], errors='ignore')
        df_4 = df_4.rename(columns={"Day": "Name"})
        df_4.dropna(subset=["Date"], inplace=True)
        df_4['Name'] = df_4['Name'].replace(
            ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], name)
        df_4 = df_4.drop(['Date', 'Name', 'Round', 'Venue', 'Result',
                          'Squad', 'Opponent', 'Start', 'Pos', 'Min'], axis=1)
        df_4 = df_4.rename(columns={"Def 3rd": "TouchDef3rd"})
        df_4 = df_4.rename(columns={"Mid 3rd": "TouchMid3rd"})
        df_4 = df_4.rename(columns={"Att 3rd": "TouchAtt3rd"})
        df_4 = df_4.rename(
            columns={"Att Pen": "AttPen"})
        df_4 = df_4.rename(columns={"Prog": "ProgCarries"})
        df_4 = df_4.rename(columns={"1/3": "CarriesFinThird"})
        df_4 = df_4.rename(columns={"Prog.1": "ProgPassRec"})
        df_4.fillna(0, inplace=True)

        time.sleep(2)
        new_player_link = player_link.replace("keeper", "summary")
        df_5 = pd.read_html(new_player_link, header=1)[0]
        df_5 = df_5.drop(columns=['Match Report'])
        df_5 = df_5.drop(columns=['Comp'], errors='ignore')
        df_5 = df_5.drop(columns=['Ast'], errors='ignore')
        df_5 = df_5.drop(columns=['Ast'], errors='ignore')
        df_5 = df_5.drop(columns=['Press'], errors='ignore')
        df_5 = df_5.drop(columns=['Tkl'], errors='ignore')
        df_5 = df_5.drop(columns=['Int'], errors='ignore')
        df_5 = df_5.drop(columns=['Blocks'], errors='ignore')
        df_5 = df_5.drop(columns=['xA'], errors='ignore')
        df_5 = df_5.drop(columns=['SCA'], errors='ignore')
        df_5 = df_5.drop(columns=['GCA'], errors='ignore')

        df_5 = df_5.drop(columns=['Cmp'], errors='ignore')
        df_5 = df_5.drop(columns=['Att'], errors='ignore')
        df_5 = df_5.drop(columns=['Cmp%'], errors='ignore')
        df_5 = df_5.drop(columns=['Prog'], errors='ignore')

        df_5 = df_5.drop(columns=['Carries'], errors='ignore')
        df_5 = df_5.drop(columns=['Prog.1'], errors='ignore')

        df_5 = df_5.drop(columns=['Succ'], errors='ignore')
        df_5 = df_5.drop(columns=['Att.1'], errors='ignore')

        df_5 = df_5.drop(columns=['Fls'], errors='ignore')
        df_5 = df_5.drop(columns=['Fld'], errors='ignore')
        df_5 = df_5.drop(columns=['Off'], errors='ignore')
        df_5 = df_5.drop(columns=['Crs'], errors='ignore')
        df_5 = df_5.drop(columns=['TklW'], errors='ignore')
        df_5 = df_5.drop(columns=['OG'], errors='ignore')
        df_5 = df_5.drop(columns=['PKwon'], errors='ignore')
        df_5 = df_5.drop(columns=['PKcon'], errors='ignore')
        df_5 = df_5.drop(columns=['Touches'], errors='ignore')

        df_5 = df_5.rename(columns={"Day": "Name"})
        df_5.dropna(subset=["Date"], inplace=True)
        df_5['Name'] = df_5['Name'].replace(
            ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], name)
        df_5 = df_5.drop(['Date', 'Name', 'Round', 'Venue', 'Result',
                          'Squad', 'Opponent', 'Start', 'Pos', 'Min'], axis=1)
        df_5.fillna(0, inplace=True)

        concatenated = pd.concat([df, df_2, df_3, df_4, df_5], axis=1)

        concatenated.drop(
            concatenated[concatenated["Date"] == "Date"].index, inplace=True)
        concatenated.drop(
            concatenated[concatenated["Pos"] == "On matchday squad, but did not play"].index, inplace=True)
        concatenated['sort'] = concatenated['Date']
        concatenated.sort_values('sort', inplace=True)
        concatenated = concatenated.drop('sort', axis=1)
        if len(concatenated.columns) < 90:
            print("Invalid Number of Columns", len(concatenated.columns), new_player_link)
            return
        try:
            print(player_file_name)
            f = open(player_file_name)
            concatenated.to_csv(
                player_file_name, index=False, header=False, mode='a')
            f.close()
        except:
            concatenated.to_csv(player_file_name, index=False)
    except Exception as e:
        print(e)
        print("Invalid Outfield Player", player_link)
        return


def extract_name(player_link):
    # res = requests.get(player_link)
    # html_page = res.content
    res = Request(player_link, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'})
    html_page = urlopen(res).read()
    soup = BeautifulSoup(html_page, 'html.parser')
    # name = soup.find("h1", {"itemprop": "name"})
    name = soup.find("h1")
    return name.find("span").text


def scrape_stats(league='EPL'):

    first_url_value = ""
    player_file_name = ""
    goalkeeper_file_name = ""

    if url_dict.get(league) is None:
        print(f"Invalid League! {league} Please enter League again! Possible: {url_dict}")
        exit()
    else:
        first_url_value += url_dict[league]
        player_file_name += player_file_dict[league]
        goalkeeper_file_name += goalkeeper_file_dict[league]

    # Get List of Teams
    res = Request('https://fbref.com/en/comps/182/stats/NWSL-Stats', headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.37'})
    league_html_page = urlopen(res).read()


    final_team_array = []
    if league == "NWSL":
        for teamurl in NWSL_dict.items():
            final_team_array.append(teamurl[1])
    else:
        print("Invalid League! Please enter League again!")
        exit()

    # print(final_team_array)
    # Get List of all Players and their respective links

    player_array = []
    player_final_array = []
    final_link = []

    text_contains_players = "/en/players/"
    text_contains_summary = "summary"

    for team_url in final_team_array:
        # res = requests.get(team_url)
        # team_html_page = res.content
        res = Request(team_url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'})
        team_html_page = urlopen(res).read()

        soup_team = BeautifulSoup(team_html_page, 'html.parser')

        text = soup_team.find_all("a", href=True)
        for a in text:
            if text_contains_players in a["href"] and text_contains_summary in a["href"]:
                player_array.append(a["href"])
        player_array = list(set(player_array))
        break

    for i in player_array:
        if "matchlog" in i:
            player_final_array.append("https://fbref.com" + i)

    # player_final_array = list(set(player_final_array))
    # for i in player_final_array:
    #     print(i)
    # print(player_final_array)
    for link in player_final_array:
        temp_link = link.replace("summary", "keeper")
        # temp_link = temp_link.replace(f"{season}", league_code_value)
        final_link.append(temp_link)

    final_link = list(set(final_link))
    final_link.sort()

    # Check if Player is GK.
    # If GK, call extract_goalkeeper_stats
    # If not GK, call extract_player_stats
    for player in final_link:
        # break
        # res_player = requests.get(player)
        # html_page_player = res_player.content

        res = Request(player, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'})
        html_page_player = urlopen(res).read()

        new_soup = BeautifulSoup(html_page_player, 'html.parser')

        searched_word = "GK"

        new_result = new_soup.find_all(
            string=re.compile('.*{0}.*'.format(searched_word)))

        new_result = [x for x in new_result if x != 'Att (GK)']

        print(new_result)
        print(len(new_result))

        if len(new_result) == 0:
            extract_player_stats(league, player, player_file_name)
        # else:
        #     # print(player)
        #     extract_goalkeeper_stats(league, player, goalkeeper_file_name)
        time.sleep(2)


# valid_leagues = ['EPL']

scrape_stats('NWSL')

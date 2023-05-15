
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from graphics import *
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier as rf


def get_year():
    while (True):
        inp = input("Please enter a year" + '\n')

        #Checks to make sure it's an valid year
        if (inp.isdigit()):
            inp = int(inp)
            if ((inp < 2024) & (inp > 2000)):
                return inp

def get_method():
    while (True):

        inp = input("\nPlease enter a number: \nRandom: 1 \nSeed weighted: 2\nKenPom: 3\nMachine Learning: 4\n")

        #Checks to make sure it's an valid year
        if (inp.isdigit()):
            inp = int(inp)
            if ((inp < 5) & (inp > 0)):
                return inp

def ids_to_names(id_array, name_array):
    #id_array = [[Seed, ID], [Seed, ID]]
    for i in range(len(id_array)):  # For each team ID in 2022 tourney
        for j in range(len(name_array)):  # For each team name in ncaamb
            if (id_array[i][1] == name_array[j][0]):  # if IDS ==
                id_array[i][1] = name_array[j][1]  # Set ID to name
    return id_array

'''Reorders teams so that it is easier to implement other functions
Teams are initlally ordered 1-16 increasingly, however, since seed 1
plays seed 16, seed 8 plays seed 9, and so on, it is easier to order
the seeds 1, 16, 8, 9, ...'''
def reorder(teams,order):
    new_teams = np.empty(shape=(64,2), dtype='object')
    count = 0
    for j in range(4):
        for i in range(16):
            new_teams[count + j*16] = teams[order[i] + j*16]
            count = count+1
        count = 0

    return new_teams



'''Inputted with an array of teams, outputs winning teams'''
def det_winners(teams, num, method, year):
    for i in range(num):
        if(play_match(teams[i],teams[i+1], method, year)):
            teams = np.delete(teams, i+1, 0)
        else:
            teams = np.delete(teams, i, 0)
    return teams

'''Depending on method chosen, determines winner of a 
single match with that method.'''
def play_match(team1, team2, method, year):
    if(method ==1):
        winner = random_calc()
    if(method ==2):
        winner = random_weighted_by_seed(team1, team2)
    if(method ==3):
        winner = ken_pom(team1, team2)
    if(method ==4):
        winner = ml(team1, team2, year)

    return winner

'''50/50 between who wins'''
def random_calc():
    if(np.random.randint(0, 2, 1)):
        return 1
    else:
        return 0

'''Higher chance of winning if a lower seed'''
def random_weighted_by_seed(team1, team2):
    seed1 = int((team1[0])[1:3])
    seed2 = int((team2[0])[1:3])

    dif = seed1 - seed2

    num = 3.3 * dif

    if ((np.random.randint(0, 100, 1)) > 50 + num):
        return 1

    return 0

'''Winner is based off weighted ken pom rankings'''
def ken_pom(team1,team2):
    pass


'''Adds seed and uses ml model to determine winner'''
def ml(team1, team2, year):

    scores1 = []

    team1 = team1[1]
    team2 = team2[1]

    index = (year, team1)
    team1sc = RegSeasonData.loc[index]

    seed = seed_dict.loc[index].values[0]
    if len(seed) == 4:
        seed = int(seed[1:-1])
    else:
        seed = int(seed[1:])
    team1sc['Seed'] = 3 * seed


    index = (year, team2)
    team2sc = RegSeasonData.loc[index]

    seed = seed_dict.loc[index].values[0]
    if len(seed) == 4:
        seed = int(seed[1:-1])
    else:
        seed = int(seed[1:])
    team2sc['Seed'] = 3 * seed


    score1 = team1sc - team2sc
    scores1.append(score1)
    scores1 = pd.DataFrame(scores1)
    z = scores1[scores.columns[:-1]].values
    y = model.predict_proba(z)
    #print(y)

    #print(" " + str(team1) + ": " + str(y[0][0]))
    if(y[0][0]>=.5):
        return 0
    return 1


'''Simulates the playin games'''
def playin_games(arr, method, year):

    i=0

    '''For each team'''
    while(i<(len(arr)-1)):
        '''If the seed contains a number, (playin team)'''
        if (len(arr[i,0]) == 4):

            '''Return winner'''
            winner = play_match(arr[i], arr[i+1], method, year)

            '''Remove extra character'''
            if(winner):
                arr[i, 0] = (arr[i, 0])[:-1]
                offset = 1
            else:
                arr[i + 1, 0] = (arr[i + 1, 0])[:-1]
                offset = 0

            '''Delete loser from array'''
            arr = np.delete(arr, i + offset, 0)

        i=i+1

    '''Return teams with the losers deleted'''
    return arr

'''Simulates round of 64'''
def RO64(height, width, arr, order):


    '''Flipflop is used to properly print vertical lines'''
    flip_flop = 1

    '''For each team in a quadrant'''
    for i in range (16):

        '''For top, then bottom'''
        for j in range(2):
            y = (25+(height/34)*i + (height/2)*j)
            x = 25
            x_1 = 25 + width/12

            '''Helps print left and right'''
            for k in range(2):

                '''Sets coords for horizontal left side'''
                if not (k):
                    pt1 = Point(x, y)
                    pt2 = Point(x_1, y)

                else:
                    '''Sets coords for horizontal right side'''
                    pt1 = Point(width - x, y)
                    pt2 = Point(width - x_1, y)

                '''Prints horizontal line'''
                ln = Line(pt1, pt2)
                ln.setOutline(color_rgb(255, 255, 255))
                ln.draw(win)


                '''Prints the team on the line'''
                if not (k):
                    write_in_team(x_1-(x_1-x)/2, y-8, arr, i, j, k, order, 64)
                else:
                    write_in_team(width-(x_1-((x_1-x)/2)), y-8, arr, i, j, k, order, 64)



            '''Prints vertical lines'''
            if(flip_flop):
                for k in range(2):
                    y = (25 + (height / 34) * (i) + (height / 2) * j)
                    y_1 = (25 + (height / 34) * (i+1) + (height / 2) * j)
                    x = 25

                    '''Sets coords for left side'''
                    if not (k):
                        pt1 = Point(x+(width/12), y)
                        pt2 = Point(x+(width / 12), y_1)
                    else:
                        '''Sets coords for right side'''
                        pt1 = Point(width - (x+width/12), y)
                        pt2 = Point(width - (x + (width / 12)), y_1)

                    '''Prints vertical lines'''
                    ln = Line(pt1, pt2)
                    ln.setOutline(color_rgb(255, 255, 255))
                    ln.draw(win)

        '''Switch flip flop'''
        if(flip_flop):
            flip_flop = 0
        else:
            flip_flop = 1

'''Simulates round of 32'''
def RO32(height, width, arr, order):

    '''Flip flop is used to properly print vertical lines'''
    flip_flop = 1

    '''For each team in a quadrant'''
    for i in range(8):

        '''For top, then bottom'''
        for j in range(2):
            y = (25 + (height/34)/2 + (height / 17) * i + (height / 2) * j)
            x = 25 + width/12
            x_1 = 25 + 2*(width/12)

            '''Helps print left and right'''
            for k in range(2):

                '''Sets coords for horizontal left side'''
                if not (k):
                    pt1 = Point(x, y)
                    pt2 = Point(x_1, y)
                else:
                    '''Sets coords for horizontal right side'''
                    pt1 = Point(width - x, y)
                    pt2 = Point(width - x_1, y)

                '''Prints horizontal line'''
                ln = Line(pt1, pt2)
                ln.setOutline(color_rgb(255, 255, 255))
                ln.draw(win)

                '''Prints the team on the line'''
                if not (k):
                    write_in_team((x_1-(x_1 - x)/2), y - 8, arr, i, j, k, order, 32)
                else:
                    write_in_team(width - (x_1-((x_1 - x)/2)), y - 8, arr, i, j, k, order, 32)

            '''Prints vertical lines'''
            if (flip_flop):
                for k in range(2):
                    y = (25 + (height/34)/2 + (height / 17) * (i) + (height / 2) * j)
                    y_1 = (25 + (height / 34)/2 + (height/17) * (i + 1) + (height / 2) * j)
                    x = 25 + 2*(width/12)

                    '''Sets coords for left side'''
                    if not (k):
                        pt1 = Point(x, y)
                        pt2 = Point(x, y_1)

                    else:
                        '''Sets coords for right side'''
                        pt1 = Point(width - x, y)
                        pt2 = Point(width - x , y_1)

                    '''Prints vfertical lines'''
                    ln = Line(pt1, pt2)
                    ln.setOutline(color_rgb(255, 255, 255))
                    ln.draw(win)

        '''Switches flip flop'''
        if (flip_flop):
            flip_flop = 0
        else:
            flip_flop = 1

'''Simulates sweet 16'''
def S16(height, width, arr, order):

    '''Flipflop is used to properly print vertical lines'''
    flip_flop = 1

    '''FOr each team in a quadrant'''
    for i in range(4):

        '''For top, then bottom'''
        for j in range(2):
            y = (25 + 1.5*(height / 34) + (4 * height / 34) * i + (height / 2) * j)

            x = 25 + 2*(width / 12)
            x_1 = 25 + 3*(width / 12)

            '''Helps print left and right'''
            for k in range(2):

                '''Sets coords for horizontal left side'''
                if not (k):
                    pt1 = Point(x, y)
                    pt2 = Point(x_1, y)

                else:
                    '''Sets coords for horizontal right side'''
                    pt1 = Point(width - x, y)
                    pt2 = Point(width - x_1, y)

                '''Prints horizontal line'''
                ln = Line(pt1, pt2)
                ln.setOutline(color_rgb(255, 255, 255))
                ln.draw(win)

                '''Prints the team on the line'''
                if not (k):
                    write_in_team((x_1-(x_1 - x)/2), y - 8, arr, i, j, k, order, 16)
                else:
                    write_in_team(width - (x_1-((x_1 - x)/2)), y - 8, arr, i, j, k, order, 16)


            '''Prints vertical lines'''
            if (flip_flop):
                for k in range(2):
                    y = (25 + 1.5*(height / 34) + (4 * height / 34) * i + (height / 2) * j)
                    y_1 = (25 + 1.5*(height / 34) + (4 * height / 34) * (i+1) + (height / 2) * j)

                    x = 25 + 3 * (width / 12)

                    '''Sets coords for left side'''
                    if not (k):
                        pt1 = Point(x, y)
                        pt2 = Point(x, y_1)

                    else:
                        '''Sets coords for right side'''
                        pt1 = Point(width-x, y)
                        pt2 = Point(width-x, y_1)

                    '''Prints vertical lines'''
                    ln = Line(pt1, pt2)
                    ln.setOutline(color_rgb(255, 255, 255))
                    ln.draw(win)

        '''Switches flip flop'''
        if (flip_flop):
            flip_flop = 0
        else:
            flip_flop = 1

'''Simulates elite 8'''
def E8(height, width, arr, order):

    '''Flip flop is used to properly print vertical lines'''
    flip_flop = 1
    for i in range(2):

        '''For each team in a quadrant'''
        for j in range(2) :
            y = (25 + 3.5 * (height / 34) + (8* height / 34) * i + (height / 2) * j)

            x = 25 + 3 * (width / 12)
            x_1 = 25 + 4 * (width / 12)

            '''Helps print left and right'''
            for k in range(2):

                '''Sets coords for horizontal left side'''
                if not (k):
                    pt1 = Point(x, y)
                    pt2 = Point(x_1, y)

                else:
                    '''Sets coords for horizontal right side'''
                    pt1 = Point(width - x, y)
                    pt2 = Point(width - x_1, y)

                '''Prints horizontal line'''
                ln = Line(pt1, pt2)
                ln.setOutline(color_rgb(255, 255, 255))
                ln.draw(win)

                '''Prints the team on the line'''
                if not (k):
                    write_in_team((x_1-(x_1 - x)/2), y - 8, arr, i, j, k, order, 8)
                else:
                    write_in_team(width - (x_1-((x_1 - x)/2)), y - 8, arr, i, j, k, order, 8)


            '''Prints vertical lines'''
            if (flip_flop):
                for k in range(2):
                    y = (25 + 3.5 * (height / 34) + (8 * height / 34) * i + (height / 2) * j)
                    y_1 = (25 + 3.5 * (height / 34) + (8 * height /34) * (i + 1) + (height / 2) * j)

                    x = 25 + 4 * (width / 12)

                    '''Sets the coords for left side'''
                    if not (k):
                        pt1 = Point(x, y)
                        pt2 = Point(x, y_1)

                    else:
                        '''Sets coords for right side'''
                        pt1 = Point(width - x, y)
                        pt2 = Point(width - x, y_1)

                    '''Prints vertical lines'''
                    ln = Line(pt1, pt2)
                    ln.setOutline(color_rgb(255, 255, 255))
                    ln.draw(win)

            '''Switches flip flop'''
        if (flip_flop):
            flip_flop = 0
        else:
            flip_flop = 1

'''Simulates final 4'''
def F4(height, width, arr, order):
    flip_flop = 1
    for i in range(1):

        for j in range(2):
            y = (25 + 7.5 * (height / 34) + (8* height / 34) * i + (height / 2) * j)

            x = 25 + 4 * (width / 12)
            x_1 = 25 + 5 * (width / 12)

            # Prints horizontal lines
            for k in range(2):

                # Prints left side
                if not (k):
                    pt1 = Point(x, y)
                    pt2 = Point(x_1, y)

                # Prints right side
                else:
                    pt1 = Point(width - x, y)
                    pt2 = Point(width - x_1, y)

                ln = Line(pt1, pt2)
                ln.setOutline(color_rgb(255, 255, 255))
                ln.draw(win)

                if not (k):
                    write_in_team((x_1-(x_1 - x)/2), y - 8, arr, i, j, k, order, 4)
                else:
                    write_in_team(width - (x_1-((x_1 - x)/2)), y - 8, arr, i, j, k, order, 4)

            # Prints vertical lines
        if (flip_flop):
            for k in range(2):
                y = (25 + 7.5 * (height / 34) + (8 * height / 34) * i + (height / 2) * 0)
                y_1 = (25 + 16.5 * (height / 34) + (8 * height /34) * (i + 1) + (height / 2) * 0)

                x = 25 + 5 * (width / 12)

                # Prints left side
                if not (k):
                    pt1 = Point(x, y)
                    pt2 = Point(x, y_1)

                # Prints right side
                else:
                    pt1 = Point(width - x, y)
                    pt2 = Point(width - x, y_1)

                ln = Line(pt1, pt2)
                ln.setOutline(color_rgb(255, 255, 255))
                ln.draw(win)

        if (flip_flop):
            flip_flop = 0
        else:
            flip_flop = 1

'''Simualtes championship game'''
def C(height, width, arr, order):


        '''Sets proper unique coordinates for horizontal line'''
        y = (25 + 7.5 * (height / 34) + (8* height / 34))

        x = 25 + 5 * (width / 12)
        x_1 = 25 + 6.61 * (width / 12)

        pt1 = Point(x, y)
        pt2 = Point(x_1, y)

        '''Prints horizontal line'''
        ln = Line(pt1, pt2)
        ln.setOutline(color_rgb(255, 255, 255))
        ln.draw(win)



        for i in range (2):
            seed = (arr[i][0])[1:3]
            if (int(seed) < 10):
                seed = seed[1]

            team = arr[i][1]
            for z in range(len(names)):  # For each team ID in 2022 tourney
                if (team == names[z][0]):  # if IDS ==
                    team = names[z][1]  # Set ID to name

            team_write = str(team) + ' (' + str(seed) + ')'

            if not (i):
                team_write = ' (' + str(seed) + ')' + str(team)

            print(team)
            txt = Text(Point(x+80+50*i, y-12+25*i), team_write)
            txt.setTextColor(color_rgb(255, 255, 255))
            txt.setSize(8)
            txt.setFace('courier')
            txt.draw(win)





def write_in_team(x, y, arr, i, j, k, order, size):


    '''Selects correct team to be printed'''
    team = (arr[i + k * int(size/2) + j * int(size/4)][1])
    for z in range(len(names)):  # For each team ID in 2022 tourney
        if (team == names[z][0]):  # if IDS ==
            team = names[z][1]  # Set ID to name


    seed = (arr[i + k * int(size/2) + j * int(size/4)][0])[1:3]
    if (int(seed) <10):
        seed = seed[1]

    team_write = str(team) + ' (' + str(seed) + ')'
    if not (k):
        team_write = ' (' + str(seed) + ')' + str(team)

    txt = Text(Point(x,y), team_write)
    txt.setTextColor(color_rgb(255, 255, 255))
    txt.setSize(9)
    txt.setFace('courier')
    txt.draw(win)

def display_winner(width, height, seeds_year_ordered, year):

    '''Properly displays the winner with unique coordinates'''
    x = width/2
    y = height/6

    team = seeds_year_ordered[0][1]
    for z in range(len(names)):  # For each team ID in 2022 tourney
        if (team == names[z][0]):  # if IDS ==
            team = names[z][1]  # Set ID to name

    txt = Text(Point(x,y),'Champions: ' + str(team))
    txt.setTextColor(color_rgb(255, 255, 255))
    txt.setSize(22)
    txt.setFace('courier')
    txt.draw(win)

    txt = Text(Point(x,y/2), year)
    txt.setTextColor(color_rgb(255, 255, 255))
    txt.setSize(22)
    txt.setFace('courier')
    txt.draw(win)





def change_location(loc):
    if loc =='H':
        return 'A'
    elif loc =='A':
        return 'H'
    else:
        return 'H'


if __name__ == "__main__":

    '''Reads in data'''
    seedsData = pd.read_csv("MNCAATourneySeeds.csv")
    print("\n\n\nSeeds Data")
    print(seedsData)

    conferences = pd.read_csv("MteamConferences.csv")
    print("\n\n\nConferences")
    print(conferences)

    detailedRegularSeason = pd.read_csv("MRegularSeasonDetailedResults.csv")
    print("\n\n\n Detailed regular season")
    print(detailedRegularSeason)

    compactTournamentInfo = pd.read_csv("MNCAATourneyCompactResults.csv")
    print("\n\n\n tournament info")
    print(compactTournamentInfo)

    WTeams = pd.DataFrame()
    LTeams = pd.DataFrame()

    columns = ['Season', 'TeamID', 'Points', 'OppPoints', 'Loc', 'NumOT',
     'FGM', 'FGA', 'FGM3', 'FGA3', 'FTM', 'FTA', 'OR', 'DR', 'Ast', 'TO',
     'Stl', 'Blk', 'PF', 'OppFGM', 'OppFGA', 'OppFGM3', 'OppFGA3', 'OppFTM', 'OppFTA', 'OppOR',
     'OppDR', 'OppAst', 'OppTO', 'OppStl', 'OppBlk', 'OppPF']

    WTeams[columns] = detailedRegularSeason[['Season', 'WTeamID', 'WScore', 'LScore', 'WLoc', 'NumOT',
     'WFGM', 'WFGA', 'WFGM3', 'WFGA3', 'WFTM', 'WFTA', 'WOR', 'WDR', 'WAst', 'WTO',
     'WStl', 'WBlk', 'WPF', 'LFGM', 'LFGA', 'LFGM3', 'LFGA3', 'LFTM', 'LFTA', 'LOR',
     'LDR', 'LAst', 'LTO', 'LStl', 'LBlk', 'LPF']]
    WTeams['Wins'] = 1
    WTeams['Losses'] = 0

    print("\n\n\n Wteams")
    print(WTeams)

    LTeams[columns] = detailedRegularSeason[['Season', 'LTeamID', 'LScore', 'WScore', 'WLoc', 'NumOT',
     'LFGM', 'LFGA', 'LFGM3', 'LFGA3', 'LFTM', 'LFTA', 'LOR', 'LDR', 'LAst', 'LTO',
     'LStl', 'LBlk', 'LPF', 'WFGM', 'WFGA', 'WFGM3', 'WFGA3', 'WFTM', 'WFTA', 'WOR',
     'WDR', 'WAst', 'WTO', 'WStl', 'WBlk', 'WPF']]
    LTeams['Loc'] = LTeams['Loc'].apply(change_location)
    LTeams['Wins'] = 0
    LTeams['Losses'] = 1

    print("\n\n\n LTeams")
    print(LTeams)

    WinLTeams = pd.concat([WTeams, LTeams])

    print("\n\n\n WinLTeams")
    print(WinLTeams)

    BothTeams = WinLTeams.groupby(['Season', 'TeamID']).sum()
    print("\n\n\n Both Teams")
    print(BothTeams)

    BothTeams['NumGames'] = BothTeams['Wins'] + BothTeams['Losses']




    RegSeasonData = pd.DataFrame()

    RegSeasonData['WinRatio'] = BothTeams['Wins']/BothTeams['NumGames']
    RegSeasonData['PointsPerGame'] = BothTeams['Points'] / BothTeams['NumGames']
    RegSeasonData['PointsAllowedPerGame'] = BothTeams['OppPoints'] / BothTeams['NumGames']
    RegSeasonData['PointsRatio'] = BothTeams['Points'] / BothTeams['OppPoints']
    RegSeasonData['OTPerGame'] = BothTeams['NumOT'] / BothTeams['NumGames']

    RegSeasonData['FGPerGame'] = BothTeams['FGM'] / BothTeams['NumGames']
    RegSeasonData['FGRatio'] = BothTeams['FGM'] / BothTeams['FGA']
    RegSeasonData['FGAllowedPerGame'] = BothTeams['OppFGM'] / BothTeams['NumGames']

    RegSeasonData['FG3PerGame'] = BothTeams['FGM3'] / BothTeams['NumGames']
    RegSeasonData['FG3Ratio'] = BothTeams['FGM3'] / BothTeams['FGA3']
    RegSeasonData['FG3AllowedPerGame'] = BothTeams['OppFGM3'] / BothTeams['NumGames']

    RegSeasonData['FTPerGame'] = BothTeams['FTM'] / BothTeams['NumGames']
    RegSeasonData['FTRatio'] = BothTeams['FTM'] / BothTeams['FTA']
    RegSeasonData['FTAllowedPerGame'] = BothTeams['OppFTM'] / BothTeams['NumGames']

    RegSeasonData['ORRatio'] = BothTeams['OR'] / (BothTeams['OR'] + BothTeams['OppDR'])
    RegSeasonData['DRRatio'] = BothTeams['DR'] / (BothTeams['DR'] + BothTeams['OppOR'])

    RegSeasonData['AstPerGame'] = BothTeams['Ast'] / BothTeams['NumGames']
    RegSeasonData['TOPerGame'] = BothTeams['TO'] / BothTeams['NumGames']
    RegSeasonData['StlPerGame'] = BothTeams['Stl'] / BothTeams['NumGames']
    RegSeasonData['BlkPerGame'] = BothTeams['Blk'] / BothTeams['NumGames']
    RegSeasonData['PFPerGame'] = BothTeams['PF'] / BothTeams['NumGames']


    print("\n\n\n Regular Season data")
    print(RegSeasonData)

    print("\n\n\n Stats used")
    print(RegSeasonData.columns.values)

    '''
    conferences2 = conferences.groupby(['Season', 'TeamID']).sum()


    power6 = []
    for index, row in RegSeasonData.iterrows():
        ct = 0
        season, team_id = index


        conf = conferences2.loc[index].values[0]
        if (conf == 'sec' or conf == 'big_east' or conf == 'big_ten' or
                conf == 'acc' or conf == 'pac_twelve' or conf == 'big_twelve' or
                conf == 'pac_ten'):
            val = 1
        else:
            val = 0

        power6.append(val)
        ct = ct + 1

    #RegSeasonData['Power6'] = None
    RegSeasonData['Power6'] = power6
    '''


    seed_dict = seedsData.set_index(['Season', 'TeamID'])
    print("\n\n\n Seed Dict")
    print(seed_dict)

    TourneyInput = pd.DataFrame()
    winIDs = compactTournamentInfo['WTeamID']
    loseIDs = compactTournamentInfo['LTeamID']
    season = compactTournamentInfo['Season']

    winners = pd.DataFrame()
    winners[['Season', 'Team1', 'Team2']] = compactTournamentInfo[['Season', 'WTeamID', 'LTeamID']]
    winners['Result'] = 1

    losers = pd.DataFrame()
    losers[['Season', 'Team1', 'Team2']] = compactTournamentInfo[['Season', 'LTeamID', 'WTeamID']]
    losers['Result'] = 0


    TourneyInput = pd.concat([winners, losers])
    TourneyInput = TourneyInput[TourneyInput['Season']>=2003].reset_index(drop=True)

    team1seeds = []
    team2seeds = []

    print("\n\n\n Tourney Input")
    print(TourneyInput)

    for x in range(len(TourneyInput)):
        index = (TourneyInput['Season'][x], TourneyInput['Team1'][x])
        seed = seed_dict.loc[index].values[0]
        if len(seed) == 4:
            seed = int(seed[1:-1])
        else:
            seed = int(seed[1:])
        team1seeds.append(seed)

    for x in range(len(TourneyInput)):
        index = (TourneyInput['Season'][x], TourneyInput['Team2'][x])
        seed = seed_dict.loc[index].values[0]
        if len(seed) == 4:
            seed = int(seed[1:-1])
        else:
            seed = int(seed[1:])
        team2seeds.append(seed)

    TourneyInput['Team1Seed'] = team1seeds
    TourneyInput['Team2Seed'] = team2seeds




    scores = []

    print("\n\n\n Tourney Input")
    print(TourneyInput)


    '''For each Tournament game, create train data scores'''
    for x in range(len(TourneyInput)):
        index = (TourneyInput['Season'][x], TourneyInput['Team1'][x])
        team1score = RegSeasonData.loc[index]
        team1score.loc['Seed'] = TourneyInput['Team1Seed'][x]

        index = (TourneyInput['Season'][x], TourneyInput['Team2'][x])
        team2score = RegSeasonData.loc[index]
        team2score['Seed'] = TourneyInput['Team2Seed'][x]

        score = team1score - team2score
        score['Result'] = TourneyInput['Result'][x]
        scores.append(score)

    scores = pd.DataFrame(scores)


    print("\n\n\n scores:")
    print(scores)

    corrs = round(scores.corr(method = 'kendall'), 2)
    print("\n\n\n Correlations: ")
    print(np.abs(corrs['Result']))


    plt.figure(figsize=(15,10))
    sns.heatmap(corrs)
    plt.show()


    x = scores[scores.columns[:-1]].values
    y = scores['Result'].values

    np.random.seed()
    index = np.random.permutation(len(x))
    train_index = index[:int(-.2*len(x))]
    test_index = index[int(-.2*len(x)):]

    x_train = x[train_index]
    x_test = x[test_index]
    y_train = y[train_index]
    y_test = y[test_index]


    mins = x_train.min(axis=0)
    maxes = x_train.max(axis=0)

    x_train = (x_train - mins) / (maxes - mins)
    x_test = (x_test - mins) / (maxes - mins)


    model = rf()
    model = model.fit(x_train, y_train)
    accuracy = model.score(x_test, y_test)

    print("\n\n")
    print("Accuracy: " + str(round(accuracy, 3)))
    print("\n\n")



















    '''Main method'''
    year = get_year()
    method = get_method()


    seeds = pd.read_csv('MNCAATourneySeeds.csv')
    seeds_year = seeds.loc[seeds['Season'] == year]
    seeds_year = seeds_year.to_numpy()
    seeds_year = seeds_year[:, 1:3]  # array of team IDs and seeds

    names = pd.read_csv('MTeams.csv')
    names = names.to_numpy()


    rankings = pd.read_csv('MMasseyOrdinals_thru_Season2023_Day128.csv')
    rankings_year = rankings.loc[((rankings['Season'] == year) & (rankings['SystemName'] == 'POM'))]



    print(seeds_year)
    order = np.array([0,15,7,8,4,11,3,12,5,10,2,13,6,9,1,14])

    win = GraphWin("My Window", 1920*.8 , 1080*.8)
    win.setBackground(color_rgb(0,0,0))
    height = win.getHeight()
    width  = win.getWidth()


    seeds_year = playin_games(seeds_year, method, year)

    '''Reorder seeds to 1,16,8,9,5,12... format'''
    seeds_year_ordered = reorder(seeds_year, order)


    RO64(height, width, seeds_year_ordered, order)

    RO32_teams = det_winners(seeds_year_ordered, 32, method, year)
    RO32(height, width, RO32_teams, order)

    S16_teams= det_winners(RO32_teams, 16, method, year)
    S16(height, width, S16_teams, order)

    E8_teams = det_winners(S16_teams, 8, method, year)
    E8(height, width, E8_teams, order)

    F4_teams = det_winners(E8_teams, 4, method, year)
    F4(height, width, F4_teams, order)

    C_teams = det_winners(F4_teams, 2, method, year)
    C(height, width, C_teams, order)

    C = det_winners(C_teams, 1, method, year)
    display_winner(width, height, C, year)



    win.getMouse()
    win.close()




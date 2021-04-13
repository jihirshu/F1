import pandas as pd
import ssl
import random
import requests
import csv



def main_func(inputs):
    currentUserInput = {}
    currentPref = []
    for i in range(1,6):
        if (inputs[i-1] == 'Y' or inputs[i-1] == 'y'):
            currentUserInput[i] = 1
            currentPref.append(1)
        elif (inputs[i-1] == 'N' or inputs[i-1] == 'n'):
            currentUserInput[i] = 0
            currentPref.append(0)
        else:
            raise IOError('Enter Y or N')

    ssl._create_default_https_context = ssl._create_unverified_context
    df = pd.read_csv('https://s3.amazonaws.com/f1fs001-aws/TrainingData.csv')

    df.Liked.replace(to_replace=['Y','N'], value=[1,0], inplace=True)

    uniqueUsers = df['UserID'].unique()

    data_dict = {}
    preferences = []
    distance = []
    for user in uniqueUsers:
        temp = df[df['UserID'] ==  user]
        data_dict[user] = {}
        for index, row in temp.iterrows():
            data_dict[user][row['ArtistID']] = row['Liked']
        user_pref = []
        sumOfAbsDiff = 0
        for i in range(1,6):
            user_pref.append(data_dict[user][i])
            sumOfAbsDiff = sumOfAbsDiff + abs(currentUserInput[i] - data_dict[user][i])
        distance.append(sumOfAbsDiff)
        preferences.append(user_pref)

    similarUser = distance.index(min(distance)) + 1


    potentialLikes = []

    for i in range(6,26):
        currentUserInput[i] = data_dict[similarUser][i]
        if (data_dict[similarUser][i] == 1):
            potentialLikes.append(i)
    recommendations = []
    if len(potentialLikes)<5:
        recommendations = potentialLikes
    else:
        recommendations = random.sample(potentialLikes, 5)

    recommendations = sorted(recommendations)

    print("You may be interested in : ")

    for likes in recommendations:
        print("Artist {}".format(likes))

    print(currentUserInput)

    currentUser = len(uniqueUsers) + 1
    for key in currentUserInput.keys():
        newLine = [currentUser, key, currentUserInput[key]]
        df.loc[len(df)] = newLine


    df.Liked.replace(to_replace=[1,0], value=['Y','N'], inplace=True)
    df.to_csv("newTrainingData.csv", index=False)

    with open('newTrainingData.csv', 'r') as f:
        r = requests.post('https://f1func-001.azurewebsites.net/api/TrainingDataUpdate?code=2EiVjdBauREP4kyVOXLUDLYCJRjJ1Ud/e6LLqL8YFBg0JP9kTU4XTw==',
                          files={'newTrainingData.csv': f})

    return recommendations
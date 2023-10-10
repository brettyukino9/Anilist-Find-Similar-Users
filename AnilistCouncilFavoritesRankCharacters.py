import csv
import json
import os
import webbrowser
from pip._vendor import requests
import sys
import math
# arg 2 = username


map = {}
username = "higui"

# Make query to get user Id
queryOld = '''
query($name:String){User(name:$name){id}}
'''

# Define our query variables and values that will be used in the query request
variablesOld = {
    'name': username
}

url = 'https://graphql.anilist.co'

# Make the HTTP Api request to get the user id of the username
response = requests.post(url, json={'query': queryOld, 'variables': variablesOld}).json()
userId = response['data']['User']['id']

# Define our query variables and values that will be used in the query request
variables = {
    'userId': userId
}

# Get all user favorites
users = {}
queries = {}
pages = 10 #1200 users per page, 24 a's on a page, 50 users per a
for i in range(1, pages+1) : 
  # 1 = 1,25 = (i-1) * 25 - (i-2) = i * 25 - (i -1 )
  # 2 = 25, 49 = (i-1) * 25 - (i-2) = i * 25 - (i -1 )
  # 3 = 49, 73 = (i-1) * 25 - (i-2) = i * 25 - (i -1 )
  # 4 = 73, 97 = (i-1) * 25 - (i-2) = i * 25 - (i -1 )
  idk = ''
  for x in range((i-1) * 25 - (i-2), i * 25 - (i -1 )) :
    toAdd = "a"+str(x)+''': Page(page: '''+str(x)+''') {
      following(userId: $userId, sort: ID) {
        ...stuff
      }
    }
    '''
    idk = idk+toAdd

  query ='''
    query ($userId: Int!) { '''+idk+ ''' User(id: $userId) {
      ...stuff
    }
  }

  fragment stuff on User {
    name
    favourites {
      characters1: characters(page: 1) {
        nodes {
          name {
            full
          }
        }
      }
      characters2: characters(page: 2) {
        nodes {
          name {
            full
          }
        }
      }
      characters3: characters(page: 3) {
        nodes {
          name {
            full
          }
        }
      }
      characters4: characters(page: 4) {
        nodes {
          name {
            full
          }
        }
      }
    }
  }
  '''
  users[i] = requests.post(url, json={'query': query, 'variables': variables}).json()
  print(users[i])


# Make query to get user favorites
chars = []
username2 = sys.argv[1]
query = '''
query ($name: String!) {
  User(name: $name) {
    ...stuff
  }
}

fragment stuff on User {
  name
  favourites {
    characters1: characters(page:1) {
      nodes {
        name {
          full
        }
      }
    }
    characters2: characters(page:2) {
      nodes {
        name {
          full
        }
      }
    }
    characters3: characters(page:3) {
      nodes {
        name {
          full
        }
      }
    }
    characters4: characters(page:4) {
      nodes {
        name {
          full
        }
      }
    }

  }
}

'''

# Define our query variables and values that will be used in the query request
variables = {
    'name': username2
}

# Make the HTTP Api request to get the users favorite characters
response2 = requests.post(url, json={'query': query, 'variables': variables}).json()
print(response2)


#Get user favorites
for x in range(1,2) : 
    for i in response2['data']['User']['favourites']['characters'+str(x)]['nodes']:
        chars.append(i['name']['full'])

# Go through everyones favorites
count = 0
for x in range(1, pages * 25 - (pages -1 )) :
    num = math.floor((x-1)/24)+1
    for user in users[num]['data']['a'+str(x)]['following'] :
      name = user['name']
      count +=1
      for y in range(1,5) :
          for i in user['favourites']['characters'+str(y)]['nodes']:
              char = i['name']['full']
              if(char in chars) :
                  if(name in map) :
                      map[name] = map[name] + 1
                  else :
                      map[name] = 1

res = {key: val for key, val in sorted(map.items(), key = lambda ele: ele[1], reverse = True)}
[print(key,':',value) for key, value in res.items()]
with open('Characters Results/'+username2+' results.txt', 'w', encoding='utf8') as f:
    f.write("Number of shared favorite characters between " + username2+" and x user")
    f.write("-----------------------------------------------------------------------\n")
    for key, value in res.items() :
        f.write(key+' : '+str(value)+"\n")

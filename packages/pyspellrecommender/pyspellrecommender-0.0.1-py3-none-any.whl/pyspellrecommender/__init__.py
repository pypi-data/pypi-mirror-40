import requests
import json


class SpellRecommender:
  def __init__(self):
    self.url = 'https://api.textgears.com/check.php'
    self.key = 'zHOhWHCGjaqGed7M'

  def padtext(self, sentence):
    allText = sentence.split()
    return "+".join(allText)

  def recommend(self, text):
    PARAMS = { 'text': self.padtext(text), 'key': self.key }
    r = requests.get(url = self.url, params= PARAMS)
    binary = r.content
    res = json.loads(binary)
    errors = res['errors']
    recommend = {}
    i = 0
    for error in errors:
      recommend[i]= {}
      bad = error['bad']
      recommend[i]['error'] = bad
      solutions = []
      for better in error['better']:
        solutions.append(better)
      recommend[i]['solution'] = solutions
      i += 1
    return recommend

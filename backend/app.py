from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
import subprocess
import os
import os.path
import json
from dotenv import load_dotenv
from data_wrangle.rfc_model import ReviewModel
from data_wrangle.nn_model import NnModel
from data_wrangle.text_review import Reviewer
from data_wrangle.dataset_manager import datasetManager
from data_wrangle.adj_finder import TagFinder
import essentia
import essentia.standard as es

app = Flask(__name__)
CORS(app)
load_dotenv()
model = ReviewModel()
nn_model = NnModel()
reviewer = Reviewer()
datasetManager = datasetManager()
tagger = TagFinder()

@app.route("/api/ping")
def ping():
  return "pong"

@app.route('/api/upload', methods=['POST'])
def upload():
  file = request.files['song']
  file.save('./temp.wav')
  features, features_frames = es.MusicExtractor(lowlevelStats=['mean'],
                                              rhythmStats=['mean'],
                                              tonalStats=['mean'])('./temp.wav')
  row = []
  row.append(features['lowlevel.spectral_complexity.mean'])
  row.append(features['lowlevel.average_loudness'])
  row.append(features['lowlevel.dissonance.mean'])
  row.append(features['lowlevel.pitch_salience.mean'])
  row.append(features['tonal.tuning_frequency'])
  row.append(features['tonal.chords_strength.mean'])
  row.append(features['rhythm.bpm'])
  row.append(features['rhythm.danceability'])
  row.append(features['rhythm.beats_count'])
  row.append(features['metadata.audio_properties.length'])
  row.extend(map_key(features['tonal.chords_key']))

  score = model.predict(row)
  neighbors = nn_model.kneighbors(1000, row)
  review = reviewer.generate(neighbors[0])
  nearest_neighbors = nn_model.kneighbors(15, row)
  similar_songs = datasetManager.get_similar_songs(nearest_neighbors[0])
  tags = tagger.generate(neighbors[0][:100])

  data = {
    'spectral_complexity': features['lowlevel.spectral_complexity.mean'],
    'average_loudness': features['lowlevel.average_loudness'],
    'dissonance': features['lowlevel.dissonance.mean'],
    'pitch_salience': features['lowlevel.pitch_salience.mean'],
    'tuning_frequency': features['tonal.tuning_frequency'],
    'chords_strength': features['tonal.chords_strength.mean'],
    'bpm': features['rhythm.bpm'],
    'danceability': features['rhythm.danceability'],
    'beats_count': features['rhythm.beats_count'],
    'length': features['metadata.audio_properties.length'],
    'chords_key': features['tonal.chords_key'],
    'score': int(score[0]),
    'neighbors': str(neighbors[0]),
    'review': review,
    'nearest': str(nearest_neighbors[0]),
    'similar_songs': similar_songs,
    'tags':tags

  }
  # data['score'] = int(score[0])
  return jsonify(data)

@app.route('/api/attributes', methods=['POST'])
def attributes():
  features = request.get_json()
  row = []
  row.append(features['spectral_complexity'])
  row.append(features['average_loudness'])
  row.append(features['dissonance'])
  row.append(features['pitch_salience'])
  row.append(features['tuning_frequency'])
  row.append(features['chords_strength'])
  row.append(features['bpm'])
  row.append(features['danceability'])
  row.append(features['beats_count'])
  row.append(features['length'])
  row.extend(map_key(features['chords_key']))
  
  score = model.predict(row)
  neighbors = nn_model.kneighbors(1000, row)
  review = reviewer.generate(neighbors[0])
  nearest_neighbors = nn_model.kneighbors(15, row)
  similar_songs = datasetManager.get_similar_songs(nearest_neighbors[0])
  tags = tagger.generate(neighbors[0][:100])
  data = {
    'spectral_complexity': features['spectral_complexity'],
    'average_loudness': features['average_loudness'],
    'dissonance': features['dissonance'],
    'pitch_salience': features['pitch_salience'],
    'tuning_frequency': features['tuning_frequency'],
    'chords_strength': features['chords_strength'],
    'bpm': features['bpm'],
    'danceability': features['danceability'],
    'beats_count': features['beats_count'],
    'length': features['length'],
    'chords_key': features['chords_key'],
    'score': int(score[0]),
    'neighbors': str(neighbors[0]),
    'review': review,
    'similar_songs': similar_songs,
    'tags':tags
  }
  # data['score'] = int(score[0])
  return jsonify(data)

def map_key(key):
  # A#, C, D, D#, E, F#, G, G# 
  keys = {
    'A#': [1, 0, 0, 0, 0, 0, 0, 0],
    'C': [0, 1, 0, 0, 0, 0, 0, 0],
    'D': [0, 0, 1, 0, 0, 0, 0, 0],
    'D#': [0, 0, 0, 1, 0, 0, 0, 0],
    'E': [0, 0, 0, 0, 1, 0, 0, 0],
    'F#': [0, 0, 0, 0, 0, 1, 0, 0],
    'G': [0, 0, 0, 0, 0, 0, 1, 0],
    'G#': [0, 0, 0, 0, 0, 0, 0, 1]
  }
  if key in keys:
    return keys[key]
  else:
    return [0, 0, 0, 0, 0, 0, 0, 0]

"""
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return send_from_directory('./build/', 'index.html')
"""
if __name__ == '__main__':
    app.run("0.0.0.0", port=8000, debug=True)

import React, { Component } from 'react'
import 'semantic-ui-css/semantic.min.css'
import { Button, Container, Header, List, Segment } from 'semantic-ui-react'
import axios from 'axios'
import './App.css'

class App extends Component {
  state = {
    song: undefined
  }

  componentDidMount() {
    // axios.get('http://localhost:8000/api/ping').then(res => console.log(res))
  }

  getJson = () => {
    axios.get('http://localhost:8000/api/json').then(res => this.setState({ song: res.data }))
  }

  render() {
    const { song } = this.state
    console.log(song)
    return (
      <Container>
        <Header as="h1">Music review generator</Header>
        <label htmlFor="uploader">Select a song</label>
        <input id="uploader" type="file" />
        <Button content="submit" onClick={this.getJson}/>
        {song ?
        <div>
          <Header as="h2" content="Attributes of your song" /> 
          <List>
            <List.Item>average_loudness: {song.lowlevel.average_loudness.toFixed(2)}</List.Item>
            <List.Item>dissonance mean: {song.lowlevel.dissonance.mean.toFixed(2)}</List.Item>
            <List.Item>dynamic_complexity: {song.lowlevel.dynamic_complexity.toFixed(2)}</List.Item>
            <List.Item>pitch_salience mean: {song.lowlevel.pitch_salience.mean.toFixed(2)}</List.Item>
            <List.Item>spectral_complexity mean: {song.lowlevel.spectral_complexity.mean.toFixed(2)}</List.Item>

            <List.Item>chords_scale: {song.tonal.chords_scale}</List.Item>
            <List.Item>chords_key: {song.tonal.chords_key}</List.Item>
            <List.Item>tuning_frequency: {song.tonal.tuning_frequency.toFixed(2)}</List.Item>
            <List.Item>chords_strength mean: {song.tonal.chords_strength.mean.toFixed(2)}</List.Item>
            <List.Item>chords_changes_rate: {song.tonal.chords_changes_rate.toFixed(2)}</List.Item>

            <List.Item>bpm: {song.rhythm.bpm.toFixed(2)}</List.Item>
            <List.Item>danceability: {song.rhythm.danceability.toFixed(2)}</List.Item>
            <List.Item>beats_count: {song.rhythm.beats_count.toFixed(2)}</List.Item>
            
            <List.Item>audio_properties length: {song.metadata.audio_properties.length.toFixed(2)}</List.Item>
          </List>
          <Header as="h2" content="Song review" />
          <Header as="h3" content="Score: 5/5" />
          <Segment>
            This song is definately _____. The sound is really ____.
          </Segment>
          <Header as="h3" content="Estimated popularity: 500k views on Youtube" />
        </div>
        : undefined}
      </Container>
    )
  }
}

export default App

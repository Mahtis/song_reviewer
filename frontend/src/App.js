import React, { Component } from 'react'
import 'semantic-ui-css/semantic.min.css'
import { Button, Container, Form, Header, Input, Label, List, Segment } from 'semantic-ui-react'
import axios from 'axios'
import './App.css'

class App extends Component {
  state = {
    song: undefined,
    file: {}
  }

  componentDidMount() {
    // axios.get('http://localhost:8000/api/ping').then(res => console.log(res))
  }

  getJson = () => {
    axios.get('http://localhost:8000/api/json').then(res => this.setState({ song: res.data }))
  }

  handleChange = (e) => {
    const file = e.target.files[0]
    // console.log(file)
    if (file && file !== this.state.file) {
      this.setState({ file })
    } else {
      this.setState({ file: {} })
    }
  }

  submitForm = (e) => {
    e.preventDefault()
    const form = new FormData()
    console.log(this.state.file)
    form.append('song', this.state.file)
    axios.post('http://localhost:8000/api/upload', form).then((res) => this.setState({ song: res.data }))
  }

  render() {
    const { song } = this.state
    console.log(song)
    return (
      <Container>
        <Header as="h1">Music review generator</Header>
        <Form onSubmit={this.submitForm}>
          <Label htmlFor="uploader">Select a song</Label>
          <Input id="uploader" type="file" onChange={this.handleChange} />
          <Button content="submit" type="submit" />
        </Form>
        {song ?
        <div>
          <Header as="h2" content="Attributes of your song" /> 
          <List>
            <List.Item>average_loudness: {song.average_loudness.toFixed(2)}</List.Item>
            <List.Item>dissonance mean: {song.dissonance.toFixed(2)}</List.Item>
            {/* <List.Item>dynamic_complexity: {song.dynamic_complexity.toFixed(2)}</List.Item> */}
            <List.Item>pitch_salience mean: {song.pitch_salience.toFixed(2)}</List.Item>
            <List.Item>spectral_complexity mean: {song.spectral_complexity.toFixed(2)}</List.Item>

            {/* <List.Item>chords_scale: {song.chords_scale}</List.Item> */}
            <List.Item>chords_key: {song.chords_key}</List.Item>
            <List.Item>tuning_frequency: {song.tuning_frequency.toFixed(2)}</List.Item>
            <List.Item>chords_strength mean: {song.chords_strength.toFixed(2)}</List.Item>
            {/* <List.Item>chords_changes_rate: {song.chords_changes_rate.toFixed(2)}</List.Item> */}

            <List.Item>bpm: {song.bpm.toFixed(2)}</List.Item>
            <List.Item>danceability: {song.danceability.toFixed(2)}</List.Item>
            <List.Item>beats_count: {song.beats_count.toFixed(2)}</List.Item>
            
            <List.Item>audio_properties length: {song.length.toFixed(2)}</List.Item>
          </List>
          <Header as="h2" content="Song review" />
          <Header as="h3" content={`Score: ${song.score}/5`} />
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

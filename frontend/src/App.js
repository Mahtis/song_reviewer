import React, { Component } from 'react'
import 'semantic-ui-css/semantic.min.css'
import { Button, Container, Form, Grid, Header, Input, Label, List, Loader, Segment } from 'semantic-ui-react'
import axios from 'axios'
import './App.css'

const API_URL = process.env.NODE_ENV === 'development' ? 'http://localhost:8000/api' : 'http://song-reviewer.mahtisoft.com/api'

class App extends Component {
  state = {
    song: undefined,
    customValues: {
      average_loudness: 0,
      dissonance: 0,
      pitch_salience: 0,
      spectral_complexity: 0,
      chords_key: 'C',
      tuning_frequency: 0,
      chords_strength: 0,
      bpm: 0,
      danceability: 0,
      beats_count: 0,
      length: 0,
      score: 0
    },
    file: {},
    loading: false
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

  submitForm = async (e) => {
    e.preventDefault()
    const form = new FormData()
    console.log(this.state.file)
    form.append('song', this.state.file)
    await this.setState({ loading: true })
    axios.post(`${API_URL}/upload`, form).then((res) => this.setState({ song: res.data, loading: false }))
  }

  submitAttributes = async (e) => {
    e.preventDefault()
    await this.setState({ loading: true })
    axios.post(`${API_URL}/attributes`, this.state.customValues)
      .then((res) => this.setState({ song: res.data, loading: false }))
  }

  changeValue = (e, { value }) => {
    const customValues = { ...this.state.customValues }
    customValues[e.target.name] = e.target.name === 'chords_key' ? value : Number(value)
    this.setState({ customValues })
  }

  render() {
    console.log(this.state)
    const { song, loading, customValues } = this.state
    return (
      <Container>
        <Grid columns={2}>
          <Grid.Row>
            <Grid.Column>
        <Loader active={loading} />
        <Header as="h1">Music review generator</Header>
        <Form onSubmit={this.submitForm}>
          <Label htmlFor="uploader">Select a song</Label>
          <Input id="uploader" accept=".wav" type="file" onChange={this.handleChange} />
          <Button content="submit" type="submit" />
        </Form>
        </Grid.Column>
        </Grid.Row>
        <Grid.Row>
        {song ?
        <Grid.Column>
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
        </Grid.Column>
        : undefined}
        <Grid.Column>
          <Form onSubmit={this.submitAttributes}>
            <Header as="h2">
              Get review by custom attributes <Button content="submit attributes" /></Header>
            <List>
              <List.Item>
                average_loudness:
                <Input
                  name='average_loudness'
                  type="number"
                  size="mini"
                  value={customValues.average_loudness}
                  onChange={this.changeValue}
                />
              </List.Item>
              <List.Item>
                dissonance:
                <Input
                  name='dissonance'
                  type="number"
                  size="mini"
                  value={customValues.dissonance}
                  onChange={this.changeValue}
                />
              </List.Item>
              <List.Item>
                pitch_salience:
                <Input
                  name='pitch_salience'
                  type="number"
                  size="mini"
                  value={customValues.pitch_salience}
                  onChange={this.changeValue}
                />
              </List.Item>
              <List.Item>
                spectral_complexity:
                <Input
                  name='spectral_complexity'
                  type="number"
                  size="mini"
                  value={customValues.spectral_complexity}
                  onChange={this.changeValue}
                />
              </List.Item>
              <List.Item>
                chords_key:
                <Input
                  name='chords_key'
                  type="text"
                  size="mini"
                  value={customValues.chords_key}
                  onChange={this.changeValue}
                />
              </List.Item>
              <List.Item>
                tuning_frequency:
                <Input
                  name='tuning_frequency'
                  type="number"
                  size="mini"
                  value={customValues.tuning_frequency}
                  onChange={this.changeValue}
                />
              </List.Item>
              <List.Item>
                chords_strength:
                <Input
                  name='chords_strength'
                  type="number"
                  size="mini"
                  value={customValues.chords_strength}
                  onChange={this.changeValue}
                />
              </List.Item>
              <List.Item>
                bpm:
                <Input
                  name='bpm'
                  type="number"
                  size="mini"
                  value={customValues.bpm}
                  onChange={this.changeValue}
                />
              </List.Item>
              <List.Item>
                danceability:
                <Input
                  name='danceability'
                  type="number"
                  size="mini"
                  value={customValues.danceability}
                  onChange={this.changeValue}
                />
              </List.Item>
              <List.Item>
                beats_count:
                <Input
                  name='beats_count'
                  type="number"
                  size="mini"
                  value={customValues.beats_count}
                  onChange={this.changeValue}
                />
              </List.Item>
              <List.Item>
                length:
                <Input
                  name='length'
                  type="number"
                  size="mini"
                  value={customValues.length}
                  onChange={this.changeValue}
                />
              </List.Item>
            </List>
          </Form>
        </Grid.Column>
        </Grid.Row>
        </Grid>
      </Container>
    )
  }
}

export default App

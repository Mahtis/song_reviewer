import React, { Component } from 'react'
import 'semantic-ui-css/semantic.min.css'
import { Button, Container, Dimmer, Form, Grid, Header, Icon, Input, Label, List, Loader, Message, Segment } from 'semantic-ui-react'
import axios from 'axios'
import './App.css'

const API_URL = process.env.NODE_ENV === 'development' ? 'http://localhost:8000/api' : 'http://song-reviewer.mahtisoft.com/api'

// Plz no steling this okthx
const YOUTUBE_API_KEY = 'AIzaSyDfbfuc5Z7rpdeWyC4AG2t5TNtfjJRHTSE'

class App extends Component {
  state = {
    song: undefined,
    customValues: {
      average_loudness: 0.9,
      dissonance: 0.5,
      pitch_salience: 0.5,
      spectral_complexity: 38,
      chords_key: 'C#',
      tuning_frequency: 440,
      chords_strength: 0.5,
      bpm: 92,
      danceability: 1.2,
      beats_count: 164,
      length: 107
    },
    file: {},
    loading: false,
    youtubePredictions: undefined
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

  getYoutubeViews = async () => {
    const { similar_songs: songs } = this.state.song
    const songAmounts = await Promise.all(songs.map(async song => {
      const searchResults = await axios.get('https://www.googleapis.com/youtube/v3/search', {
        params: {
          key: YOUTUBE_API_KEY,
          part: 'snippet',
          type: 'video',
          q: `${song.artist} ${song.title}`
        }
      })
      const stats = await Promise.all(searchResults.data.items.map(async (video) => {
        const videoStats = await axios.get('https://www.googleapis.com/youtube/v3/videos', {
          params: {
            id: video.id.videoId,
            key: YOUTUBE_API_KEY,
            part: 'statistics'
          }
        })
        return { 
          views: Number(videoStats.data.items[0].statistics.viewCount) || 0,
          likes: Number(videoStats.data.items[0].statistics.likeCount) || 0,
          dislikes: Number(videoStats.data.items[0].statistics.dislikeCount || 0)
        }
      }))
      const songStats = stats.reduce((acc, cur) => ({
        views: acc.views + cur.views,
        likes: acc.likes + cur.likes,
        dislikes: acc.dislikes + cur.dislikes
      }), { views: 0, likes: 0, dislikes: 0 })
      console.log('song stats', songStats)
      return songStats
    }))
    const predictions = songAmounts.reduce((acc, cur) => ({
      views: acc.views + (cur.views / songAmounts.length),
      likes: acc.likes + (cur.likes / songAmounts.length),
      dislikes: acc.dislikes + (cur.dislikes / songAmounts.length)
    }), { views: 0, likes: 0, dislikes: 0 })
    console.log('predictions', predictions)
    this.setState({ youtubePredictions: predictions })
    // https://www.googleapis.com/youtube/v3/search?key=AIzaSyDfbfuc5Z7rpdeWyC4AG2t5TNtfjJRHTSE&part=snippet&type=video&q=surfing
    // https://www.googleapis.com/youtube/v3/videos?id=7lCDEYXw3mM&key=AIzaSyDfbfuc5Z7rpdeWyC4AG2t5TNtfjJRHTSE&part=statistics
  }

  changeValue = (e) => {
    const customValues = { ...this.state.customValues }
    customValues[e.target.name] = e.target.name === 'chords_key'
      ? e.target.value : Number(e.target.value)
    this.setState({ customValues })
  }


  render() {
    console.log(this.state)
    const { song, loading, customValues, youtubePredictions } = this.state
    return (
      <Container style={{background: '#F7F5F4'}}>
        <Grid columns={2}>
          <Grid.Row>
            <Grid.Column>
              <Header as="h1"><Header.Subheader>Welcome to the</Header.Subheader>Music review generator</Header>
              <Message floating info>
                <p>This great application helps you see, how good that new song you've been working on actually is!</p>
                <p>Just upload a .wav -version of your song below and click submit to create a review for it.</p>
                <p>The application will anlyse the audio properties of the song and generate a numerical score for it on a scale of 1 to 5.</p>
                <p>You will also receive a textual review of the song, along with a list of words that most closely
                describe the song. To top it off, you will receive a list of similar songs and the option to
                predict the success of your song in terms of Youtube views and likes.</p>
              </Message>
              <Form onSubmit={this.submitForm}>
                <Label attached="top left" color="teal" htmlFor="uploader" pointing="below">Select a song</Label>
                <Input id="uploader" accept=".wav" type="file" onChange={this.handleChange} />
                <Button color="blue" content="submit" type="submit" />
              </Form>
            </Grid.Column>
          </Grid.Row>
        <Grid.Row>
          <Dimmer active={loading} inverted={true}>
            <Loader />
          </Dimmer>
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
          <Header as="h3">
            Tags related to this song: {song.tags.map(tag => <Label color="violet" size="large">{tag}</Label>)}
          </Header>
          <Segment>
              {song.review.map(i => <div key={i}>{i}</div>) }
          </Segment>
          <Header as="h3" content="Similar songs:" />
          <Segment>
              {song.similar_songs.map(s => <div key={s.title}>{s.artist} - {s.title} ({s.genre})</div>)}
          </Segment>
          {youtubePredictions 
            ? <Header as="h3"> 
                Estimated popularity:
                <p>{Math.floor(youtubePredictions.views)} views on Youtube</p>
                <p>{Math.floor(youtubePredictions.likes)} <Icon name="thumbs up" /> likes</p>
                <p>{Math.floor(youtubePredictions.dislikes)} <Icon name="thumbs down" /> dislikes</p>
              </Header>
            : <div>
                <Header as="h3" content="The popularity of your song is not yet calculated" />
                <Button color="red" content="Youtube views!" onClick={this.getYoutubeViews}/>
              </div>}
        </Grid.Column>
        : undefined}
        <Grid.Column>
          <Segment>
            <p>In case you don't have a song available, but want to test the song-reviewer,
            you can insert some audio properties and see how a song with those properties would fare.
            You can also first analyse your own song, check it's properties and then tune them a bit to see how these changes would affect the results.</p>
            <Form onSubmit={this.submitAttributes}>
              <Header as="h3">
                Get review by custom attributes <Button content="submit attributes" /></Header>
              <List>
                <List.Item>
                  average_loudness:
                  <input
                    name='average_loudness'
                    type="range"
                    min={0}
                    max={1}
                    step={0.01}
                    value={customValues.average_loudness}
                    onChange={this.changeValue}
                  /> {customValues.average_loudness}
                </List.Item>
                <List.Item>
                  dissonance:
                  <input
                    name='dissonance'
                    type="range"
                    min={0}
                    max={1}
                    step={0.01}
                    value={customValues.dissonance}
                    onChange={this.changeValue}
                  /> {customValues.dissonance}
                </List.Item>
                <List.Item>
                  pitch_salience:
                  <input
                    name='pitch_salience'
                    type="range"
                    min={0}
                    max={1}
                    step={0.01}
                    value={customValues.pitch_salience}
                    onChange={this.changeValue}
                  />{customValues.pitch_salience}
                </List.Item>
                <List.Item>
                  spectral_complexity:
                  <input
                    name='spectral_complexity'
                    type="range"
                    min={0}
                    max={50}
                    step={0.1}
                    value={customValues.spectral_complexity}
                    onChange={this.changeValue}
                  /> {customValues.spectral_complexity}
                </List.Item>
                <List.Item>
                  chords_key:
                  <input
                    name='chords_key'
                    type="text"
                    value={customValues.chords_key}
                    onChange={this.changeValue}
                  />
                </List.Item>
                <List.Item>
                  tuning_frequency:
                  <input
                    name='tuning_frequency'
                    type="range"
                    min={0}
                    max={600}
                    step={1}
                    value={customValues.tuning_frequency}
                    onChange={this.changeValue}
                  /> {customValues.tuning_frequency}
                </List.Item>
                <List.Item>
                  chords_strength:
                  <input
                    name='chords_strength'
                    type="range"
                    min={0}
                    max={1}
                    step={0.01}
                    value={customValues.chords_strength}
                    onChange={this.changeValue}
                  /> {customValues.chords_strength}
                </List.Item>
                <List.Item>
                  bpm:
                  <input
                    name='bpm'
                    type="range"
                    min={0}
                    max={300}
                    step={1}
                    value={customValues.bpm}
                    onChange={this.changeValue}
                  /> {customValues.bpm}
                </List.Item>
                <List.Item>
                  danceability:
                  <input
                    name='danceability'
                    type="range"
                    min={0}
                    max={2}
                    step={0.01}
                    value={customValues.danceability}
                    onChange={this.changeValue}
                  /> {customValues.danceability}
                </List.Item>
                <List.Item>
                  beats_count:
                  <input
                    name='beats_count'
                    type="range"
                    min={0}
                    max={500}
                    step={1}
                    value={customValues.beats_count}
                    onChange={this.changeValue}
                  /> {customValues.beats_count}
                </List.Item>
                <List.Item>
                  length:
                  <input
                    name='length'
                    type="range"
                    min={0}
                    max={500}
                    step={1}
                    value={customValues.length}
                    onChange={this.changeValue}
                  /> {customValues.length}
                </List.Item>
              </List>
            </Form>
          </Segment>
        </Grid.Column>
        </Grid.Row>
        </Grid>
      </Container>
    )
  }
}

export default App

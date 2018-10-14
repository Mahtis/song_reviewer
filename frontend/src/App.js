import React, { Component } from 'react'
import axios from 'axios'
import './App.css'

class App extends Component {

  componentDidMount() {
    axios.get('http://localhost:8000/api/ping').then(res => console.log(res))
  }

  render() {
    return (
      <div>
        <h1>Music review generator</h1>
        <label htmlFor="uploader">Select a song</label>
        <input id="uploader" type="file" />
      </div>
    )
  }
}

export default App

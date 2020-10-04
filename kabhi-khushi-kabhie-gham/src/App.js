import React, { useEffect, useState } from 'react';
import Plot from 'react-plotly.js';
import './App.css';

function App() {
  const [twitterID, setTwitterID] = useState("twitter");
  const [sentimentData, setSentimentData] = useState([]);

  useEffect(() => {
    fetch(`/tweetSentiments?id=${twitterID}`).then(response =>
      response.json().then(data => {
        var dates = [];
        var posCounts = [];
        var negCounts = [];

        for (var date in data) {
          dates.push(date);
          posCounts.push(data[date][0]);
          negCounts.push(data[date][1]);
        }

        var posDataObj = {
          x: dates,
          y: posCounts,
          name: 'Positive',
          type: 'bar'
        };

        var negDataObj = {
          x: dates,
          y: negCounts,
          name: 'Negative',
          type: 'bar'
        };

        setSentimentData([posDataObj, negDataObj]);
      })
    );
  }, [twitterID])

  return (
    <div className="App">
      <form>
        <label>
          Twitter ID:
          <input type="text" name="twitterID" onChange={event => setTwitterID(event.target.value)}/>
        </label>
      </form>

      <Plot
        data={sentimentData}
        layout={ {barmode: 'group', title: 'Number of Positive and Negative Tweets by Day'} }
      />
    </div>
  );
}

export default App;

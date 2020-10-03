import React, { useEffect, useState} from 'react';
import Plot from 'react-plotly.js';
import './App.css';

function App() {
  const [sentimentData, setSentimentData] = useState([]);
  
  /*useEffect(() => {
    fetch('/tweetSentiments').then(response =>
      response.json().then(data => {
        console.log(data);
      })
    );
  }, [])*/

  useEffect(() => {
    var trace1 = {
      x: ['01-01-2020', '02-02-2020', '03-03-2020'],
      y: [3, 6, 2],
      name: 'Positive',
      type: 'bar'
    };
    
    var trace2 = {
      x: ['01-01-2020', '02-02-2020', '03-03-2020'],
      y: [2, 5, 7],
      name: 'Negative',
      type: 'bar'
    };
  
    setSentimentData([trace1, trace2]);
  }, [])

  return (
    <div className="App">
      <Plot
        data={sentimentData}
        layout={ {barmode: 'group', title: 'Number of Positive and Negative Tweets by Day'} }
      />
    </div>
  );
}

export default App;

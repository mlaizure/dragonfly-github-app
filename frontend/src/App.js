import React, { useState, useEffect } from 'react';
import './App.css';

function App() {

  const [data, setData] = useState([{}])

  useEffect(() => {
    fetch("/testing").then(
      res => res.json()
    ).then(
      data => {
        setData(data)
        console.log(data)
      }
    )
  }, [])

  return (
    <div>
     
      {(typeof data.testing === 'undefined') ? (
        <p>Loading...</p>
      ) : (
        data.testing.map((test, i) => (
          <p key={i}>{test}</p>
        ))
      )}

    </div>
  )
}

export default App;

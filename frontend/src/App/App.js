import React, { useState, useEffect } from 'react';
import './App.css';
import Header from '../Header/Header.js';
import Footer from '../Footer/Footer.js';

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
    <React.Fragment>
      <div>
        <Header />
      </div>
    
      <div>
        {(typeof data.testing === 'undefined') ? (
          <p>Loading...</p>
        ) : (
          data.testing.map((test, i) => (
            <p key={i}>{test}</p>
          ))
        )}
      </div>
      <div>
        <Footer />
      </div>
    </React.Fragment>
  )
}

export default App;

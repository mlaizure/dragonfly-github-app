import React, { useState, useEffect } from 'react';
import './App.css';
import Header from '../Header/Header.js';
import Footer from '../Footer/Footer.js';


function App() {
  
  const [imageData, setImageData] = useState('');
  useEffect(() =>{
    fetch('/chart')
      .then(response => response.blob())
      .then(image => {
        // Create a local URL of that image
        const localUrl = URL.createObjectURL(image);
        setImageData(localUrl);
      });
  }, []);

  const [data, setData] = useState([{}])

  useEffect(() => {
    fetch("/dashboard").then(
      res => res.json()
    ).then(
      data => {
        setData(data)
      }
    )
  }, [])

  console.log(JSON.parse(data))

  return (
    <React.Fragment>
      <div>
        <Header />
      </div>
    
      <div className='chart'>
        {(imageData === '') ? (
          <p>Loading...</p>
        ) : (
          <img src="/chart" alt="chart" />
        )}
      </div>

      <div className='jsonData'>
        {(JSON.stringify(data) === '[{}]') ? (
          <p>Loading...</p>
        ) : (
          <p>{JSON.stringify(data)}</p>
        )}
      </div>
     
      <div className='footer'>
        <Footer />
      </div>
    </React.Fragment>
  )
}

export default App;

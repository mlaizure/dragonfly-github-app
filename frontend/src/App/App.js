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

  console.log(JSON.stringify(imageData))

  return (
    <React.Fragment>
      <div>
        <Header />
      </div>
    
      <div>
        {(imageData === '') ? (
          <p>Loading...</p>
        ) : (
          <img src={imageData} alt="chart" />
        )}
      </div>

      <div>
        {(JSON.stringify(data) === '[{}]') ? (
          <p>Loading...</p>
        ) : (
          <p>{JSON.stringify(data)}</p>
        )}
      </div>
     
     <div>
        <Footer />
      </div>
    </React.Fragment>
  )
}

export default App;

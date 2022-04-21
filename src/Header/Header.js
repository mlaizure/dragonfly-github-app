import './Header.css';
import React, { useEffect } from 'react';
import logo from '../assets/logo.png';

function Header({data}) {

  useEffect(() => {
    const jsonse = JSON.stringify(data);
    const blob = new Blob([jsonse], {type: "application/json"});
    const url  = URL.createObjectURL(blob);
    document.getElementById('download_link').href = url;
  }, [data])

  return (
    <React.Fragment>
      <div className="Header">
        <div className="logo">
          <img src={logo} alt="Dragonfly Logo" width="60px" height="60px"></img>
        </div>
        <div className="links">
          <h1><a href="https://github.com/mlaizure/dragonfly" target="_blank" rel="noopener noreferrer">Dragonfly Local Tool</a></h1>
          <h1><a id="download_link" href="" download="dragonflyData">Download Analytics</a></h1>
        </div>
      </div>
    </React.Fragment>
  )
}

export default Header;

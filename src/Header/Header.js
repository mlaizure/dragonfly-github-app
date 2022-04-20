import './Header.css';
import React from 'react';
import logo from '../assets/logo.png';

function Header() {
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
      <script>
        var jsonse = JSON.stringify(data);
        var blob = new Blob([jsonse], {type: "application/json"});
        var url  = URL.createObjectURL(blob);
        document.getElementById('download_link').href = url;
      </script>
    </React.Fragment>
  )
}

export default Header;

import React from 'react';
import { useState, useEffect, useCallback } from 'react';
import './App.css';
import Header from '../Header/Header.js';
import Footer from '../Footer/Footer.js';
import { makeTable } from '../Table/makeTable.js';
import logo from '../assets/logo.png';

function maybeRenderData (data, jsx) {
  if (data.length === 0)
      return (<h2>No repositories found.</h2>)
  else
    return jsx
}

function maybeRenderCommits (repositoryHasNoCommits, jsx) {
  if (repositoryHasNoCommits)
    return (<h2 style={ { marginLeft: "20px" } }>No bug fix related commits found in the selected repository.</h2>)
  else
    return jsx
}

function App() {

  const [userHasInstallation, setUserHasInstallation] = useState(true)
  const [repositoryHasNoCommits, setRepositoryHasNoCommits] = useState(false)
  const [imgIsLoading, setImgIsLoading] = useState(true)
  const [selectedRepo, setSelectedRepo] = useState('')
  const [repos, setRepos] = useState([])
  const imageFinishedLoadingHandler = useCallback(() => {
    setImgIsLoading(false)
  }, [ ])

  useEffect(() => {
    const img = document.getElementById('chart')
    if (!img) return

    img.removeEventListener('load', imageFinishedLoadingHandler)
    img.addEventListener('load', imageFinishedLoadingHandler)
  }, [selectedRepo])

  useEffect(() => {
    fetch("/repos").then( res => res.json())
      .then((res) => {
        if (res.userHasNoInstallation)
          setUserHasInstallation(false)
        else {
          setRepos(res.repos)
          setSelectedRepo(res.repos[0].full_name)
        }
      })
  }, [])

  const selectedRepoData = () => {
    if (!selectedRepo)
      return null
    let repo = repos.find((repo) => repo.full_name === selectedRepo)
    return repo
  }

  useEffect(() => {
      fetch("/user-is-authenticated")
      .then(res => res.json())
      .then( ({ userIsAuthenticated, redirectUrl }) => {
        if (!userIsAuthenticated)
          window.location.replace(redirectUrl)
      })
  }, [])

  const [data, setData] = useState([{}])
  useEffect(() => {
    let repoData = selectedRepoData()
    if (!repoData)
      return
    let tableSrc = `/dashboard?owner=${encodeURIComponent(repoData.owner.login)}&repo_name=${encodeURIComponent(repoData.name)}`
    fetch(tableSrc)
      .then(res => res.json())
      .then(res => {
	if (res.userHasNoInstallation)
	  setUserHasInstallation(false)
        else if (res.repositoryHasNoCommits)
	  setRepositoryHasNoCommits(true)
	else {
          setData(res)
          setRepositoryHasNoCommits(false)
        }
      })
  }, [selectedRepo])

  const maybeRenderImgIsLoading = () => {
    if (imgIsLoading)
      return <> Loading... </>
    else
      return null
  }

  const maybeRenderImg = (imgIsLoading) => {
    let repoData = selectedRepoData()
    if (!repoData)
      return null
    let imgSrc = `/chart?owner=${encodeURIComponent(repoData.owner.login)}&repo_name=${encodeURIComponent(repoData.name)}`
    return (
        <div style={ { display: "flex", flexDirection: "column", alignItems: "center", width: "960px" } }>
	<img id='chart' src={imgSrc} style={ { display: imgIsLoading ? "none" : "inline" } }/>
	{imgIsLoading
	? null
         : <p style={ {width: "600px", fontSize: "16px", position: "relative", top: "-45px" } }><b>Each slice of the figure represents</b> <br/>&nbsp;<code style={ { margin: "5px 0", fontSize: "15px"} }>number of fixes per file / total number of fixes in repository </code><br/> where <i>fixes</i> are commit messages containing keywords such as 'bug', 'fix', or 'issue'.</p>
	}
	</div>
    )
  }

  const selectStyles = {fontSize: '20px', fontWeight: 'bold',
			padding: '2px', margin: '20px'}
  return (
    !userHasInstallation
    ?
      <div style={ { display: "flex", justifyContent: "center",
		     alignItems: "center", flexDirection: "column",
		     margin: "0 auto", width: "800px", textAlign: "center",
		     height: "100vh" } }>
        <img src={logo} alt="Dragonfly Logo" width="60px" height="60px"/>
        <a href="https://github.com/apps/dragonfly-analytics">Install Dragonfly</a>
        <p>Dragonfly is a GitHub app that provides automated bug analysis and metrics to improve code stability</p>
      <img src="https://raw.githubusercontent.com/mlaizure/dragonfly-github-app/main/src/assets/dashboard_preview.png" width="800px"/>
      </div>
    : <React.Fragment>
      { maybeRenderData(data,
        <>
          <div>
            <Header data={data}/>
          </div>
          <div>
          <select style={selectStyles} value={selectedRepo} onChange={(e) => {
            setSelectedRepo(e.target.value)
            setData([{}])
            setImgIsLoading(true)
            setRepositoryHasNoCommits(false)
          }}>
              {repos.map(repo => <option key={repo.full_name}>{repo.full_name}</option>)}
            </select>
          </div>

          { maybeRenderCommits(repositoryHasNoCommits,
            <>
              <div>
                {maybeRenderImgIsLoading()}
		{maybeRenderImg(imgIsLoading)}
              </div>

              <div>
                {(JSON.stringify(data) === '[{}]') ? (
                  <p>Loading...</p>
                ) : (
                  <div>{makeTable(data)}</div>
                  //<p>{JSON.stringify(data)}</p>
                )}
              </div>

             <div>
                <Footer />
              </div>
            </>
          )}
      </>
    )}
    </React.Fragment>
  )
}

export default App;

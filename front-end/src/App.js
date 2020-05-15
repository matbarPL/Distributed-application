import React, { Component, useState  } from 'react'
import { BrowserRouter as Router, Route } from 'react-router-dom'
import PrivateRoute from './PrivateRoute';
import { AuthContext } from "./context/auth";

import Navbar from './components/Navbar'
import Landing from './components/Landing'
import Login from './components/Login'
import Register from './components/Register'
import Profile from './components/Profile'
import Run from './components/Run'

function App(props){
  const existingTokens = localStorage.getItem("usertoken");
  const [authTokens, setAuthTokens] = useState(existingTokens);
  const setTokens = (data) => {
    localStorage.setItem("usertoken", JSON.stringify(data));
    setAuthTokens(data);
  }
  console.log(existingTokens)
  return (
    <AuthContext.Provider >
      <Router>
        <div className="App">
          <Navbar />
          <Route exact path="/" component={Landing} />
          <div className="container">
            <Route exact path="/register" component={Register} />
            <Route exact path="/login" component={Login} />
            <Route path="/profile" component={Profile} />
            <Route exact path="/run" component={Run} />
          </div>
        </div>
      </Router>
    </AuthContext.Provider>
  )
}

export default App

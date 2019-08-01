import React, {useEffect, useReducer, useState, createContext, useContext} from 'react';
import {postJSON, appReducer} from './helpers'
import {BrowserRouter as Router, Switch, Route} from 'react-router-dom'
import Users from './Users'
import Context from './Context'
import UserTweets from './UserTweets'
import Nav from './Nav'
import Predict from './Predict'
import './App.css';

function App() {
  const [state, dispatch] = useReducer(appReducer, {users: []})
  const fetchUsers = async()=>{
    const response = await fetch('/api/users');
    const data = await response.json();
    const users = data.map(user=> ({...user, loading:false}))
    dispatch({type: 'setUsers', payload: users});
  }
  useEffect(()=>{
    fetchUsers()
  },[])
  return (
    <Router>
      <Context.Provider value={dispatch}>
        <Nav/>

        <Route  path="/" exact render={
          (props)=> (
          <div className="home-content">
            <Users {...props} users={state.users}/>
            <Predict {...props} users={state.users}/>
          </div>
          )
        }/>
        <Route path="/user/:id" component={UserTweets}/>
        
      </Context.Provider>
    </Router>
    
  );
}


export default App;

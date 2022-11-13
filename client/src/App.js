import React, { createContext } from 'react';
import { Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './components/Home';
import About from './components/About';
import Contact from './components/Contact';
import Login from './components/Login';
import Registeration from './components/Registeration';
import PrevPrediction from './components/PrevPrediction';
import ErrorPage from './components/ErrorPage';
import Logout from './components/Logout';

const App = () => {

  return (
    <>
      <Navbar />

      <Route exact path="/home">
        <Home />
      </Route>

      <Route path="/about">
        <About />
      </Route>

      <Route path="/contact">
        <Contact />
      </Route>

      <Route path="/login">
        <Login />
      </Route>
      
      <Route path="/registeration">
        <Registeration />
      </Route>

      <Route path="/prevprediction">
        <PrevPrediction />
      </Route>

      <Route path = "/logout">
        <Logout />
      </Route>
    </>
  )
}

export default App
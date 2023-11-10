import { BrowserRouter, Route, Routes, useNavigate } from 'react-router-dom';
import React, { useState, useEffect } from 'react';

import Login from './pages/Login';
import Home from './pages/Home'
import RegistrationComplete from './pages/RegistrationComplete';
import Register from './pages/Register';
import CreateNewListing from './pages/CreateNewListing';


const ProtectedRoute = ({ children }) => {

  const navigate = useNavigate();
  const storedToken = localStorage.getItem('access_token');

  useEffect(() => {
    if (storedToken == null) {
      navigate('/');
    }
  }, [navigate, storedToken]);

  return children;

};

const RoutesWrapper = ({ setToken }) => {

  return (
    <Routes>
      <Route path="/" element={<Login setToken={setToken} />} />
      <Route path="/home" element={<ProtectedRoute><Home /></ProtectedRoute>} />
      <Route path="/register" element={<Register />} />
      <Route path="/registration-complete" element={<RegistrationComplete />} />
      <Route path="/create-new" element={<CreateNewListing/>}></Route>
    </Routes>
  );
  
};

const App = () => {

  // eslint-disable-next-line
  const [_, setToken] = useState(null);

  return (
    <BrowserRouter>
      <RoutesWrapper setToken={setToken} />
    </BrowserRouter>
  );
};

export default App;

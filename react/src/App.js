import { BrowserRouter, Route, Routes, useNavigate } from 'react-router-dom';
import React, { useState, useEffect } from 'react';

import Login from './pages/Login';
import Home from './pages/Home'
import RegistrationComplete from './pages/RegistrationComplete';
import Register from './pages/Register';
import CreateNewListing from './pages/CreateNewListing';
import PartThree from './pages/PartThree';

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
      <Route path="/part3" element={<PartThree></PartThree>}></Route>
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

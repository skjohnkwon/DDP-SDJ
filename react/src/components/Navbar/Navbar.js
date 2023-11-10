import React from 'react'
import axios from "axios";
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './Navbar.css';
import CheckAuthButton from '../CheckAuthButton/CheckAuthButton';

const Navbar = () => {
  
  const [username, setUsername] = useState('Unknown');

  const navigate = useNavigate();

  useEffect(() => {

    const token = localStorage.getItem('access_token');

    const storedUserData = localStorage.getItem('user_data');

    if (storedUserData) {

        const userData = JSON.parse(storedUserData);

        setUsername(userData.username);

    }

    axios.get('http://127.0.0.1:8000/get-account-data/', {

        headers: {

          'Authorization': `Bearer ${token}`
        }

      })
      .then(response => {
        
      // If request is successful, populate state
        if (response.status === 200) {

          console.log("response data:", response.data);

          setUsername(response.data.username);

        }
      })

  }, []);

  const sign_out = () => {

    localStorage.removeItem("user_data");
    localStorage.removeItem("access_token");
    navigate('/');

  };

  const create_listing = () => {
    navigate('/create-new');
  }

  return (
    <nav class="nav">
        <a href = "/home" className="nav-element">DSJ-DDP p2</a>
        <h2>Signed in as {username}</h2>
        <ul>
          
          <CheckAuthButton/>
          <button onClick={create_listing} className="create-listing">Create New Item</button>
          <button onClick={sign_out} className='signout'>Sign Out</button>
        </ul>
    </nav>
  )
}

export default Navbar

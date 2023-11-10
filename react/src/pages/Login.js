import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from 'react-router-dom';

import '../styles/Shared.css';

const Login = () => {

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState(null);
    const navigate = useNavigate();
  
    const login = async (event) => {

        event.preventDefault(); // Prevent default form submission

        try {
            axios.post('http://127.0.0.1:8000/login/', {
                username,
                password,
            })
            .then(response => {
                const { access, refresh, user } = response.data;
                localStorage.setItem('access_token', access);
                localStorage.setItem('refresh_token', refresh);
                localStorage.setItem('user_data', JSON.stringify(user));  
                navigate('/home');
            })
            .catch((error) => {
                console.error("There was an error!", error);
                if(error.response.status === 401) {
                    setError("Invalid credentials");
                }
            });
        } catch (error) {
            setError("Login failed");
            console.log("login error", error);
        }
    }
  
    const go_to_register = () => { navigate('./register') }

    return (
      <div className="shared">
          {error && <label className='error'>{error}</label>}
          <form onSubmit={login}>
              <div className='input-div'>
                  <label className='input-label'>Username</label>
                  <input
                      className='input-field'
                      type="text"
                      placeholder="Username"
                      onChange={e => setUsername(e.target.value)}
                      autoComplete="username" // Added autocomplete for username
                  />
              </div>
              <div className='input-div'>
                  <label className='input-label'>Password</label>
                  <input
                      className='input-field'
                      type="password"
                      placeholder="Password"
                      onChange={e => setPassword(e.target.value)}
                      autoComplete="current-password" // Added autocomplete for password
                  />
              </div>
          </form>
          <button type="submit" onClick={login}>Login</button>
          <button onClick={go_to_register}>Register</button>
      </div>
  );
}

export default Login;

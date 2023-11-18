import React, { useState } from 'react';
import axios from 'axios';

import './CheckAuthButton.css';

const CheckAuthButton = () => {
  // eslint-disable-next-line
  const [_, setResult] = useState('');
  const [buttonColor, setButtonColor] = useState('default');

  const check_auth = async () => {
    const token = localStorage.getItem('access_token');
    console.log("This is the localStorage token: ", token);

    try {

      const response = await axios.get('http://localhost:8000/check-auth/', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.status === 200) {
        console.log("This is the response: ", response.data.message);
        console.log("username: ", response.data.username)
        console.log("user_id:", response.data.user_id)
        console.log("email: ", response.data.email)
        setResult(`response.data: ${response.data.message}`);
        setButtonColor('green');
        setTimeout(() => {
          setButtonColor('');
        }, 3000);
      } else {
        setResult('Something went wrong');
        setButtonColor('red');
        setTimeout(() => {
          setButtonColor('');
        }, 3000);
      }

    } catch (error) {
      console.log("Authentication failed", error);
      setResult('Authentication failed');
      setButtonColor('red');
      setTimeout(() => {
        setButtonColor('');
      }, 3000);
    }
  };

  return (
    <div>
      <button className="check-auth-button"
        onClick={check_auth} 
        style={{ backgroundColor: buttonColor }}
      >
        Check Auth
      </button>
    </div>
  );
};

export default CheckAuthButton;

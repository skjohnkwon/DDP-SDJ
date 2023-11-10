import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import { useEffect } from 'react';

import '../styles/Shared.css';
import '../styles/Register.css';

const Register = () => {

  const [username, setUsername] = useState('');
  const [first_name, setFirstName] = useState('');
  const [last_name, setLastName] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [usernameValid, setUsernameValid] = useState(true);
  const [emailValid, setEmailValid] = useState(true);
  const [passwordValid, setPasswordValid] = useState(true);
  const [confirmPasswordValid, setConfirmPasswordValid] = useState(true);
  const navigate = useNavigate();

  const signup = async () => {

      if (!checkUsername()) {
        if (username.length < 3) {
          setErrorMessage('Username is too short! 3 char minimum');
        } else {
          setErrorMessage('Username is too long! 25 char maximum');
        }

      } else if(!checkUsername() && (username.length > 25)) {

        setErrorMessage('Username is too short! 3 char minimum')
      
      } else if(!checkEmail()) {

        setErrorMessage('Please enter a valid email')
      
      } else if(!passwordValid) {

        setErrorMessage('Password must include number and must be a reasonable length')
      
      } else if(!confirmPasswordValid) {

        setErrorMessage( 'Passwords do not match!')
      
      } else {

        try {
          console.log('Password before sending:', password);

          const response = await axios.post('http://127.0.0.1:8000/register/', {
            username,
            email,
            password,
            first_name,
            last_name,
          });

          if (response.status === 201) {
            console.log('User registered in:', response.data);
            localStorage.setItem("reg_token", response.data.reg_token);
            console.log("reg_token:", response.data.reg_token);
            redirect()
          }

        } catch (error) {

          //console.log('Error during registration!', error);

          if (error.response && error.response.data) {

            //console.log('Server responded with:', error.response.data);

            const serverError = error.response.data.error;
        
            if (serverError === 'Username is already taken') {

              //console.log('Username is already taken');

              setErrorMessage('Username is already taken');

              setTimeout(() => {
                setErrorMessage('');
              }, 5000);

            } else if (serverError === 'Email is already taken') {
              setErrorMessage('Email is already taken');

              setTimeout(() => {
                setErrorMessage('');
              }, 5000);

            } else {
              setErrorMessage('Something went wrong :/');

              setTimeout(() => {
                setErrorMessage('');
              }, 5000);
            }
          }
        }

      } 
  };
      
  const redirect = () => {
        navigate('/registration-complete');
  }

  function checkUsername() {
    if(username.length > 25 || username.length < 3) {
      setUsernameValid(false);
      return false;
    }
    setUsernameValid(true);  // Reset to true when valid
    return true;
  }
  
  function checkPassword() {
    const hasNumber = /\d/;
    if(password.length < 8 || password.length > 25 || !hasNumber.test(password)) {
      // console.log("password:", password)
      // console.log("Password is invalid");
      setPasswordValid(false);
      return false;
    }
    // console.log("password:", password)
    // console.log("Password is valid");
    setPasswordValid(true);  // Reset to true when valid
    return true;
  }
  
  function checkEmail() {
    if(!(email.includes("@") && email.includes("."))) {
      setEmailValid(false);
      return false;
    }
    setEmailValid(true);  // Reset to true when valid
    return true;
  }

  useEffect(() => {
    const checkConfirmPassword = () => {
      if (!(password === confirmPassword)) {
        setConfirmPasswordValid(false);
        return false;
      }
      setConfirmPasswordValid(true);  // Reset to true when valid
      return true;
    };
  
    checkConfirmPassword();
  }, [password, confirmPassword]);

  useEffect(() => {
    checkPassword();
  }, [password]);
  

  return (
    <div className="shared">
      {errorMessage && <label className='error'>{errorMessage}</label>}
      

        <div className='input-div'>
          <label className='input-label'>Username</label>
          <input className={`input-field ${usernameValid ? '' : 'red-input'}`}
              type="text"
              placeholder="Username"
              onChange={e => { setUsername(e.target.value); checkUsername(); }}
          />
        </div>

        <div className='input-div'>

            <label className='input-label'>First Name</label>
            <input 
            
              className='input-field'
              type = "text"
              placeholder="First Name"
              onChange={e => { setFirstName(e.target.value);}}

            />

        </div>

        <div className='input-div'>

            <label className='input-label'>Last Name</label>
            <input 
              
              className='input-field'
              type = "text"
              placeholder="Last Name"
              onChange={e => { setLastName(e.target.value);}}

            />

        </div>

        <div className='input-div'>

            <label className='input-label'>E-Mail</label>
            <input className={`input-field ${emailValid ? '' : 'red-input'}`}
                type="text"
                placeholder="E-Mail"
                onChange={e => { setEmail(e.target.value); checkEmail(); }}
                autoComplete='email'
            />

        </div>

        <div className='input-div'>
        
          <label className='input-label'>Password</label>
          <input

              className='input-field'
              type = "password"
              placeholder="Password"
              autoComplete="new-password" // added this
              onChange={e => {setPassword(e.target.value);}}
          />

        </div>

        <div className='input-div'>
        
          <label className='input-label'>Confirm Password</label>
          <input 

              className='input-field'
              type = "password"
              placeholder="Confirm Password"
              autoComplete="new-password" // added this
              onChange={e => {setConfirmPassword(e.target.value);}}
          />

        </div>

        <button type="submit" onClick={signup}>Register</button>
        <button type="button" onClick={redirect}>Go Back</button>

    </div>
  );
}

export default Register

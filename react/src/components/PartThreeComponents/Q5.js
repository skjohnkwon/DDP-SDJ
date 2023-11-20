import React, {useState, useEffect } from 'react'
import '../../styles/PartThreeQuestions.css'
import axios from 'axios';

const Q5 = () => {

  const [answers, setAnswers] = useState([]);

  const [userX, setUserX] = useState('');
  const [userY, setUserY] = useState('');

  const [userList, setUserList] = useState([]);

  const get_user_list = async () => {
    
      const response = await axios.get('http://localhost:8000/part3/send-list-of-users-excluding-admin-and-current-user/');
  
      if (response.status === 200) {

        console.log(response.data);
        return response.data;
      }
  }

  useEffect(() => {
    get_user_list().then(data => setUserList(data['users']));
  }, []);

  const getAnswers = async () => {
    const url = `http://127.0.0.1:8000/part3/q5/`;

    try {
      const response = await axios.get(url, {
          params: {
              userX: userX,
              userY: userY
          }
      });
      
      if (response.status === 200) {
        console.log('Answers retrieved!', response.data['answer']);
      }
      
      setAnswers(response.data['answer']);

    } catch (error) {
      console.error('Error: ', error);
    }
  };


  return (
    <div className='question-interface-div'>
      <h2>QUESTION 5: List the other users who are favorited by both users X, and Y. Usernames X and Y will be selected from dropdown menus by the instructor.</h2>

      <div className='dropdown-div'>
          <select
              name="userX"
              className="user-list"
              onChange={e => {
                  console.log("Setting userX to:", e.target.value);
                  setUserX(e.target.value);
              }}
          >
              <option value="">Select User X</option>
              {userList.map(user => (
                  <option key={user[0]} value={user[1]}>{`${user[0]} (${user[1]})`}</option>
              ))}
          </select>
          
          <select
              name="userY"
              className="user-list"
              onChange={e => {
                  console.log("Setting userY to:", e.target.value);
                  setUserY(e.target.value);
              }}
          >
              <option value="">Select User Y</option>
              {userList.map(user => (
                  <option key={user[0]} value={user[1]}>{`${user[0]} (${user[1]})`}</option>
              ))}
          </select>
      </div>

      <button onClick={getAnswers} className='answer-button'>Answers</button>

      <div className='main-body'>
          {answers && answers.map((user, index) => (
            <div key={index} className='answer-div'>
              <p>User: {user}</p>
            </div>
          ))}
      </div>
    </div>
  )
}

export default Q5

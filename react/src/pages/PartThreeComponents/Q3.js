import React, {useState,useEffect} from 'react'
import '../../styles/PartThree.css'
import axios from 'axios'

const Q3 = () => {

  const [answers, setAnswers] = useState([]);

  const [user, setUser] = useState('');

  const [userList, setUserList] = useState([]);

  const get_user_list = async () => {

    const token = localStorage.getItem('access_token');
    
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
    const url = `http://127.0.0.1:8000/part3/q3/`;

    try {
      const response = await axios.get(url, {
          params: {
              user: user
          }
      });
      
      if (response.status === 200) {
        console.log('Answers retrieved!', response.data['answer']);
      }
      
      setAnswers(response.data['answer']); // Update the state with the answers

    } catch (error) {
      console.error('Error: ', error);
    }
  };


  return (
    <div className='question-interface-div'>

      <h2>QUESTION 3: List all the items posted by user X, such that all the comments are "Excellent" or "good" for these items. User X is arbitrary and will be determined by the instructor. </h2>

      <div className='dropdown-div'>
          <select
              name="user"
              className="user-list"
              onChange={e => {
                  console.log("Setting user to:", e.target.value);
                  setUser(e.target.value);
              }}
          >
              <option value="">Select User </option>
              {userList.map(user => (
                  <option key={user[0]} value={user[1]}>{`${user[0]} (${user[1]})`}</option>
              ))}
          </select>
          
      </div>

      <button onClick={getAnswers} className='answer-button'>Answers</button>

      <div className='main-body'>
        {answers.map((answer, index) => (
          <div key={index} className='answer-div'>
            <p>Item ID: {answer.item_id} - Title: {answer.title}</p>
            {answer.comments.map((comment, commentIndex) => (
              <div key={commentIndex}>
                <p>     Comment: {comment[0]} (Rating: {comment[1]})</p>
              </div>
            ))}
          </div>
        ))}
      </div>
    </div>
  )
}

export default Q3

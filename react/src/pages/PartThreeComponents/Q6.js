import React, { useState } from 'react';
import '../../styles/PartThreeQuestions.css';
import axios from 'axios';

const Q6 = () => {

  const [answers, setAnswers] = useState([]);

  const getAnswers = async () => {
    const url = `http://127.0.0.1:8000/part3/q6/`;

    try {
      const response = await axios.get(url);
      
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
      <h2>QUESTION 6: Display all the users who never posted any "excellent" items: an item is excellent if at least three reviews are excellent.</h2>
      <button onClick={getAnswers} className='answer-button'>Answers</button>
      <div className='main-body'>
        {answers && answers.map((user, index) => (
          <div key={index} className='answer-div'>
            <p>{user}</p>
          </div>
        ))}
      </div>
    </div>
  )
}

export default Q6

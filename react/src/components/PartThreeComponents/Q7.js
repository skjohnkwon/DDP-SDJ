import React, { useState } from 'react';
import '../../styles/PartThreeQuestions.css';
import axios from 'axios';

const Q7 = () => {

  const [answers, setAnswers] = useState([]);

  const getAnswers = async () => {
    const url = `http://127.0.0.1:8000/part3/q7/`;

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
      <h2>QUESTION 7: Display all the users who never posted a "poor" review.</h2>
      <button onClick={getAnswers} className='answer-button'>Answers</button>
      <div className='main-body'>
        {answers.map((answer, index) => (
          <div key={index} className='answer-div'>
            <p>User: {answer}</p>
          </div>
        ))}
      </div>
    </div>
  )
}

export default Q7

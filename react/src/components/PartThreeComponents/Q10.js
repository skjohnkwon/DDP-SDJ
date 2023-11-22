import React, { useState } from 'react';
import '../../styles/PartThreeQuestions.css';
import axios from 'axios';

const Q10 = () => {

  const [answers, setAnswers] = useState([]);

  const getAnswers = async () => {
    const url = `http://127.0.0.1:8000/part3/q10/`;

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
      <h2>QUESTION 10: List a user pair (A, B) such that they always gave each other "excellent" reviews for every single item they posted.</h2>
      <button onClick={getAnswers} className='answer-button'>Answers</button>
      <div className='main-body'>
        {answers && answers.map((pair, index) => (
          <div key={index} className='answer-div'>
            <p>User Pair: {pair[0]} and {pair[1]}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Q10;

import React, { useState } from 'react';
import '../../styles/PartThreeQuestions.css';
import axios from 'axios';

const Q8 = () => {

  const [answers, setAnswers] = useState([]);

  const getAnswers = async () => {
    const url = `http://127.0.0.1:8000/part3/q8/`;

    try {
      const response = await axios.get(url);
      
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
      <h2>QUESTION 8: Display all the users who posted some reviews, but each of them is "poor"</h2>
      <button onClick={getAnswers} className='answer-button'>Answers</button>
      <div className='main-body'>
        {answers && answers.map((user, index) => (
          <div key={index} className='answer-div'>
            <p>{user} only posted poor reviews.</p>
          </div>
        ))}
      </div>
    </div>
  )
}

export default Q8

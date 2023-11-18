import React, {useState} from 'react'
import '../../styles/PartThree.css'
import axios from 'axios'

const Q1 = () => {

  const [answers, setAnswers] = useState([]);

    const getAnswers = async () => {
      const url = `http://127.0.0.1:8000/part3/q1/`;

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
      <h2>QUESTION 1: List the most expensive items in each category.</h2>
      <button onClick={getAnswers} className='answer-button'>Answers</button>
      <div className='main-body'>
      {answers && answers.map((answer, index) => (
        <div key={index} className='answer-div'>
          <p>Category: {answer.category}, Max Price: {answer.max_price}</p>
        </div>
      ))}
      </div>
    </div>
  )
}

export default Q1

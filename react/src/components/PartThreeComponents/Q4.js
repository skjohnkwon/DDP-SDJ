import React, {useState} from 'react'
import '../../styles/PartThree.css'
import axios from 'axios'

const Q4 = () => {

  const [answers, setAnswers] = useState([]);

    const getAnswers = async () => {
      const url = `http://127.0.0.1:8000/part3/q4/`;

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
      <h2>QUESTION 4: List the users who posted the most number of items on a specific date like 5/1/2023; if there is a tie, list all the users who have a tie. The specific date can be hard coded into your SQL select query or given by the user. </h2>
      <button onClick={getAnswers} className='answer-button'>Answers</button>
      <div className='main-body'>
        {answers.map((answer, index) => (
          <div key={index} className='answer-div'>
            <p>{answer[0]} with {answer[1]} items</p>
          </div>
        ))}
      </div>
    </div>
  )
}

export default Q4

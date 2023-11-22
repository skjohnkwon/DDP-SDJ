import React, {useState} from 'react'
import '../../styles/PartThree.css'
import axios from 'axios'

const Q2 = () => {

  const [answers, setAnswers] = useState([]);
  const [categoryX, setCategoryX] = useState('');
  const [categoryY, setCategoryY] = useState('');

  const getAnswers = async () => {
    const url = `http://127.0.0.1:8000/part3/q2/`;

    try {
      const response = await axios.get(url, {
          params: {
              categoryX: categoryX,
              categoryY: categoryY
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
      <h2>QUESTION 2: List the users who posted at least two items that were posted on the same day, one has a category of X, and another has a category of Y.</h2>
      
      <div className='category-input-div'>
      <div className='input-div'>

        <input className='input-field'

        type = "text"
        placeholder="Category X"
        onChange={e => { setCategoryX(e.target.value); }}


        />

        </div>

        <div className='input-div'>

        <input className='input-field'

        type = "text"
        placeholder="Category Y"
        onChange={e => { setCategoryY(e.target.value); }}

        />

        </div>
      </div>

      <button onClick={getAnswers} className='answer-button'>Answers</button>

      <div className='main-body'>
        {answers && answers.map((answer, index) => (
          <div key={index} className='answer-div'>
            <p>{answer}</p>
          </div>
        ))}
      </div>
    </div>
  )
}

export default Q2

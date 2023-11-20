import React, { useState } from 'react';
import Navbar from '../components/Navbar/Navbar';
import '../styles/PartThree.css';
import Q1 from '../components/PartThreeComponents/Q1'
import Q2 from '../components/PartThreeComponents/Q2'
import Q3 from '../components/PartThreeComponents/Q3'
import Q4 from '../components/PartThreeComponents/Q4'
import Q5 from '../components/PartThreeComponents/Q5'
import Q6 from '../components/PartThreeComponents/Q6'
import Q7 from '../components/PartThreeComponents/Q7'
import Q8 from '../components/PartThreeComponents/Q8'
import Q9 from '../components/PartThreeComponents/Q9'
import Q10 from '../components/PartThreeComponents/Q10'
import axios from 'axios';

const PartThree = () => {
    const [currentComponentKey, setCurrentComponentKey] = useState(null);
    const [selectedButton, setSelectedButton] = useState(null);

    const componentMap = {
        q1: <Q1 />,
        q2: <Q2 />,
        q3: <Q3 />,
        q4: <Q4 />,
        q5: <Q5 />,
        q6: <Q6 />,
        q7: <Q7 />,
        q8: <Q8 />,
        q9: <Q9 />,
        q10: <Q10 />
    };

    const init_db = async () => {
        console.log('Initializing database...');
        try {
            const response = await axios.post('http://127.0.0.1:8000/init-db/');
            if (response.status === 201) {
                console.log(response.data);
            }
        } catch (error) {
            console.log('Error during database initialization!', error);
        }
    }
    
    const setComponent = (key, q) => {

        if (key === selectedButton) {
            setCurrentComponentKey(null);
            setSelectedButton(null);
        } else {
            setCurrentComponentKey(key);
            setSelectedButton(key);
        }
        console.log(key, q);
    }

    const getButtonClass = (key) => {
        return key === selectedButton ? 'selected-button' : '';
    }

    const navigate = () => {
        window.location.href = '/home';
    }

    return (
        <div className='partthree-div'>
            <Navbar />
            <div className='partthree-div-body'>
                <h1> Part Three Questions </h1>
                <div className='button-div'>
                    {['q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10'].map((key, index) => (
                        <button 
                            key={key}
                            className={getButtonClass(key)}
                            onClick={() => setComponent(key, `Query ${index + 1}`)}
                        >
                            {index + 1}
                        </button>
                    ))}
                </div>
                <div className='current-component'>
                    {componentMap[currentComponentKey]}
                </div>
            </div>
            <div className='button-div'>
                <button className='back-button' onClick={navigate}>Back</button>
                <button className='init-db-bttn' onClick={init_db}>Initialize Database</button>
            </div>
        </div>
    );
}

export default PartThree;

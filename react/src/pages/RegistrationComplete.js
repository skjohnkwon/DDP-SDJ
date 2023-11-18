import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const RegistrationComplete = () => {

  const navigate = useNavigate();

  useEffect(() => {
    
    const registrationStatus = localStorage.getItem('reg_token');

    if (registrationStatus === null) {

      navigate('/');

    }
    
  }, [navigate]);

  const back = () => {

    localStorage.removeItem('reg_token');
    
    navigate('/');

  };

  return (
    <div>
      <div id='container'>
        <label>registration complete</label>
        <button onClick={back}>Go Back</button>  {/* Fixed this line */}
      </div>
    </div>
  );
};

export default RegistrationComplete;

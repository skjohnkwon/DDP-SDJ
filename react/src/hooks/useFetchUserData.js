import { useState, useEffect } from 'react';
import axios from 'axios';

const useFetchUserData = (url) => {  

  const [userData, setUserData] = useState({
    username: '',
    email: '',
    first_name: '',
    last_name: '',
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null); 

  useEffect(() => {
    setIsLoading(true); 
    try {
      const token = localStorage.getItem('access_token');

      axios.get(url, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      .then(response => {
        if (response.status === 200) {
          setUserData({
            username: response.data.username,
            email: response.data.email,
            first_name: response.data.first_name,
            last_name: response.data.last_name,
          });
        }
        setIsLoading(false);
      })
      .catch(err => {
        setError(err);
        setIsLoading(false);
      });
    } catch (err) {
      setError(err);
      setIsLoading(false);
      console.error("There was an error fetching user details:", err);
    };
  }, [url]);

  return [userData, error];
};
export default useFetchUserData;

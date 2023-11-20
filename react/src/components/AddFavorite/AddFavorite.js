import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './AddFavorite.css';

const AddFavorite = () => {

    const [userList, setUserList] = useState([]);
    const [fav_user, setFavUser] = useState('');

    const get_user_list = async () => {

      const token = localStorage.getItem('access_token');
      
        const response = await axios.get('http://localhost:8000/part3/send-list-of-users-excluding-admin-and-current-user/', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
    
        if (response.status === 200) {
          console.log('Added Favorite!');
          console.log(response.data);
          return response.data;
        }
    }

    useEffect(() => {
      get_user_list().then(data => setUserList(data['users']));
    }, []);

    const add_favorite = async () => {

        const token = localStorage.getItem('access_token');
        const userdata = JSON.parse(localStorage.getItem('user_data'));
    
        try {
          const response = await axios.post('http://127.0.0.1:8000/part3/add-favorite/', {
            user: userdata.id,
            fav_user: fav_user,
          }, {
            headers: {
              Authorization: `Bearer ${token}`,
            }
          });
    
          if (response.status === 201) {
            console.log('Added Favorite!');
            console.log(response.data);
          }
        } catch (error) {
          console.log('Error during comment creation!', error);
        }
    }

  return (
    <div className='add-fav-div'>

      <h2>Add Favorite User</h2>

      <select
          name="user"
          className="user-list"
          onChange={e => {
              console.log("Setting user to:", e.target.value);
              setFavUser(e.target.value);
          }}
      >
          <option value="">Select User</option>
          {userList.map(user => (
              <option key={user[0]} value={user[1]}>{`${user[0]} (${user[1]})`}</option>
          ))}
      </select>

      <button className='add-fav-submit' onClick={add_favorite}>submit</button>
    </div>
  )
}

export default AddFavorite

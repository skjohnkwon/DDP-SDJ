import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import Navbar from '../components/Navbar/Navbar'

import '../styles/CreateNewListing.css'

const CreateNewListing = () => {

    const [title, setTitle] = useState('');
    const [description, setDescription] = useState('');
    const [price, setPrice] = useState('');
    const [category, setCategory] = useState('');
    const navigate = useNavigate();
    const [message, setMessage] = useState('');

    const create = async () => {

        var categories = category.split(',');

        const userdata = JSON.parse(localStorage.getItem('user_data'));
        
        console.log("userdata" + userdata);

        const token = localStorage.getItem('access_token');

        console.log("title: " + title);
        console.log("description: " + description);
        console.log("price: " + price);
        console.log("categories: " + categories);
        console.log("user: " + userdata.id);

        try {
            const response = await axios.post('http://127.0.0.1:8000/create-item/', {
                title,
                description,
                price,
                categories,
                user: userdata.id,
            }, {
                headers: {
                    Authorization: `Bearer ${token}`,  // Replace 'token' with your actual token variable
                }
            });
            
            if (response.status === 201) {
                console.log('Item created:', response.data);
                setMessage('Item created!');
                setTimeout(() => {
                    setMessage('');
                }, 3000);

                // Reset the fields
                setTitle('');
                setDescription('');
                setPrice('');
                setCategory('');
            }
        } catch (error) {
            console.log('Error during item creation!', error);

        }
    }

    const redirect = () => {
        navigate('/home');
    }

  return (
    
    <div className='container'>
        <Navbar></Navbar>
        <h1>Create a new listing:</h1>
        <div className='item-form'>
            <div className='input-div'>

                <label className='input-label'>Title</label>
                <input className='input-field'

                type = "text"
                placeholder="i.e. Smartphone"
                onChange={e => { setTitle(e.target.value); }}


                />

            </div>

            <div className='input-div'>

                <label className='input-label'>Description</label>
                <textarea className='input-field'

                type = "text"
                placeholder="i.e. This is the new iPhone 15 Pro Max"
                onChange={e => { setDescription(e.target.value); }}

                />

            </div>

            <div className='input-div'>

                <label className='input-label'>Categories</label>
                <textarea className='input-field'

                type = "text"
                placeholder="seperated by commas i.e. Electronics, Phones, Apple"
                onChange={e => { setCategory(e.target.value); }}

                />

            </div>

            <div className='input-div'>

                <label className='input-label'>Price</label>
                <input className='input-field'

                type = "text"
                placeholder="i.e. 1000"
                onChange={e => { setPrice(e.target.value); }}

                />

            </div>
            <div className='button-div'>
                <button onClick={create}>Submit</button>
                <button onClick={redirect}>Go Back</button>
                {/* <button onClick={test}>test</button> */}
            </div>
            
        </div>

        <label>{message}</label>
    </div>
  )
}

export default CreateNewListing
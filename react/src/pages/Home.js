
import React from 'react';
import Search from "../components/Search/Search";
import Navbar from '../components/Navbar/Navbar';

import '../styles/Home.css';

const Home = () => {


  return (
  
    <div className = "home">
      <Navbar/>
      <Search/>
    </div>
  )
}

export default Home;

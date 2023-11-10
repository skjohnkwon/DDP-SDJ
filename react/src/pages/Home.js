
import React from 'react';
import Navbar from "../components/Navbar/Navbar";
import Search from "../components/Search/Search";

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

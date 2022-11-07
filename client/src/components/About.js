import React,{useEffect, useState} from 'react'
import {useHistory} from "react-router-dom";

const About = () => {

  const history = useHistory();
  const [userData, setUserData] = useState();

  const callAboutPage = async () => {
    try{
      const res = await fetch("/about", {
        method : "GET",
        headers : {
          Accept : "application/json",
          "Content-Type" : "application/json"
        },
        credentials : "include"
      });

      const data = await res.json();
      setUserData(data);

      if(!res.status === 200){
        const error = new Error(res.error);
        throw error;
      }

    }catch(err){
      history.push("/login");
    }
  }

  useEffect(() => {
    callAboutPage();
  }, []);

  return (
    <>
      <div className='row mt-4'>
        <div className='col-md-1'>
          <label>Name</label>
        </div>
        <div className='col-md-6'>
          <label>Harsh Gupta</label>
        </div>
      </div>

      <div className='row mt-4'>
        <div className='col-md-1'>
          <label>UserName</label>
        </div>
        <div className='col-md-6'>
          <label>Harsh Gupta</label>
        </div>
      </div>

      <div className='row mt-4'>
        <div className='col-md-1'>
          <label>Phone No</label>
        </div>
        <div className='col-md-6'>
          <label>Harsh Gupta</label>
        </div>
      </div>

      <div className='row mt-4'>
        <div className='col-md-1'>
          <label>Email</label>
        </div>
        <div className='col-md-6'>
          <label>Harsh Gupta</label>
        </div>
      </div>

      <div className='row mt-4'>
        <div className='col-md-1'>
          <label>Password</label>
        </div>
        <div className='col-md-6'>
          <label>Harsh Gupta</label>
        </div>
      </div>
    </>
  )
}

export default About
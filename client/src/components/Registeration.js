import React, {useState} from 'react'
import { NavLink , useHistory} from 'react-router-dom'
import "./Registeration.css"

const Registeration = () => {

  const history = useHistory();

  const [user, setUser] = useState({
      name : "", username : "", phoneno : "", email : "", password : ""
  });

  let name, value;

  const handleInputs = (e) => {
      name = e.target.name;
      value = e.target.value;
      setUser({...user, [name] : value});
  }

  const PostData = async (e) => {
    e.preventDefault();
    const {name, username, phoneno, email, password} = user;
    const res = await fetch("/register", {
      method : "post",
      headers : {
        "Content-Type" : "application/json"
      },
      body : JSON.stringify({
        name, username, phoneno, email, password
      })
    });
    
    const data = await res.json();

    if(data.status === 500 || !data){
      window.alert("Invalid Registeration");
      console.log("Invalid Registeration");
    }else{
      window.alert("Registeration successful");
      console.log("Registeration successful");
      history.push("/login");
    }

  }

  return (
    <div>
      <div className = "outer-form-div-register">
        <form>
          <div>
            <input type = "text" name = "name" id = "Name-register" autoComplete = "on" placeholder='Name'
            value = {user.name} onChange = {handleInputs}/>
          </div>
          <div>
            <input type = "text" name = "username" id = "UserName-register" autoComplete = "on" placeholder='UserName'
            value = {user.username} onChange = {handleInputs}/>
          </div>
          <div>
            <input type = "number" name = "phoneno" id = "PhoneNo-register" autoComplete = "on" placeholder='PhoneNo'
            value = {user.phoneno} onChange = {handleInputs}/>
          </div>
          <div>
            <input type = "email" name = "email" id = "Email-register" autoComplete = "on" placeholder='Email'
            value = {user.email} onChange = {handleInputs}/>
          </div>
          <div>
            <input type = "password" name = "password" id = "Password-register" autoComplete = "on" placeholder='Password'
            value = {user.password} onChange = {handleInputs}/>
          </div>
          <div className='evaluate-button'>
            <input type = "submit" name = "register" id = "register-register" 
            value = "Register" onClick={PostData}/>
            <br/>
          </div>
        </form>
      </div>
    </div>
  )
}

export default Registeration
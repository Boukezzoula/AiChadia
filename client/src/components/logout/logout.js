import Login from "../login/Login";
import {json, useNavigate} from 'react-router-dom';
import React,{useEffect} from 'react'
import { getAuthToken } from '../../util/auth';

export default function Logout() {
    const navigate = useNavigate();
    const token = getAuthToken();
    useEffect(() => {
          logoutquery();
          
    
      }, []);
    async function logoutquery(){
        console.log(token)
        //const response = await fetch('https://mocking-bird-rest-api.onrender.com/logout', {
        const response = await fetch('http://127.0.0.1:5000/logout', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' , 'Authorization': 'Bearer '+token},
          })

        if (response.status === 401 || response.status === 422){
            return response.text;
        }
        if (!response.ok){
            throw json({message: 'could not logout user'},{status: 500});
        }
        console.log("logout succesfully");
        navigate("/login",{replace: true});
        
  
    };

    return <Login/>
    
  };
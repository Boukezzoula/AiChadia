import { Grid, Typography } from "@mui/material";
import Header from "../Header/Header";
import Box from '@mui/joy/Box';
import logo from '../../resources/logo.jpg'
export default function UserDash(){

return(
    
    <div >
        <Header/>
        <h1 style={{ display: 'flex', justifyContent:'center'}}>Welcome To Mockingbird Platform</h1>

    <Grid style={{
      width: '100%',
      textAlign: 'center',
      borderRadius: '5px',
      marginTop: '10px',
      display: 'flex',
    justifyContent: 'center'
    }}>
    <div style={{
        display: 'flex',
        justifyContent: 'center',
      }}>
      <img
       src={logo} alt="cur" 
       style={{
        width:'50%'
       }}
          
      />
      </div>
    </Grid>
     
      

    <Box>
    <br></br>
        <Typography level="h2" style={{ display: 'flex', justifyContent:'center'}}>Here is what you can do in our platform ? </Typography>
        <ul style={{display:'block',textAlign:'center',justifyContent:'center',alignContent:'center',padding: 0}}>
            <li><Typography>1- extract audio file from youtube link</Typography></li>
            <li><Typography>2- translate any mp3 audio file</Typography> </li>
            <li><Typography>3- transcribe any mp3 audio file </Typography></li>
            <li><Typography>4- generate transcript audio file</Typography> </li>
            <li><Typography>5- generate english voice over based on ai </Typography> </li>
        </ul>
    </Box>
        
    </div>
)


}
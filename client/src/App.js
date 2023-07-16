import React from 'react'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import Login from './components/login/Login'
import Signup from './components/singup/Signup'
import UserDash from './components/authComponents/UserDash'
import ErrorPage from './constants/Error'
import { tokenLoader} from './util/auth'
import Translate from './components/translate/Translate'
import Transcribe from './components/transcribe/Transcribe'
import Logout from './components/logout/logout'

const router = createBrowserRouter([
  {path:'/',
   element: <Login/>,
   errorElement: <ErrorPage/>,
   id: 'root',
   loader: tokenLoader
  },
  {path:'/login', element: <Login/>},
  {path:'/signup', element: <Signup/> },
  {path:'/dashboard', element: <UserDash/>},
  { path:'translate', element: <Translate/>},
  { path:'transcribe', element: <Transcribe/>},
  {path:'logout', element: <Logout/>}
  
  
])


const App = () => {
  return (
    <RouterProvider router={router}/>
  )
}

export default App
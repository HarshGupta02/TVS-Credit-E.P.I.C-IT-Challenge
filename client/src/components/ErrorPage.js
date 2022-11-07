import React from 'react'
import { NavLink } from 'react-router-dom'

const ErrorPage = () => {
  return (
    <div>
        <div className = "error-page">
            <p>Error 404</p>
            <NavLink to = "/">Back To the Home Page</NavLink>
        </div>
    </div>
  )
}

export default ErrorPage
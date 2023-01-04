import { useState, createContext } from 'react';


// Nav enum for navigation metadata
export const Nav = {
    HOME: {
      order: 1,
      name: 'Home',
      display_realm: true,
      display_profession: false
    },
    PROFESSION: {
      order: 2, 
      name: 'Profession',
      display_realm: true,
      display_profession: true
    },
    ABOUT: {
      order: 3,
      name: 'About',
      display_realm: false,
      display_profession: false
    },
};


// create Context
export const NavContext = createContext();


// create Provider
export const NavProvider = ({children}) => {
  
  const [nav, setNav] = useState(Nav.HOME);
  
  const value = {nav, setNav};
  
  return (
    <NavContext.Provider value={value}>
      {children}
    </NavContext.Provider>
  )
}
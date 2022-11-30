import { React, useState, createContext } from 'react';

// Navs enums for navigation metadata
export const Nav = {
    HOME: {
      order: 1,
      name: 'Home',
      display_realm: true
    },
    PROFESSION: {
      order: 2, 
      name: 'Profession',
      display_realm: true
    },
    ABOUT: {
      order: 3,
      name: 'About',
      display_realm: false
    },
};


export const NavContext = createContext(Nav.HOME);

export const NavProvider = ({children}) => {
  
  const [nav, setNav] = useState(Nav.HOME);
  
  const value = {nav, setNav};
  
  return (
    <NavContext.Provider value={value}>
      {children}
    </NavContext.Provider>
  )
}
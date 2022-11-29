import { React, useState, createContext } from 'react';

// metadata for navigation tabs
export const navs = {
    home: {
      order: 1,
      name: 'Home',
      display_realm: true
    },
    profession: {
      order: 2, 
      name: 'Profession',
      display_realm: true
    },
    about: {
      order: 3,
      name: 'About',
      display_realm: false
    },
};


export const NavContext = createContext(navs.home);

export const NavProvider = ({children}) => {
  const [nav, setNav] = useState(navs.home);
  const value = {nav, setNav};
  return (
    <NavContext.Provider value={value}>
      {children}
    </NavContext.Provider>
  )
}
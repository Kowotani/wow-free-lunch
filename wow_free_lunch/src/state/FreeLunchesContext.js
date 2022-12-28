import { useState, createContext } from 'react';


// create Context
export const FreeLunchesContext = createContext({});


// create Provider
export const FreeLunchesProvider = ({children}) => {
  
  const [freeLunches, setFreeLunches] = useState({
    is_loading: false,
    free_lunches: []
  });

  const value = {freeLunches, setFreeLunches};
  
  return (
    <FreeLunchesContext.Provider value={value}>
      {children}
    </FreeLunchesContext.Provider>
  )
}
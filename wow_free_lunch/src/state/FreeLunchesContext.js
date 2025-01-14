import { useState, createContext } from 'react';


// create Context
export const FreeLunchesContext = createContext({});


// create Provider
export const FreeLunchesProvider = ({children}) => {
  
  const [freeLunches, setFreeLunches] = useState({
    free_lunches: [],
    update_time: null,
  });

  const value = {freeLunches, setFreeLunches};
  
  return (
    <FreeLunchesContext.Provider value={value}>
      {children}
    </FreeLunchesContext.Provider>
  )
}
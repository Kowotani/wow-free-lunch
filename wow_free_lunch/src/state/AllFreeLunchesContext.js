import { useState, createContext } from 'react';


// create Context
export const AllFreeLunchesContext = createContext({});


// create Provider
export const AllFreeLunchesProvider = ({children}) => {
  
  const [allFreeLunches, setAllFreeLunches] = useState({
    is_loading: false,
    free_lunches: {}
  });

  const value = {allFreeLunches, setAllFreeLunches};
  
  return (
    <AllFreeLunchesContext.Provider value={value}>
      {children}
    </AllFreeLunchesContext.Provider>
  )
}
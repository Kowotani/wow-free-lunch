import { useState, createContext } from 'react';


// create Context
export const AllFreeLunchesContext = createContext({});


// create Provider
export const AllFreeLunchesProvider = ({children}) => {
  
  const [allFreeLunches, setAllFreeLunches] = useState({
    free_lunches: {},
    update_time: null,
  });

  const value = {allFreeLunches, setAllFreeLunches};
  
  return (
    <AllFreeLunchesContext.Provider value={value}>
      {children}
    </AllFreeLunchesContext.Provider>
  )
}
import { useState, createContext } from 'react';


// create Context
export const ReagentPricesContext = createContext({});


// create Provider
export const ReagentPricesProvider = ({children}) => {
  
  const [reagentPrices, setReagentPrices] = useState({});

  const value = {reagentPrices, setReagentPrices};
  
  return (
    <ReagentPricesContext.Provider value={value}>
      {children}
    </ReagentPricesContext.Provider>
  )
}
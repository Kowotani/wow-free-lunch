import { useState, createContext } from 'react';


// create Context
export const ReagentPricesContext = createContext({});


// create Provider
export const ReagentPricesProvider = ({children}) => {
  
  const [reagentPrices, setReagentPrices] = useState({
    by_item_class: {},
    by_item_id: {}
  });

  const value = {reagentPrices, setReagentPrices};
  
  return (
    <ReagentPricesContext.Provider value={value}>
      {children}
    </ReagentPricesContext.Provider>
  )
}
import { useState, createContext } from 'react';


// create Context
export const ReagentPricesContext = createContext({});


// create Provider
export const ReagentPricesProvider = ({children}) => {
  
  const [reagentPrices, setReagentPrices] = useState({
    is_loading: false,
    by_item_class: {},
    by_item_id: {},
    update_time: null,
  });

  const value = {reagentPrices, setReagentPrices};
  
  return (
    <ReagentPricesContext.Provider value={value}>
      {children}
    </ReagentPricesContext.Provider>
  )
}
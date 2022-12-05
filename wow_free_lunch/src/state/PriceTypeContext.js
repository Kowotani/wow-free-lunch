import { useState, createContext } from 'react';


// Price Type enum
export const PriceType = {
  VWAP: 'VWAP',
  MIN: 'Min'
};


// create Context
export const PriceTypeContext = createContext({
  type: PriceType.VWAP
});


// create Provider
export const PriceTypeProvider = ({children}) => {
  
  const [priceType, setPriceType] = useState({  
    type: PriceType.VWAP
  });
setPriceType
  const value = {priceType, setPriceType};
  
  return (
    <PriceTypeContext.Provider value={value}>
      {children}
    </PriceTypeContext.Provider>
  )
}
import { React, useState, createContext } from 'react';

export const FactionContext = createContext({
  name: 'Horde'
});

export const FactionProvider = ({children}) => {
  
  const [faction, setFaction] = useState({  
    name: 'Horde'
  });
  
  const value = {faction, setFaction};
  
  return (
    <FactionContext.Provider value={value}>
      {children}
    </FactionContext.Provider>
  )
}
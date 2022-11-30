import { React, useState, createContext } from 'react';


// Faction enum
export const Faction = {
  ALLIANCE: 'Alliance',
  HORDE: 'Horde'
}


// create Context
export const FactionContext = createContext({
  name: Faction.HORDE
});


// create Provider
export const FactionProvider = ({children}) => {
  
  const [faction, setFaction] = useState({  
    name: Faction.HORDE
  });
  
  const value = {faction, setFaction};
  
  return (
    <FactionContext.Provider value={value}>
      {children}
    </FactionContext.Provider>
  )
}
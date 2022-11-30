import { React, useState, createContext } from 'react';


// Faction enums
export const Faction = {
  ALLIANCE: 'Alliance',
  HORDE: 'Horde'
}


export const FactionContext = createContext({
  name: Faction.HORDE
});

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
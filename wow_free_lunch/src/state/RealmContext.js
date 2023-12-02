import { useState, createContext } from 'react';

// Realm enum
export const SupportedRealm = {
    BENEDICTION: 'Benediction',
    CHAOS_BOLT: 'Chaos Bolt',
    CRUSADER_STRIKE: 'Crusader Strike',
    FAERLINA: 'Faerlina',
    GROBBULUS: 'Grobbulus',
    LONE_WOLF: 'Lone Wolf',
    WILD_GROWTH: 'Wild Growth'
}


// create Context
export const RealmContext = createContext({});


// create Provider
export const RealmProvider = ({children}) => {
  
  const [realm, setRealm] = useState({  
    name: 'Lone Wolf',
    isSelectorTransitioning: false,
  });
  
  const value = {realm, setRealm};
  
  return (
    <RealmContext.Provider value={value}>
      {children}
    </RealmContext.Provider>
  )
}
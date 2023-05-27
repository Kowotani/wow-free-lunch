import { useState, createContext } from 'react';

// Realm enum
export const SupportedRealm = {
    ARUGAL: 'Arugal',
    BENEDICTION: 'Benediction',
    FAERLINA: 'Faerlina',
    GROBBULUS: 'Grobbulus',
    MANKRIK: 'Mankrik',
    PAGLE: 'Pagle',
    SKYFURY: 'Skyfury',
    WHITEMANE: 'Whitemane',
}


// create Context
export const RealmContext = createContext({});


// create Provider
export const RealmProvider = ({children}) => {
  
  const [realm, setRealm] = useState({  
    name: 'Whitemane',
    isSelectorTransitioning: false,
  });
  
  const value = {realm, setRealm};
  
  return (
    <RealmContext.Provider value={value}>
      {children}
    </RealmContext.Provider>
  )
}
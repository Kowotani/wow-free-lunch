import { useState, createContext } from 'react';

// Realm enum
export const SupportedRealm = {
    BENEDICTION: 'Benediction',
    ERANIKUS: 'Eranikus',
    MYZRAEL: 'Myzrael',
    SKYFURY: 'Skyfury',
}


// create Context
export const RealmContext = createContext({
  name: 'Skyfury'
});


// create Provider
export const RealmProvider = ({children}) => {
  
  const [realm, setRealm] = useState({  
    name: 'Skyfury'
  });
  
  const value = {realm, setRealm};
  
  return (
    <RealmContext.Provider value={value}>
      {children}
    </RealmContext.Provider>
  )
}
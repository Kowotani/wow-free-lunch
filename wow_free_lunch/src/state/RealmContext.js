import { useState, createContext } from 'react';

// Realm enum
export const SupportedRealm = {
    MYZRAEL: 'Myzrael',
    SKYFURY: 'Skyfury',
}


// create Context
export const RealmContext = createContext({});


// create Provider
export const RealmProvider = ({children}) => {
  
  const [realm, setRealm] = useState({  
    name: 'Skyfury',
    isSelectorTransitioning: false,
  });
  
  const value = {realm, setRealm};
  
  return (
    <RealmContext.Provider value={value}>
      {children}
    </RealmContext.Provider>
  )
}
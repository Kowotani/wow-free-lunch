import { useState, createContext } from 'react';

// Realm enum
export const SupportedRealm = {
    AZURESONG: 'Azuresong',
    MYZRAEL: 'Myzrael',
    SKYFURY: 'Skyfury',
    WINDSEEKER: 'Windseeker',
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
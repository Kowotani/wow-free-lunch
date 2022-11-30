import { React, useState, createContext } from 'react';


// create Context
export const RealmContext = createContext({
  name: "Skyfury"
});


// create Provider
export const RealmProvider = ({children}) => {
  
  const [realm, setRealm] = useState({  
    name: "Skyfury"
  });
  
  const value = {realm, setRealm};
  
  return (
    <RealmContext.Provider value={value}>
      {children}
    </RealmContext.Provider>
  )
}
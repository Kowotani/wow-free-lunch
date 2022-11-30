import { React, useState, createContext } from 'react';


// Profession enum
export const Profession = {
    ALCHEMY: 'Alchemy',
    BLACKSMITHING: 'Blacksmithing',
    COOKING: 'Cooking',
    ENGINEERING: 'Engineering',
    INSCRIPTION: 'Inscription',
    JEWELCRAFTING: 'Jewelcrafting',
    LEATHERWORKING: 'Leatherworking',
    TAILORING: 'Tailoring'
}

// create Context
export const ProfessionContext = createContext({
  name: Profession.BLACKSMITHING
});


// create Provider
export const ProfessionProvider = ({children}) => {
  
  const [profession, setProfession] = useState({  
    name: Profession.BLACKSMITHING
  });
  
  const value = {profession, setProfession};
  
  return (
    <ProfessionContext.Provider value={value}>
      {children}
    </ProfessionContext.Provider>
  )
}
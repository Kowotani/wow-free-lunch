import { useState, createContext } from 'react';


// create Context
export const CraftedItemRecipesContext = createContext({});


// create Provider
export const CraftedItemRecipesProvider = ({children}) => {
  
  const [craftedItemRecipes, setCraftedItemRecipes] = useState({
    is_loading: false,
    recipes: []
  });

  const value = {craftedItemRecipes, setCraftedItemRecipes};
  
  return (
    <CraftedItemRecipesContext.Provider value={value}>
      {children}
    </CraftedItemRecipesContext.Provider>
  )
}
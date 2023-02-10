import { useContext } from 'react';
import {
  Box,
  ChakraProvider,
  theme,
} from '@chakra-ui/react';

import { About } from './components/About'
import { AllFreeLunches } from './components/AllFreeLunches'
import { Header } from './components/Header'
import { ReagentPrices } from './components/ReagentPrices'
import { ProfessionFreeLunches } from './components/ProfessionFreeLunches'

import { AllFreeLunchesProvider } from './state/AllFreeLunchesContext';
import { CraftedItemRecipesProvider } from './state/CraftedItemRecipesContext';
import { FactionProvider } from './state/FactionContext';
import { FreeLunchesProvider } from './state/FreeLunchesContext';
import { Nav, NavContext, NavProvider } from './state/NavContext';
import { ProfessionProvider } from './state/ProfessionContext';
import { ReagentPricesProvider } from './state/ReagentPricesContext';
import { RealmProvider } from './state/RealmContext';


// =========
// Constants
// =========

const MIN_PAGE_WIDTH = 370


//  ========
//  Main App
//  ========

const MainContent = () => {
  const { nav } = useContext(NavContext);
  
  return (
    <>
    {nav === Nav.HOME && (
        <AllFreeLunches/>
      )}
    {nav === Nav.PROFESSION && (
      <>
        <ReagentPrices/>
        <ProfessionFreeLunches/>
      </>
    )}
    {nav === Nav.ABOUT && <About />} 
    </>
  )
}

function App() {
  
  return (
    <ChakraProvider theme={theme}>
      <AllFreeLunchesProvider>
        <CraftedItemRecipesProvider>
          <FactionProvider>
            <FreeLunchesProvider>
              <NavProvider>
                <ProfessionProvider>
                  <RealmProvider>
                    <ReagentPricesProvider>
                      
                      <Box minWidth={MIN_PAGE_WIDTH}>
                        <Header />
                        <MainContent />
                      </Box>
                      
                    </ReagentPricesProvider>
                  </RealmProvider>
                </ProfessionProvider>
              </NavProvider>
            </FreeLunchesProvider>
          </FactionProvider>
        </CraftedItemRecipesProvider>
      </AllFreeLunchesProvider>
    </ChakraProvider>
  );
}

export default App;

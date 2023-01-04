import { useContext, React } from 'react';
import {
  ChakraProvider,
  Box,
  Text,
  Link,
  VStack,
  Code,
  Grid,
  theme,
} from '@chakra-ui/react';
import { ColorModeSwitcher } from './ColorModeSwitcher';
import { Logo } from './Logo';

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
    {nav === Nav.ABOUT && <Box>About Content</Box>} 
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
                  
                      <Header />
                      <MainContent />
                      
                      <Box textAlign="center" fontSize="xl">
                        <Grid minH="100vh" p={3}>
                          <ColorModeSwitcher justifySelf="flex-end" />
                          <VStack spacing={8}>
                            <Logo h="40vmin" pointerEvents="none" />
                            <Text>
                              Edit <Code fontSize="xl">src/App.js</Code> and save to reload.
                            </Text>
                            <Link
                              color="teal.500"
                              href="https://chakra-ui.com"
                              fontSize="2xl"
                              target="_blank"
                              rel="noopener noreferrer"
                            >
                              Learn Chakra
                            </Link>
                          </VStack>
                        </Grid>
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

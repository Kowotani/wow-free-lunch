import { React } from 'react';
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
import { Header } from './components/Header'
import { ReagentPrices } from './components/ReagentPrices'


import { FactionProvider } from './state/FactionContext';
import { NavProvider } from './state/NavContext';
import { ProfessionProvider } from './state/ProfessionContext';
import { RealmProvider } from './state/RealmContext';

//  ========
//  Main App
//  ========


function App() {
  
  return (
    <ChakraProvider theme={theme}>
      <FactionProvider>
        <NavProvider>
          <ProfessionProvider>
            <RealmProvider>
              <Header />
              <Box>
                <ReagentPrices />
              </Box>
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
            </RealmProvider>
          </ProfessionProvider>
        </NavProvider>
      </FactionProvider>
    </ChakraProvider>
  );
}

export default App;

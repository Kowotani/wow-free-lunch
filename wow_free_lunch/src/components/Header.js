import {React, useState, useContext} from 'react';
import {
  Box,
  Button, 
  ButtonGroup,
  Image,
  Spacer,
} from '@chakra-ui/react';
import logo from '../assets/logo.png';
import { navs, NavContext, NavProvider } from '../state/NavContext';

// component for nav buttons in header
const NavButtons = () => {
  return (
    <ButtonGroup colorScheme="teal" spacing="2">
      <NavButton name="Home" navkey={navs.home}/>
      <NavButton name="Profession" navkey={navs.profession}/>
      <NavButton name="About" navkey={navs.about}/>
    </ButtonGroup>
  )
}

// component for individual nav button in header
const NavButton = (props) => {
  
  const { nav, setNav } = useContext(NavContext);
  
  const variant = (nav.name === props.name ? "solid" : "ghost");
  const onClick = () => {setNav(props.navkey)};
  
  return (
    
      <Button 
        variant={variant}
        onClick={onClick}
      >
        {props.name}
      </Button>
    
  )
}

// Header component
export const Header = () => {
  return (
    <NavProvider>
      <Box display="flex" bg="gray.300" color="white">
        <Box display="flex" alignItems="flex-end">
          <Image src={logo} h="100"/>
          <NavButtons />
        </Box>
        <Spacer />
        <Box display="flex" alignItems="flex-end" justify="flex-end" fontSize="xl">
          <p>Realm Selector</p>
        </Box>
      </Box>
    </NavProvider>
  )
};
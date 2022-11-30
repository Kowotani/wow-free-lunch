import {React, useState, useContext} from 'react';
import {
  Box,
  Button, 
  ButtonGroup,
  Image,
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  Spacer,
} from '@chakra-ui/react';
import { ChevronDownIcon } from '@chakra-ui/icons';

import logo from '../assets/logo.png';
import hordeIcon from '../assets/horde_icon.png';
import allianceIcon from '../assets/alliance_icon.png';

import { navs, NavContext, NavProvider } from '../state/NavContext';
import { RealmContext, RealmProvider } from '../state/RealmContext';
import { FactionContext, FactionProvider } from '../state/FactionContext';


// ===========
// Nav Section
// ===========


// component for nav buttons in header
// TODO: remove hard-coded navkey prop
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
  
  return (
    
      <Button 
        variant={variant}
        onClick={() => {setNav(props.navkey)}}
      >
        {props.name}
      </Button>
    
  )
}


// =============
// Realm Section
// =============


const RealmSelectorManager = () => {
  
  const { nav, setNav } = useContext(NavContext);
  
  return (
    <>
      {(nav === navs.home || nav === navs.profession) && <RealmSelector />}
    </>
  )
}


// component for realm selector
const RealmSelector = () => {
  
  const { realm, setRealm } = useContext(RealmContext);
  const { faction, setFaction } = useContext(FactionContext);
  
  const factionColorScheme = (faction.name === "Horde" ? "red" : "blue");
  
  return (
    <>
      <Menu>
        <MenuButton as={Button} colorScheme="blackAlpha">
          {realm.name}
        </MenuButton>
        <MenuList>
          <MenuItem onClick={() => {setRealm({name: "Angerforge"})}}>Angerforge</MenuItem>
          <MenuItem onClick={() => {setRealm({name: "Skyfury"})}}>Skyfury</MenuItem>
        </MenuList>
      </Menu>
      <Menu>
        <MenuButton as={Button} colorScheme={factionColorScheme}>
          {faction.name}
        </MenuButton>
        <MenuList>
          <MenuItem onClick={() => {setFaction({name: "Alliance"})}}>Alliance</MenuItem>
          <MenuItem onClick={() => {setFaction({name: "Horde"})}}>Horde</MenuItem>
        </MenuList>
      </Menu>
    </>
  )
}


// ==============
// Main Component
// ==============


// Header component
export const Header = () => {
  return (
    <NavProvider>
      <RealmProvider>
        <FactionProvider>
          <Box display="flex" bg="gray.300">
            <Box display="flex" alignItems="flex-end">
              <Image src={logo} h="100"/>
              <NavButtons />
            </Box>
            <Spacer />
            <Box display="flex" alignItems="flex-end" justify="flex-end" fontSize="xl">
              <RealmSelectorManager />
            </Box>
          </Box>
        </FactionProvider>
      </RealmProvider>
    </NavProvider>
  )
};
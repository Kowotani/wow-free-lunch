import { useContext, useEffect, useState, createRef, forwardRef, } from 'react';
import {
  Box,
  Button, 
  ButtonGroup,
  Icon,
  IconButton,
  Image,
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  Spacer,
} from '@chakra-ui/react';

import { CSSTransition } from 'react-transition-group'

import logo from '../assets/logo.png';
import { AllianceIcon, HordeIcon } from '../assets/Icons'

import { useWindowDimensions } from '../hooks/WindowDimensions';

import { Faction, FactionContext } from '../state/FactionContext';
import { Nav, NavContext } from '../state/NavContext';
import { Profession, ProfessionContext } from '../state/ProfessionContext';
import { RealmContext, SupportedRealm } from '../state/RealmContext';

import '../styles.css';


// =========
// Constants
// =========

// ProfessionBar
const PROFESSION_BAR_TWO_BREAKPOINT = 845   // 2 line display
const PROFESSION_BAR_TWO_HEIGHT = 88  // 2 line display height
const PROFESSION_BAR_THREE_BREAKPOINT = 450   // 3 line display
const PROFESSION_BAR_THREE_HEIGHT = 132  // 3 line display height
const PROFESSION_BAR_TRANSITION_TIME = 500  // transition delay

// RealmSelector
const REALM_SELECTOR_BREAKPOINT = 525   // Top or bottom display
const REALM_SELECTOR_TRANSITION_TIME = 500   // transition delay


// ===========
// Nav Section
// ===========


// component for nav buttons in header
// TODO: remove hard-coded navkey prop
const NavButtons = () => {
  return (
    <ButtonGroup colorScheme='teal' spacing={0}>
      <NavButton name="Home" navkey={Nav.HOME}/>
      <NavButton name="Profession" navkey={Nav.PROFESSION}/>
      <NavButton name="About" navkey={Nav.ABOUT}/>
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
        borderBottomRightRadius='0px'
        borderBottomLeftRadius='0px'
        borderTopLeftRadius='12px'
        borderTopRightRadius='12px'
      >
        {props.name}
      </Button>
  )
}


// ==============
// Realm Selector
// ==============

// component for Realm Selector
const RealmSelector = () => {

  const { nav } = useContext(NavContext);  
  const { realm, setRealm } = useContext(RealmContext);
  const { faction, setFaction } = useContext(FactionContext);
  
  const { width } = useWindowDimensions();
  
  const [ isRealmSelectorNav, setIsRealmSelectorNav ] = useState(false);
  
  const factionColorScheme = (faction.name === Faction.HORDE ? 'red' : 'blue');

  const nodeRef = createRef();


  useEffect(() => {
    
    // transition requires a toggle switching from false -> true
    setIsRealmSelectorNav(nav.display_realm);
  }, [nav])


  function updateRealm(name, isSelectorTransitioning) {
    setRealm({
      name: name,
      isSelectorTransitioning: isSelectorTransitioning
    })
  }


  return (
    <>
      <CSSTransition 
        nodeRef={nodeRef}
        timeout={REALM_SELECTOR_TRANSITION_TIME}
        in={isRealmSelectorNav}
        classNames={width < REALM_SELECTOR_BREAKPOINT 
          ? 'realmselectortop'
          : 'realmselectorbottom'
        }
        appear={true}
        unmountOnExit={true}
        onEnter={() => {updateRealm(realm.name, true)}}
        onEntered={() => {updateRealm(realm.name, false)}}
        onExit={() => {updateRealm(realm.name, true)}}
      >
        <Box ref={nodeRef} position='absolute' height='100%'>
          <Menu isLazy={true}>
            <MenuButton 
              as={Button} 
              bg='gray.600'
              _hover={{bg: '#3B4451'}}
              _active={{bg: 'gray.700'}}
              color='white'
              borderBottomRightRadius='0px'
              borderBottomLeftRadius={
                width < REALM_SELECTOR_BREAKPOINT
                  ? '12px'
                  : '0px'
              }
              borderTopLeftRadius={
                width < REALM_SELECTOR_BREAKPOINT
                  ? '0px'
                  : '12px'
              }
              borderTopRightRadius='0px'
            >
              {realm.name}
            </MenuButton>
            <MenuList minWidth={0}>
              {Object.values(SupportedRealm)
                .map((realm) => {
                  return (
                    <MenuItem 
                      key={realm} 
                      onClick={() => {updateRealm(realm, false)}}
                    >
                      {realm}
                    </MenuItem>
                  )
                })
                .sort()
              }
            </MenuList>
          </Menu>
          <Menu isLazy={true}>
            <MenuButton 
              as={IconButton} 
              colorScheme={factionColorScheme}
              icon={
                <Icon as={faction.name === Faction.HORDE
                  ? HordeIcon 
                  : AllianceIcon
                } 
                  boxSize='30px' 
                  color='white'
                />
              }
              borderBottomRightRadius={
                width < REALM_SELECTOR_BREAKPOINT
                  ? '12px'
                  : '0px'
              }
              borderBottomLeftRadius='0px'
              borderTopLeftRadius='0px'
              borderTopRightRadius={
                width < REALM_SELECTOR_BREAKPOINT
                  ? '0px'
                  : '12px'
              }
            >
              {faction.name}
            </MenuButton>
            <MenuList minWidth={0}>
              <MenuItem
                icon={<AllianceIcon boxSize='30px' color='blue.500'/>}
                onClick={() => {setFaction({name: Faction.ALLIANCE})}}
              >
                Alliance
              </MenuItem>
              <MenuItem 
                icon={<HordeIcon boxSize='30px' color='red'/>}
                onClick={() => {setFaction({name: Faction.HORDE})}}
              >
                Horde
              </MenuItem>
            </MenuList>
          </Menu>
        </Box>
      </CSSTransition>
    </>
  )
}


// ==============
// Profession Bar
// ==============


// component for Profession buttons in Profession Bar
const ProfessionButton = (props) => {
  
  const { nav } = useContext(NavContext);
  const { profession, setProfession } = useContext(ProfessionContext);
  
  const [ isProfessionNav, setIsProfessionNav ] = useState(false);
  
  const variant = (profession.name === props.profession ? "solid" : "ghost");
  
  const nodeRef = createRef();
  
  useEffect(() => {
    
    // transition requires a toggle switching from false -> true
    setIsProfessionNav(nav.display_profession);
  }, [nav])  

  return (
      <CSSTransition
        nodeRef={nodeRef}
        timeout={PROFESSION_BAR_TRANSITION_TIME}
        in={isProfessionNav}
        classNames='professionbarbutton'
        unmountOnExit={true}
      >
        <Button
          ref={nodeRef}
          variant={variant}
          onClick={() => {setProfession({name: props.profession})}}
          m='6px'
        >
          {props.name}
        </Button>
      </CSSTransition>
  )
}

// component for Profession Bar
const ProfessionBar = forwardRef((props, ref) => {

  return (
    <Box ref={ref}
        display='flex'
        width='100%' 
        bg='gray.100'
    >
      <ButtonGroup 
        width='100%' 
        colorScheme='blue' 
        size='sm' 
        spacing='0px' 
        alignItems='center'
        justifyContent='center' 
        flexWrap='wrap'
      >
        {Object.values(Profession)
          .map((profession) => {
            return (
              <ProfessionButton 
                key={profession} 
                name={profession} 
                profession={profession}
              />
            )
          })
          .sort()
        }
      </ButtonGroup>
    </Box>
  )
})

// manager displaying the Realm Selector
const ProfessionBarManager = () => {
  
  const { nav } = useContext(NavContext);
  
  const [ isProfessionNav, setIsProfessionNav ] = useState(false);

  const { width } = useWindowDimensions();

  const nodeRef = createRef();
  
  
  useEffect(() => {
    
    // transition requires a toggle switching from false -> true
    setIsProfessionNav(nav.display_profession);
  }, [nav])
  
  
  useEffect(() => {
    
    // set the CSS height property for the ProfessionBar
    if (nodeRef.current?.offsetHeight !== undefined) {
      nodeRef.current?.style?.setProperty(
        '--h', nodeRef.current?.offsetHeight + 'px');
    }
  }, [nodeRef, width])


  useEffect(() => {
    
    // set the CSS height property for the ProfessionBar
    if (width < PROFESSION_BAR_THREE_BREAKPOINT) {
      nodeRef.current?.style?.setProperty(
        '--h', PROFESSION_BAR_THREE_HEIGHT + 'px');
    } else if (width < PROFESSION_BAR_TWO_BREAKPOINT) {
      nodeRef.current?.style?.setProperty(
        '--h', PROFESSION_BAR_TWO_HEIGHT + 'px');
    }
  }, [nodeRef, nav, width])


  return (
    <>
      <CSSTransition 
        nodeRef={nodeRef}
        timeout={PROFESSION_BAR_TRANSITION_TIME}
        in={isProfessionNav}
        classNames='professionbar'
      >
        <ProfessionBar ref={nodeRef}/>
      </CSSTransition>
    </>
  )
}


// ==============
// Main Component
// ==============


// Header content
export const Header = () => {
  
  const { realm } = useContext(RealmContext);
  
  const [ realmSelectorLocation, setRealmSelectorLocation ] = useState('bottom');
  
  const { width } = useWindowDimensions();
  
  useEffect(() => {
    setRealmSelectorLocation(width < REALM_SELECTOR_BREAKPOINT ? 'top' : 'bottom')
  }, [width])
  
  
  return (
    <>
      <Box 
        display='flex' 
        bg='gray.300' 
        flexWrap='wrap' 
        borderBottom='4px' 
        borderColor='teal.500'
      >
        <Image src={logo} w='100px' m='0px 8px 0px 0px'/>
        <Box display='flex' flexGrow={1} flexDirection='column'>
        
          <Box 
            display='flex' 
            width='100%' 
            flexGrow={1} 
            justifyContent='flex-end' 
            position='relative' 
            overflow={realm.isSelectorTransitioning ? 'hidden' : 'visible'}
          >
            <Spacer />
            {realmSelectorLocation === 'top' && <RealmSelector />}
          </Box>
          
          <Box display='flex'>
            <Box display='flex' justifyContent='flex-start' alignItems='flex-end'>
              <NavButtons />
            </Box>
            <Spacer flexShrink />
            <Box 
              display='flex' 
              flexGrow={4} 
              justifyContent='flex-end' 
              position='relative' 
              overflow={realm.isSelectorTransitioning ? 'hidden' : 'visible'}
            >
              {realmSelectorLocation === 'bottom' && <RealmSelector />}
            </Box>
          </Box>
          
        </Box>
      </Box>    
      <ProfessionBarManager />
    </>
  )
}
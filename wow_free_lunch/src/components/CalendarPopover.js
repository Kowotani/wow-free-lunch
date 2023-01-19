import {
  Box,
  Icon,
  IconButton,
  Popover,
  PopoverTrigger,
  PopoverContent,
  PopoverArrow,
  PopoverBody,
} from '@chakra-ui/react';

import { CgCalendar } from 'react-icons/cg'


// ==============
// Main Component
// ==============


export const CalendarPopover = (props) => {
  
  return (
    <Popover placement='left' arrowShadowColor={props.color}>
      <PopoverTrigger display='flex' alignItems='center'>
        <IconButton 
          size='sm'
          colorScheme='teal' 
          icon={<Icon as={CgCalendar} boxSize='24px' />}
          isDisabled={props.isDisabled}
        />
      </PopoverTrigger>
      <PopoverContent width='150px' height='34px' bg={props.color} borderColor={props.color}>
        <PopoverArrow bg={props.color}/>
        <PopoverBody>
          <Box textAlign='center' fontSize='sm'>
            {props.label}
          </Box>
        </PopoverBody>
      </PopoverContent>
    </Popover>    
  )
}
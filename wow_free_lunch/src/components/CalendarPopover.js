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
          colorScheme='teal' 
          icon={<Icon as={CgCalendar} boxSize='24px' />} 
        />
      </PopoverTrigger>
      <PopoverContent width='200px' bg={props.color} borderColor={props.color}>
        <PopoverArrow bg='gray.600'/>
        <PopoverBody>
          <Box textAlign='center'>
            {props.label}
          </Box>
        </PopoverBody>
      </PopoverContent>
    </Popover>    
  )
}
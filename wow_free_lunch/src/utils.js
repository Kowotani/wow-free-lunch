// =========
// Constants
// =========

// dev origin (for API calls)
export const DEV_BASE_URL = 'https://0983fcdb7462476a98cf4fcf96f8e461.vfs.cloud9.us-west-1.amazonaws.com'


// =========
// Functions
// =========

// return text color for an item given the input quality
export function getItemQualityColor(quality) {
  switch (quality) {
    
    case 'COMMON':
      return 'black'
      
    case 'UNCOMMON':
      // return '#1eff00' true colour
      return '#1eb600'
      
    case 'RARE':
      return '#0070dd'
      
    case 'EPIC': 
      return '#a335ee'
    
    default:
      return 'black'
  }
}

// return the date formatted as `MMM [D]D, HH:00 [AA]`
export function getFormattedDate(input_date) {
  
  const date = input_date.toLocaleDateString(
    'en-us', {month: 'short', day: 'numeric'})
    
  const time = input_date.toLocaleTimeString(
    'en-us', {hour: 'numeric'})
  
  return `${date}, ${time}`
}

// return a random integer between min and max inclusive
export function getRandomInt(min=1, max=100) { 
  return Math.floor(Math.random() * (max - min + 1) + min)
}

// return WoWHead url formatted with item_id
export function getWowHeadUrl(item_id) {
  return `https://www.wowhead.com/wotlk/item=${item_id}/`
}
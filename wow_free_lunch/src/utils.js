// return WoWHead url formatted with item_id
export function getWowHeadUrl(item_id) {
  return `https://www.wowhead.com/wotlk/item=${item_id}/`
}

// return text color for an item given the input quality
export function getItemQualityColor(quality) {
  switch (quality) {
    
    case 'COMMON':
      return 'black'
      
    case 'UNCOMMON':
      return '#1eff00'
      
    case 'RARE':
      return '#0070dd'
      
    case 'EPIC': 
      return '#a335ee'
    
    default:
      return 'black'
  }
}
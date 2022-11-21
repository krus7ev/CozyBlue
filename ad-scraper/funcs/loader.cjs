const fs = require('fs/promises');

module.exports = {
  /** Parses ads.txt into a css selector */
  getAdsSelector: async () => {
    const data = await fs.readFile('ads.txt', { encoding: 'utf8' });
    return data.split('\n').filter(row => row.startsWith('##')).map(row => row.slice(2)).join(', ');
  },
  /** Parses obstructions.txt into a css selector */
  getObstructionsSelector: async () => {
    const data = await fs.readFile('obstructions.txt', { encoding: 'utf8' });
    return data.split('\n').filter(row => row.startsWith('##')).map(row => row.slice(2)).join(', ');
  },
  /** Parses domains.txt into a list of domains */
  getDomains: async () => {
    const data = await fs.readFile('domains.txt', { encoding: 'utf8' });
    return data.split('\n').filter(domain => (!domain.startsWith('//')));
  }
};
/**
 * This script will first:
 *   Load domains from domains.txt;
 *   Load selectors for obstructions from obstructions.txt;
 *   Load selectors for ads from ads.txt;
 *   Launch Puppeteer.
 * 
 * Then:
 *   Visit each domain;
 *   Mess around to fully load the page;
 *   Remove obstructions;
 *   Identify ads and fetch their geometry;
 *   Take screenshots of the ads and place into relevant folders;
 *   Identify ad networks;
 *   Log results to console.
 * 
 * Finally:
 *   Write the collected data to data.json;
 *
 * Tip: generalFuncs.pause() pauses the script until you press enter in the console.
 */

// TODO: click consent buttons

const puppeteer = require('puppeteer');
const loader = require('./funcs/loader.cjs');
const fs = require('fs/promises');
const pageFuncs = require('./funcs/pageFuncs.cjs');
const generalFuncs = require('./funcs/generalFuncs.cjs');

(async () => {

  let data = {};

  const domainsPromise = loader.getDomains();
  const adsSelectorPromise = loader.getAdsSelector();
  const obstructionsSelectorPromise = loader.getObstructionsSelector();
  const browser = await puppeteer.launch({
     headless: false
  });
  const page = (await browser.pages())[0];
  await page.setViewport({ width: 1900, height: 900 });

  const domains = await domainsPromise;
  for (const domain of domains) {
    try {
      
      await page.goto(`http://${domain}`);
      pageFuncs.fuckAround(page);
      await new Promise(r => setTimeout(r, 3000))
      await page.evaluate(pageFuncs.removeObstructions, await obstructionsSelectorPromise);
      await new Promise(r => setTimeout(r, 1000));
      const bodyRect = await page.evaluate(pageFuncs.getBodyRect);
      const ads = await pageFuncs.getAds(await adsSelectorPromise, page, domain);
      const adsVolume = ads.reduce((sumVolume, ad) => sumVolume += (ad.height * ad.width), 0);
      const bodyVolume = (bodyRect.height * bodyRect.width);
      const refIds = await page.evaluate(pageFuncs.fetchRefIds);
      
      data[domain] = {
        ads: ads,
        refIds: refIds,
        adsVolume: adsVolume / bodyVolume
      }
  
      console.log(domain, ads, refIds);

    } catch(err) {

      console.log(err);
      continue

    }
  }

  await browser.close();
  await fs.writeFile('data.json', JSON.stringify(data));

})();
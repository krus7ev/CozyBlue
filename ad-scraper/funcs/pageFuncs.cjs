const fs = require('fs');

if (!fs.existsSync(`screenshots`)) {
  fs.mkdirSync(`screenshots`);
}

/** Take a screenshot of the specified rects and save to disk */
const takeScreenshots = async (page, rects, domain) => {
  if (rects.length && !fs.existsSync(`screenshots/${domain}`)) {
    fs.mkdirSync(`screenshots/${domain}`);
  }
  for (const rect of rects) {
    const element = await page.$(`#ad_${rect.id}`);
    const boundingRect = await element.boundingBox();
    if (boundingRect.height < 1 || boundingRect.width < 1) continue;
    await element.screenshot({ path: `screenshots/${domain}/${rect.id}.png` });
    await new Promise(r => setTimeout(r, 100));
  }
};

module.exports = {
  /** Alter viewport size, scroll down and back up */
  fuckAround: async (page) => {
    await page.setViewport({ width: 1900, height: 9999 });
    await new Promise(r => setTimeout(r, 500));
    await page.setViewport({ width: 1900, height: 900 });
    await page.evaluate(async () => {
      await new Promise((resolve) => {
        var totalHeight = 0;
        var distance = 100;
        const limit = 35;
        var counter = 0;
        var timer = setInterval(() => {
          var scrollHeight = document.body.scrollHeight;
          window.scrollBy(0, distance);
          totalHeight += distance;
          counter++
          if (
            (totalHeight >= scrollHeight - window.innerHeight) ||
            (counter >= limit)
          ) {
            clearInterval(timer);
            resolve();
          }
        }, 100);
      });
      window.scrollTo(0, 0);
    });
  },
  /** Get the size and position of ad elements on page */
  getAds: async (adsSelector, page, domain) => {
    const rects = await page.evaluate((adsSelector) => {
      return [...document.querySelectorAll(adsSelector)].map(element => {
        const adId = (Math.random() + 1).toString(36).substring(7);
        element.id = `ad_${adId}`;
        const rect = element.getBoundingClientRect();
        return {
          id: adId,
          x: rect.x,
          y: rect.y,
          width: rect.width,
          height: rect.height
        }
      }).filter(
        rect => Boolean(Math.floor(rect.width)) && Boolean(Math.floor(rect.height))
      );
    }, adsSelector);
    await takeScreenshots(page, rects, domain);
    return rects;
  },
  /** Get the page body dimensions */
  getBodyRect: () => {
    const rect = document.body.getBoundingClientRect();
    return {
      height: rect.height,
      width: rect.width
    };
  },
  /** Remove elements that might obstruct ads */
  removeObstructions: (obstructionsSelector) => {
    document.querySelectorAll(obstructionsSelector).forEach(el => el.style.display = 'none !important');
  },
  /** Get referral ids */
  fetchRefIds: () => {
    let refIds = {
      other: [],
    };

    const html = document.body.innerHTML;

    const adSenseIdIndex = html.indexOf('pub-');
    if (adSenseIdIndex > -1) {
      const adSenseId = html.slice(adSenseIdIndex, adSenseIdIndex + 20);
      if (!isNaN(adSenseId.slice(4))) {
        refIds.adSense = adSenseId;
      }
    }

    const cleverNt = document.querySelector('[name="clever-core-ads"]');
    if (cleverNt) {
      refIds.cleverNt = cleverNt.src;
    }

    const other = document.querySelectorAll('a.adlink');
    if (other.length) {
      refIds.other.push() = cleverNt.href;
    }

    const adsKeeperIndex = html.indexOf('jsc.adskeeper.com');
    if (adsKeeperIndex > -1) {
      refIds.adsKeeper = html.slice(
        adsKeeperIndex,
        adsKeeperIndex + html.slice(adsKeeperIndex).indexOf('"')
      );
    }

    const mgidIndex = html.indexOf('jsc.mgid.com');
    if (mgidIndex > -1) {
      refIds.mgid = html.slice(
        mgidIndex,
        mgidIndex + html.slice(mgidIndex).indexOf('"')
      );
    }

    const eadSrvIndex = html.indexOf('eadsrv.com/display');
    if (eadSrvIndex > -1) {
      refIds.eadSrv = html.slice(
        eadSrvIndex,
        eadSrvIndex + html.slice(eadSrvIndex).indexOf('"')
      );
    }

    const geniusDIndex = html.indexOf('geniusdexchange.com/ad/display.php');
    if (geniusDIndex > -1) {
      refIds.geniusD = html.slice(
        geniusDIndex,
        geniusDIndex + html.slice(geniusDIndex).indexOf('"')
      );
    }

    const eTargetIndex = html.indexOf('etargetnet.com');
    if (eTargetIndex > -1) {
      refIds.eTarget = true;
    }

    return refIds;
  }
};
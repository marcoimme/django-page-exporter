const puppeteer = require('puppeteer');
const Handlebars = require('handlebars');
var DOMParser = require('xmldom').DOMParser;

const address = process.argv[2],
    output = process.argv[3];


let config = {};
process.argv.forEach(function (arg, i) {
    if (i > 3) {
        namev = arg.split('=');
        config[namev[0].replace('--', '')] = namev[1];
    }
});


const VIEWPORT = { width: parseInt(config.width || 1024), height: parseInt(config.height || 768) };
// , defaultViewport: {width: config.heigh, height: 768}
(async () => {
  const browser = await puppeteer.launch({args: ['--no-sandbox']});
  const page = await browser.newPage();

  if (config.cookie_name != null) {
    let cookies = [{
          'name': config.cookie_name || 'sessionid',
          'value': config.cookie_value || '',
          'domain': config.cookie_domain || 'localhost',
          'session': true
      }];
      await page.setCookie(...cookies);
  }

  if(address.startsWith("http://") || address.startsWith("https://")){
    await page.goto(address, {waitUntil: ['load', 'networkidle0']});
  }else{
    const template = Handlebars.compile("{{body}}");
    await page.goto(`data:text/html,${address}`, { waitUntil: 'networkidle0' });
  }

  if(config.format === 'pdf'){
    await page.pdf({path: output, format: "A4", landscape: config.landscape === 'true', printBackground: true});
  }else{
    await page.setViewport(VIEWPORT);

    await page.screenshot({
      path: output,
      fullPage: true
    });
  }

  await browser.close();
})();
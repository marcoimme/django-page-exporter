const puppeteer = require('puppeteer');

const address = process.argv[2],
    output = process.argv[3];

console.log(1111111, address, output);

let config = {};
process.argv.forEach(function (arg, i) {
    if (i > 3) {
        namev = arg.split('=');
        config[namev[0].replace('--', '')] = namev[1];
    }
});

console.log(1111111, config);

(async () => {
  const browser = await puppeteer.launch({args: ['--no-sandbox']});
  const page = await browser.newPage();
  console.log(22222, config.cookie_name, config.cookie_value);
  if (config.cookie_name != null) {
    let cookies = [{
          'name': config.cookie_name || 'sessionid',
          'value': config.cookie_value || '',
          'domain': config.cookie_domain || 'localhost',
          'session': true
      }];
      await page.setCookie(...cookies);
  }


  await page.goto(address, {waitUntil: 'networkidle0'});
  await page.pdf({path: output, format: "A4"});
  // await page.screenshot({path: output});

  await browser.close();
})();
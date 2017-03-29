/**
 * Created by marco on 3/27/17.
 */

var page = require('webpage').create(),
    system = require('system');


function waitFor(testFx, onReady, timeOutMillis) {
    var maxtimeOutMillis = timeOutMillis ? timeOutMillis : 3000, //< Default Max Timout is 3s
        start = new Date().getTime(),
        condition = false,
        interval = setInterval(function () {
            if ((new Date().getTime() - start < maxtimeOutMillis) && !condition) {
                // If not time-out yet and condition not yet fulfilled
                condition = (typeof(testFx) === "string" ? eval(testFx) : testFx()); //< defensive code
            } else {
                if (!condition) {
                    // If condition still not fulfilled (timeout but condition is 'false')
                    console.log("'waitFor()' timeout");
                    phantom.exit(1);
                } else {
                    // Condition fulfilled (timeout and/or condition is 'true')
                    console.log("'waitFor()' finished in " + (new Date().getTime() - start) + "ms.");
                    typeof(onReady) === "string" ? eval(onReady) : onReady(); //< Do what it's supposed to do once the condition is fulfilled
                    clearInterval(interval); //< Stop this interval
                }
            }
        }, 250); //< repeat check every 250ms
};

/**
 * arguments:
 * [1] => URL
 * [2] => output. Use /dev/stdout if you want to capture.
 * [3] => size
 */

var address = system.args[1],
    output = system.args[2];

config = {};
system.args.forEach(function (arg, i) {
    if (i > 2) {
        namev = arg.split('=');
        config[namev[0].replace('--', '')] = namev[1];
    }
});

var method = config.method || 'get',
    width = config.width || 1400,
    height = config.height || 1,
    wait = config.wait || 200;

/**
 * please note: the default height is intentionaly left as 1.
 * the thing is, if you skip the height, phantomjs falls back
 * to some default viewport. and that's not what we want. we
 * want to set the width, and let the height auto-calculate.
 */
page.viewportSize = {width: width, height: height};

format = config.format || 'png';

var check_page_status = config.page_status || null;

if (config.cookie_name != null) {
    phantom.addCookie({
        'name': config.cookie_name || 'sessionid',
        'value': config.cookie_value || '',
        'domain': config.cookie_domain || 'localhost'
    });
}


page.open(address, function (status) {
    if (status == 'success') {

        if (check_page_status != null) {
            waitFor(function () {
                // Check in the page if a specific element is now visible
                return page.evaluate(function () {
                    // check if custom variable 'aaa' is set after mapReady function into page
                    return document.page_status == 'ready';
                });
            }, function () {
                page.render(output, {format: format});
                phantom.exit();
            }, parseInt(wait));
        } else {
            setTimeout(function(){
                page.render(output, {format: format});
                phantom.exit();
            }, wait);
        }


    }
});
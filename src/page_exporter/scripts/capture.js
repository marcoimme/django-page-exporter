/**
 * Created by marco on 3/27/17.
 */

var page = require('webpage').create(),
    system = require('system');

/**
 * arguments:
 * [1] => URL
 * [2] => output. Use /dev/stdout if you want to capture.
 * [3] => size
 */

var address = system.args[1],
    output = system.args[2];


page.onConsoleMessage = function (msg) {
    console.log(msg);
};

phantom.onError = function (msg, trace) {
    var msgStack = ['PHANTOM ERROR: ' + msg];
    if (trace && trace.length) {
        msgStack.push('TRACE:');
        trace.forEach(function (t) {
            msgStack.push(' -> ' + (t.file || t.sourceURL) + ': ' + t.line + (t.function ? ' (in function ' + t.function + ')' : ''));
        });
    }
    console.log(msgStack.join('\n'));
    phantom.exit(1);
};

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
}



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
    css_selector = config.selector || null,
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
        'domain': config.cookie_domain || 'localhost',
        'secure': config.cookie_secure || false
    });
}

function render(p, out) {
    if (css_selector != null) {
        var cc = p.evaluate(function (css_s) {
            return document.querySelector(css_s).getBoundingClientRect();
        }, css_selector);

        p.clipRect = {
            top: cc.top,
            left: cc.left,
            width: cc.width,
            height: cc.height
        };

        p.render(out, {format: format});
    } else {
        p.render(out, {format: format});
    }
    phantom.exit();

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
                render(page, output);
            }, parseInt(wait));
        } else {
            setTimeout(function () {
                render(page, output);
            }, wait);
        }


    }else if(status == 'fail'){
        phantom.exit();
    }
});
const CDP = require('chrome-remote-interface');

const userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'

CDP(async function(client) {
    const {Network, Page} = client;
    await Page.enable();
    await Network.enable();
    await Network.setUserAgentOverride({userAgent});
});

Object.defineProperty(navigator, 'languages', {
    get: function() {
        return ['ko-KR','ko'];
    }
});

Object.defineProperty(navigator, 'plugins', {
    get: function() {
        return [1,2,3,4,5];
    }
});

const getParameter = WebGLRenderingContext.getParameter;
WebGLRenderingContext.prototype.getParameter = function(parameter) {
    if (parameter === 37445) {
        return 'Intel Open Source Technology Center';
    }

    if (parameter === 37446) {
        return 'Mesa DRI Intel(R) Ivybridge Mobile';
    }
    return getParameter(parameter);
};

['height','width'].foreach(property => {
    const imageDescriptor = Object.getOwnPropertyDescriptor(HTMLImageElement.prototype, property);
    Object.defineProperty(HTMLImageElement.prototype, property, {
        ...imageDescriptor,
        get: function() {
            if (this.complete && this.naturalHeight == 0) {
                return 20;
            }
            return imageDescriptor.get.apply(this);
        },
    });
});

const elementDescriptor = Object.getOwnPropertyDescriptor(HTMLImageElement.prototype, 'offsetHeight');
Object.defineProperty(HTMLDivElement.prototype, 'offsetHeight', {
    ...elementDescriptor,
    get: function() {
        if (this.id === 'modernizr') {
            return 1;
        }
        return elementDescriptor.get.apply(this);
    },
});
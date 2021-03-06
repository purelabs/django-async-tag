/*
 * Most parts adapted from jquery:
 *
 * https://github.com/jquery/jquery/blob/master/src/manipulation.js
 */
(function() {
    'use strict';

    var reScriptType = /^$|\/(?:java|ecma)script/i;
    var reCleanScript = /^\s*<!(?:\[CDATA\[|--)|(?:\]\]|--)>\s*$/g;

    function globalLoad(type, src) {
        var script = document.createElement('script');
        script.type = type;
        script.src = src;
        document.head.appendChild(script).parentNode.removeChild(script);
    }

    function globalEval(code) {
        var script = document.createElement('script');
        script.text = code;
        document.head.appendChild(script).parentNode.removeChild(script);
    }

    function getAll(context, tag) {
        // Support: IE9-11+
        // Use typeof to avoid zero-argument method invocation on host objects (#15151)
        var ret = typeof context.getElementsByTagName !== 'undefined'
            ? context.getElementsByTagName( tag || '*' )
            : typeof context.querySelectorAll !== 'undefined'
                ? context.querySelectorAll( tag || '*' )
                : [];

        if (tag === undefined || tag && context.nodeName && context.nodeName.toLowerCase() === tag.toLowerCase()) {
            ret.splice(0, 0, context);
        }

        return ret;
    }

    function replaceWith(element, content) {
        var fragment = document.createDocumentFragment();
        var wrapper = document.createElement('div');

        wrapper.innerHTML = content;

        while(wrapper.childNodes.length) {
            fragment.appendChild(wrapper.childNodes[0]);
        }

        var scripts = getAll(fragment, 'script');

        for (var i=0; i<scripts.length; i++) {
            scripts[i].type = 'ignore/' + scripts[i].type;
        }

        element.parentNode.replaceChild(fragment, element);

        for (var i=0; i<scripts.length; i++) {
            var script = scripts[i];

            script.type = script.type.substring('ignore/'.length);

            if (reScriptType.test(script.type)) {
                if (script.src) {
                    globalLoad(script.type, script.src);
                } else {
                    globalEval(script.textContent.replace(reCleanScript, ''));
                }
            }
        }
    }

    function replaceAsyncTags(uuid) {
        var startElement = document.getElementById('async_begin_' + uuid);
        var endElement = document.getElementById('async_end_' + uuid);
        var contentElement = document.getElementById('async_' + uuid);
        var element = startElement;
        while (element !== endElement) {
            var nextElement = element.nextSibling;
            element.parentNode.removeChild(element);
            element = nextElement;
        }
        replaceWith(endElement, contentElement.textContent.replace('<\\/script>', '</' + 'script>'));
    }

    window.async_tag = {
        replaceAsyncTags: replaceAsyncTags
    };
})();

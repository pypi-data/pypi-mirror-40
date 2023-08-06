// Adds a button to hide the input part of the currently selected cells

define([
    'jquery',
    'base/js/namespace',
    'base/js/events'
], function(
    $,
    Jupyter,
    events
) {
    "use strict";
    var load_ipython_extension = function() {
        console.log('loaded hotjar');
    };
    return {
        load_ipython_extension : load_ipython_extension
    };
});

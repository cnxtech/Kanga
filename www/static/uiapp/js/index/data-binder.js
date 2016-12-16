var total_set = 38620;
var total_defects = 1176;
var total_cnc_success = 1311;
var total_cnc_failure = 245;
var test_per_set = 25;
function getTotalSet(){
    return total_set + Math.round((total_cnc_success+total_cnc_failure)/test_per_set);
}
function getTotalDefect(){
    return total_defects + Math.round((total_cnc_failure)/test_per_set);
}
var Row = function(row, dt) {
    this.row = ko.observable(row);
};
ko.observableArray.fn.subscribeArrayChanged = function(addCallback) {
    console.log(addCallback);
    var previousValue = undefined;
    this.subscribe(function(_previousValue) {
        previousValue = _previousValue.slice(0);
    }, undefined, 'beforeChange');
    this.subscribe(function(latestValue) {
        var editScript = ko.utils.compareArrays(previousValue, latestValue);
        for (var i = 0, j = editScript.length; i < j; i++) {
//            console.log(editScript[i].status);
            var isRow = (editScript[i].value instanceof Row);
            if (editScript[i].status == "added" && addCallback && isRow ) {
                addCallback(editScript[i].value);
            }
        }
        previousValue = undefined;
    });
};

function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

var statsViewModel = {
    totalNumOfSET: ko.observable(numberWithCommas(getTotalSet())),
    totalCNCTestSuccess: ko.observable(numberWithCommas(total_cnc_success)),
    totalCNCTestFailure: ko.observable(numberWithCommas(total_cnc_failure)),
    totalDefect: ko.observable(numberWithCommas(getTotalDefect())),
};
ko.applyBindings(statsViewModel,document.getElementById("statPanel"));

/**
 * Created by SRIN on 5/4/2015.
 */
var Helper = {};

/**
 * CREATE DROPDOWN
 */

Helper.initDropdown = function(id){
    var config = {
        '.chosen-select': {},
        '.chosen-select-deselect': {allow_single_deselect: true},
        '.chosen-select-no-single': {disable_search_threshold: 10},
        '.chosen-select-no-results': {no_results_text: 'Oops, nothing found!'},
        '.chosen-select-width': {width: "100px"}
    }
    for (var selector in config) {
        //console.log("ID ==> "+$(selector).attr('id'));
        $(selector).chosen(config[selector]);
        //$(selector).val('').trigger("chosen:updated");
    }
}
/**
 * CREATE EDITTEXT
 */
Helper.initEditText = function(arg, cid) {
    var $cpET = ArgumentLoader.LAYOUT_DEFINITION.find("#copy-edittext").clone();
    $cpET.attr("id","et"+cid);
    $cpET.find("label").html(arg.name);
    ArgumentLoader.modalForm.append($cpET);

}

/**
 * CREATE CHECK BOX
 */
Helper.initCheckBox = function() {
    $('.i-checks').iCheck({
        checkboxClass: 'icheckbox_square-green',
        radioClass: 'iradio_square-green'
    });
}

/**
 * CREATE DATETIME PICKER
 */
Helper.initDateTimePicker = function() {
    $('.col-sm-10 .input-group.date').datetimepicker();
    $('.col-sm-10 .input-group.date').on("dp.change",function (e) {
        var elem = $(this).find("input");
        if(elem){
            elem.change();
        }
    });
}

/**
 * CREATE SPINNER
 */
Helper.initSpinner = function(cid, min, max, current) {
    var id =cid;
    $("#"+id).ionRangeSlider({
        min: min,
        max: max,
        from: current,
        postfix: "",
        prettify: false,
        hasGrid: true
    });
}
/**
 * CREATE COLOR PICKER
 */
Helper.initColorPicker = function() {
    $('INPUT.color-input').minicolors();
}

Helper.clone = function(obj) {
    if (null == obj || "object" != typeof obj) return obj;
    var copy = obj.constructor();
    for (var attr in obj) {
        if (obj.hasOwnProperty(attr)) copy[attr] = obj[attr];
    }
    return copy;
}

Helper.erroProviderLayout = '<span class="glyphicon glyphicon-warning-sign" style="color: red" title="Oops... something went wrong"></span>';
Helper.blink = function(elem, times)
{
    for(var i=0;i<times;i++) {
        elem.fadeTo('slow', 0.1).fadeTo('slow', 1.0);
    }
}
Helper.showErrorProvider = function(element, errorMessage){
    Helper.clearErrorProvider(element);
    var ep = $(Helper.erroProviderLayout);
    ep.attr("title", errorMessage);
    ep.appendTo(element);
    Helper.blink(ep, 5);
}
Helper.clearErrorProvider = function(element) {
    var obj = element.find(".glyphicon-warning-sign");
    if (obj != undefined) {
        obj.remove();
    }
}

function loadjscssfile(filename, filetype){
    if (filetype=="js"){ //if filename is a external JavaScript file
        var fileref=document.createElement('script')
        fileref.setAttribute("type","text/javascript")
        fileref.setAttribute("src", filename)
    }
    else if (filetype=="css"){ //if filename is an external CSS file
        if($("link[href*='"+filename+"']").length == 0 ) {
            var fileref = document.createElement("link")
            fileref.setAttribute("rel", "stylesheet")
            fileref.setAttribute("type", "text/css")
            fileref.setAttribute("href", filename)
        }
    }
    if (typeof fileref!="undefined")
        document.getElementsByTagName("head")[0].appendChild(fileref)
}
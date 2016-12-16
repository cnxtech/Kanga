/**
 * Created by SRIN on 2/23/2015.
 */
var ArgumentLoader = {};
/**
 *  INITALIZATION ArgumentLoader Class
 */
ArgumentLoader.init = function() {
    //$.get(BASIC_PATH+"tpl/processor-editor-layout.html", function (data) {
      //  ArgumentLoader.LAYOUT_DEFINITION = $( data );
    //});
}

/**
 * CREATE DROPDOWN
 */

ArgumentLoader.initDropdown = function(id){
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
    }
}
/**
 * CREATE EDITTEXT
 */
ArgumentLoader.initEditText = function(arg, cid) {
    var $cpET = ArgumentLoader.LAYOUT_DEFINITION.find("#copy-edittext").clone();
    $cpET.attr("id","et"+cid);
    $cpET.find("label").html(arg.name);
    ArgumentLoader.modalForm.append($cpET);

}

/**
 * CREATE CHECK BOX
 */
ArgumentLoader.initCheckBox = function() {
    $('.i-checks').iCheck({
        checkboxClass: 'icheckbox_square-green',
        radioClass: 'iradio_square-green'
    });
}

/**
 * CREATE DATETIME PICKER
 */
ArgumentLoader.initDateTimePicker = function() {
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
ArgumentLoader.initSpinner = function(cid, min, max, current) {
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




// DATA BINDING MODEL
function ArgumentModel(data) {
    this.name = ko.observable(data.name);
    this.type = ko.observable(data.type);
    this.placeholder = ko.observable(data.placeholder);
    this.value = ko.observable(data.value);
    this.options = ko.observableArray( data.options);

    this.min = ko.observable( data.min);
    this.max = ko.observable( data.max);
    this.current = ko.observable( data.current);

    this.isEditText = function(){
        return data.type=="text";
    };
    this.isDatetime = function(){
        return data.type=="datetime";
    };
    this.isCheckBox = function(){
        return data.type=="check";
    };
    this.isDropdown = function(){
        return data.type=="dropdown";
    };
    this.isUploader = function(){
        return data.type=="file";
    };
    this.isSpinner = function(){
        return false;// data.type=="spinner";
    };

}

function ArgumentBinderModel() {
    // Data
    var self = this;
    self.tasks = ko.observableArray([]);
    self.save = function(){
        self.lastSavedJson(JSON.stringify(ko.toJS(self.tasks), null, 2));
    }
    self.getMinifiedJson = function(){
        var newArg = [];
        //console.log(self.tasks());
        for(var i=0;i<self.tasks().length;i++){
            var item={};
            item["name"]= self.tasks()[i].name();
            item["value"]= self.tasks()[i].value();
            console.log("NAME::"+item["name"]);
            newArg.push(item);
        }
        console.log("Created JSON::");
        console.log(newArg);
    }
    self.lastSavedJson = ko.observable("")
    self.renderedHandler =  function (elements, index, data) {
        if ($('#containerId').children().length === this.myItems().length) {
            // Only now execute handler
            console.log("=============================================");
        }
    }
    self.postRenderHandler = function(elements, obj){
        //console.log("=============================================");
        //console.log(obj);
        if(obj.isDropdown()){
            ArgumentLoader.initDropdown();
        }else if(obj.isDatetime()){
            ArgumentLoader.initDateTimePicker();
        }else if(obj.isCheckBox()){
            //ArgumentLoader.initCheckBox();
        }else if(obj.isSpinner()){
            //ArgumentLoader.initSpinner(obj.name(), obj.min(), obj.max(), obj.current());
        }
    }

}

var tlvm = new ArgumentBinderModel();
ko.applyBindings(tlvm);

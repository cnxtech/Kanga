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

var myObservableArray = [];    // Initially an empty array

// DATA BINDING MODEL
function ArgumentModel(data) {
    if (data.is_mandatory) data.is_mandatory = '<font color=red>(*)</font>';
    else data.is_mandatory = '';
    this.is_mandatory = ko.observable(data.is_mandatory);
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
    this.isEditTextArea = function(){
        return data.type=="textarea";
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
        for(var i=0;i<self.tasks().length;i++){
            var item={};
            item["name"]= self.tasks()[i].name();
            item["value"]= self.tasks()[i].value();
//            console.log("NAME::"+item["name"]);
//            console.log("VALUE::"+item["value"]);
            newArg.push(item);
        }
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
        } else if (obj.isEditTextArea()) {
            var editors = ace.edit("aceEditor");
            editors.setTheme("ace/theme/crimson_editor");
            editors.getSession().setMode("ace/mode/javascript");
            editors.setValue(obj.value(),-1);

            editors.getSession().on('change',function(){
                var ob = obj;
                ob.value(editors.getValue());
            });
        }

    }
}
function ButtonBinderModel() {
    // Data
    var self = this;
    self.validateButton = ko.observable("1. Validate");
    self.launchButton = ko.observable("2. Launch");
    self.remotelaunchButton = ko.observable("3. Remote Launch");
    self.successValidateButton = function() {
        self.validateButton('1. Re-Validate');
    };
    self.failureValidateButton = function() {
        self.validateButton('1. Validate - failed');
    };
    self.resetValidateButton = function() {
        self.validateButton('1. Validate');
    };
    self.successLaunchButton = function() {
        self.launchButton('2. Re-Launch');
    };
    self.failureLaunchButton = function() {
        self.launchButton('2. Launch - failed');

    };
    self.resetLaunchButton = function() {
        self.launchButton('2. Launch');
    };

}
var Row = function(row, dt) {
    this.row = ko.observable(row);
};
ko.observableArray.fn.subscribeArrayChanged = function(addCallback) {
    //console.log(addCallback);
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

var tlvm = new ArgumentBinderModel();
var bvm = new ButtonBinderModel();
ko.applyBindings(tlvm,document.getElementById("myModal"));
ko.applyBindings(bvm,document.getElementById("myLaunchButton"));


function reset(){
    $("#tab-2").html("<div class='animated fadeInRight'><pre>There are currently no logs to visualize.</pre></div>");
    $("#tab-3").html("<div class='animated fadeInRight'><pre>There are currently no logs to visualize.</pre></div>");
    $("#tab-4").html("<div class='animated fadeInRight'><pre>There are currently no logs to visualize.</pre></div>");
    $("#tab-5").html("<div class='animated fadeInRight'><pre>There are currently no logs to visualize.</pre></div>");
    activaTab("tab-1");
    bvm.resetValidateButton();
    bvm.resetLaunchButton();
}

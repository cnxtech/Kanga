var assert = require('assert');
var kangaBase = '../';
var tableField = require(kangaBase + 'nodes/filter/table');
var kangaLogger = require(kangaBase + 'utils/kanga-logger');
var klogger = kangaLogger('KangaTopology1', 'error');

// Construct test object
var obj = {};
obj.field_name = 'name,age';
obj.field_type = 'string,num';
obj.klogger = klogger;
obj.event = '{"root":{"_header_":{"log":"","type":0,"timestamp":1455163028,"name":"employee"},"employee":{"name":"Mike","email":"Mike@samsung.com", "gender":"man"}}}';
var tableFieldObject = new tableField(obj);

// Test DATA event
var output_data = tableFieldObject.execute(JSON.parse(obj.event.toString()));
var expect_data = '{"root":{"_header_":{"log":"","type":0,"timestamp":1455163028,"name":"employee"},"employee":{"name":"Mike","age":0}}}';

//Test COLLECTION event
obj.event = '{"root":{"_header_":{"log":"","name":"persons","type":1,"timestamp":1455163028},"persons":[{"name":"jack","email":"jack@samsung.com"},{"name":"john","email":"john@samsung.com"}]}}';
var output_collection = tableFieldObject.execute(JSON.parse(obj.event.toString()));
var expect_collection = null;

//Test TIME_TICK event
obj.event = '{"root":{"_header_":{"log":"","type":2,"timestamp":1455163028,"name":"employee"},"employee":{"name":"Mike","email":"Mike@samsung.com","gender":"man"}}}';
var output_tick = tableFieldObject.execute(JSON.parse(obj.event.toString()));
var expect_tick = null;

//Test EOF event
obj.event = '{"root":{"_header_":{"log":"","type":3,"timestamp":1455163028,"name":"employee"},"employee":{"name":"Mike","email":"Mike@samsung.com","gender":"man"}}}';
var output_eof = tableFieldObject.execute(JSON.parse(obj.event.toString()));
var expect_eof = '{"root":{"_header_":{"log":"","type":3,"timestamp":1455163028,"name":"employee"},"employee":{"name":"Mike","email":"Mike@samsung.com","gender":"man"}}}';

//Test SYSTEM_LOG event
obj.event = '{"root":{"_header_":{"log":"","type":4,"timestamp":1455163028,"name":"employee"},"employee":{"name":"Mike","email":"Mike@samsung.com","gender":"man"}}}';
var output_log = tableFieldObject.execute(JSON.parse(obj.event.toString()));
var expect_log = '{"root":{"_header_":{"log":"","type":4,"timestamp":1455163028,"name":"employee"},"employee":{"name":"Mike","email":"Mike@samsung.com","gender":"man"}}}';

//Test other type event
obj.event = '{"root":{"_header_":{"log":"","type":5,"timestamp":1455163028,"name":"person"},"person":{"name":"Mike","gender":"male","email":"Mike@samsung.com"}}}';
var output_other = tableFieldObject.execute(JSON.parse(obj.event.toString()));
var expect_other = null;

// Execute the test case
describe("table", function () {
    it("data: table passed", function (done) {
        assert.equal(JSON.stringify(output_data), expect_data);
        done();
    });

    it("collection: table passed", function (done) {
        assert.equal(output_collection, expect_collection);
        done();
    });

    it("tick: table passed", function (done) {
        assert.equal(output_tick, expect_tick);
        done();
    });

    it("eof: table passed", function (done) {
        assert.equal(JSON.stringify(output_eof), expect_eof);
        done();
    });

    it("system log: table passed", function (done) {
        assert.equal(JSON.stringify(output_log), expect_log);
        done();
    });

    it("other: table passed", function (done) {
        assert.equal(output_other, expect_other);
        done();
    });
});

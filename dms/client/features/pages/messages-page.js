var BulkSMSModal = function () {
    this.recipient = element(by.css('.recipient .selectize-input input'));
    this.message = element(by.id('message'));
    this.notification = element(by.css('.sms-toast .growl-item .growl-message'));
    this.sendMessagesButton = element(by.id('send-sms-btn'));

    this.enterRecipientNumber = function (number) {
        return this.recipient.sendKeys(number)
    };

    this.getRecipientsFieldErrors = function (index) {
        return element.all(by.css('#recipient-errors .text-danger')).get(index).getText();
    };

    this.getTextMessageErrors = function (index) {
        return element.all(by.css('#message-errors .text-danger ')).get(index).getText();
    };
};

var MessagesPage = function () {
    var request = require('request');

    this.bulkSMSButton = element(by.id('send-bulk-sms'));

    this.messages = [
        { phone: "023020302", time: "2014-02-13T02:00:00", relayer: 2, run: '1', text: "Where are yout",
            source: "NECOC Volunteer" }
    ];

    this.formattedTime = 'Feb 13, 2014 - 2:00AM';

    this.senderLocation = { "name": "Kampala", "type": "district"};

    this.NecocVolunteer = { "name": "ayoyo", "phone": this.messages[0].phone, "email": "haha@ha.ha"};

    this.actionsButton = element(by.id('actions-btn'));

    this.associateToDisasterButton = element(by.id('add-to-disaster'));

    this.addToDisasterButton = element(by.id('add-to-disaster-btn'));

    this.associatedStatus =  element(by.css('.status .label-success'));

    this.bulkSMSModal = new BulkSMSModal();

    this.addToDisasterModalTitle = element(by.id('add-to-disaster-modal-title'));

    this.checkMessage = function () {
        return element(by.css('input[type="checkbox"]')).click();
    };

    this.postMessage = function (callback) {
        request.post('http://localhost:7999/api/v1/rapid-pro/', {form: this.messages[0]}, function () {
            callback();
        })
    };


    this.postMessages = function (number, next) {
        var index = 0;
        postInIntervals();

        function postInIntervals() {
            var message = { phone: "023020302" + index, time: "2014-02-13T02:00:00", relayer: 2, run: String(index),
                text: "I am message" + index, source: "NECOC Volunteer" };

            setTimeout(function () {
                if (index < number) {
                    request.post('http://localhost:7999/api/v1/rapid-pro/', {form: message});
                    index++;
                    postInIntervals();
                } else {
                    next();
                }
            }, 400);
        }
    };

    this.numberOfMessages = function () {
        return element.all(by.repeater("message in messages")).count();
    };

    this.getMessageData = function (name, row) {
        return element(by.repeater('message in messages').row(row).column('{[{ message.' + name + ' }]}')).getText();
    };

    this.clickSecondPagination = function (callback) {
        element(by.repeater("page in showPages").row(1).column('{[{ page }]}')).click();
    };

    this.postLocation = function (callback) {
        request.post('http://localhost:7999/api/v1/locations/', {form: this.senderLocation}, function () {
            callback();
        });
    };

    this.selectLocation = function (location) {
        return element(by.css('.page-actions .selectize-input')).click().then(function () {
            browser.sleep(200);
            return element(by.cssContainingText('.selectize-dropdown-content .option', location)).click()
        });
    };

    this.postMobileUser = function (callback) {
        var necocVolunteer = this.NecocVolunteer;
        request.get('http://localhost:7999/api/v1/locations/?format=json', function (error, response, location) {
            necocVolunteer["location"] = JSON.parse(location)[0].id;
            request.post('http://localhost:7999/api/v1/mobile-users/', {form: necocVolunteer}, function () {
                callback();
            });
        });
    };

    this.registerDisaster = function (location, callback) {
        request.post('http://localhost:7999/api/v1/locations/', {
            form: {
                name: location,
                type: "district"
            }
        }, function (err, httpResponse, location) {
            request.post('http://localhost:7999/api/v1/disaster-types/', {
                form: {
                    name: "Flood"
                }
            }, function (err, httpResponse, disasterType) {
                request.post('http://localhost:7999/api/v1/disasters/', {
                    form: {
                        name: JSON.parse(disasterType).id,
                        status: "Assessment",
                        location: JSON.parse(location).id,
                        date: "2014-10-02T19:08:00",
                        description: "Flood"
                    }
                }, callback);
            });
        });
    };

    this.selectDisasterBy = function (location) {
        return element(by.css('.add-to-disaster .selectize-input')).click().then(function () {
            browser.sleep(200);
            return element(by.cssContainingText('.selectize-dropdown-content .caption   ', location)).click()
        });
    }

    this.getAddToDisasterErrors =  function () {
        return element(by.css("#disaster-errors .text-danger")).getText();
    }
};

module.exports = new MessagesPage();
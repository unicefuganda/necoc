module.exports = function () {
    var messagesPage = require("../pages/messages-page"),
        homePage = require("../pages/home-page"),
        dataSetupPage = require("../pages/data-setup-page"),
        moment = require('moment'),
        disasterLocation = null,
        numberOfMassMessages = 20,
        messages = [];

    this.Before(function (next) {
        messages = [];
        next();
    });

    this.World = require("../support/world").World;

    this.When(/^I POST a message to the NECOC DMS$/, function (next) {
        dataSetupPage.postFullMessage(messagesPage.messages[0], function (message) {
            messages.push(message);
            next();
        });
    });

    this.When(/^I POST "([^"]*)" to the NECOC DMS$/, function (text, next) {
        dataSetupPage.postMessage({
            text: text
        }, function (message) {
            messages.push(message);
            next();
        });
    });

    this.When(/^I visit the messages listing page$/, function (next) {
        browser.setLocation('/admin/messages');
        next();
    });

    this.Then(/^I should see my messages$/, function (next) {
        should_see_my_messages(this, next);
    });

    var should_see_my_messages = function (self, next, location, index, numberOfMessages, messageIndex) {
        var _index = index || 0;
        var _numberOfMessages = numberOfMessages || 1;
        var message = messages[ messageIndex || _index];
        messagesPage.numberOfMessages()
            .then(function (noOfMessages) {
                self.expect(noOfMessages).to.equal(_numberOfMessages);
            })
            .then(function () {
                self.expect(messagesPage.getMessageData('text', _index)).to.eventually.equal(message.text);
            })
            .then(function () {
                self.expect(messagesPage.getMessageData('time | date:"MMM dd, yyyy - h:mma"', _index)).to.eventually.equal(message.formattedTime);
            })
            .then(function () {
                self.expect(messagesPage.getMessageData('location', _index)).to.eventually.equal(location || messagesPage.senderLocation.name);
            })
            .then(function () {
                self.expect(messagesPage.getMessageData('source', _index)).to.eventually.equal(message.source + ' (' + message.phone + ')')
                    .and.notify(next);
            })
    };

    this.When(/^I POST a list of messages to NECOC DMS$/, function (next) {
        dataSetupPage.postMessages(numberOfMassMessages, function (postMessages) {
            messages.concat(postMessages);
            next();
        });
    });

    this.Then(/^I should see (\d+) messages in the first pagination$/, function (paginationLimit, next) {
        this.expect(messagesPage.numberOfMessages()).to.eventually.equal(parseInt(paginationLimit))
            .and.notify(next);
    });

    this.When(/^I click on the second pagination$/, function (next) {
        messagesPage.clickSecondPagination();
        next();
    });

    this.Then(/^I should see (\d+) messages in the second pagination$/, function (numberOfMessages, next) {
        this.expect(messagesPage.numberOfMessages()).to.eventually.equal(parseInt(numberOfMessages))
            .and.notify(next);
    });

    this.Given(/^I have one Necoc Volunteer registered$/, function (next) {
        dataSetupPage.postMobileUser(next);
    });

    this.When(/^I select my location as "([^"]*)"$/, function (district, next) {
        messagesPage.selectLocation(district).then(next);
    });

    this.Then(/^I should only see my message in "([^"]*)"$/, function (location, next) {
        should_see_my_messages(this, next, location);
    });

    this.Then(/^I should see my message with location "([^"]*)"$/, function (location, next) {
        should_see_my_messages(this, next, location);
    });

    this.Given(/^I visit the dashboard$/, function (next) {
        browser.get('/');
        next();
    });

    this.Given(/^I click send bulk sms button$/, function (next) {
        messagesPage.bulkSMSButton.click().then(function () {
            browser.sleep(500);
            next();
        });
    });

    this.Given(/^I enter a sender number as "([^"]*)"$/, function (number, next) {
        messagesPage.bulkSMSModal.enterRecipientNumber(number).then(next);
    });

    this.Given(/^I enter the message as "([^"]*)"$/, function (message, next) {
        messagesPage.bulkSMSModal.message.sendKeys(message).then(next);
    });

    this.Then(/^I should see message successfully sent$/, function (next) {
        var self = this;
        self.ignoreSync(true);

        browser.wait(messagesPage.bulkSMSModal.notification.getText).then(function (text) {
            self.expect(text).to.equal('Message successfully sent');
            next();
        });
    });

    this.Given(/^I click the send button$/, function (next) {
        messagesPage.bulkSMSModal.sendMessagesButton.click().then(function () {
            browser.sleep(500);
            next();
        });
    });

    this.Then(/^I should see the sms fields required error messages$/, function (next) {
        var self = this;

        messagesPage.bulkSMSModal.getRecipientsFieldErrors(0)
            .then(function (error) {
                self.expect(error).to.be.equal('This field is required');
            })
            .then(function () {
                self.expect(messagesPage.bulkSMSModal.getTextMessageErrors(0)).to
                    .eventually.be.equal('This field is required').and.notify(next);
            });
    });

    this.Then(/^I enter a more than (\d+) characters message$/, function (arg1, next) {
        var message = Array(parseInt(arg1) + 2).join("a");
        messagesPage.bulkSMSModal.message.sendKeys(message).then(next);
    });

    this.Then(/^I should not see the fields required error messages$/, function (next) {
        var self = this;

        messagesPage.bulkSMSModal.getRecipientsFieldErrors(0)
            .then(function (error) {
                self.expect(error).to.be.empty;
            })
            .then(function () {
                self.expect(messagesPage.bulkSMSModal.getTextMessageErrors(0)).to
                    .eventually.be.empty.and.notify(next);
            });
    });

    this.Then(/^I should see please enter not more that (\d+) characters$/, function (arg1, next) {
        this.expect(messagesPage.bulkSMSModal.getTextMessageErrors(1)).to.eventually.be.equal('Please enter not more that 160 characters').and.notify(next);
    });

    this.When(/^I check the message$/, function (next) {
        messagesPage.checkMessage().then(next);
    });

    this.When(/^I check message (\d+)$/, function (index, next) {
        messagesPage.checkMessageByIndex(index - 1).then(next);
    });

    this.When(/^I click on associate to disaster button$/, function (next) {
        messagesPage.actionsButton.click().then(function () {
            return messagesPage.associateToDisasterButton.click();
        }).then(function () {
            browser.sleep(500);
            next();
        });
    });

    this.When(/^I search disaster by location$/, function (next) {
        messagesPage.selectDisasterBy(disasterLocation).then(next);
    });

    this.Then(/^I should see the message associated with the disaster$/, function (next) {

        this.expect(messagesPage.associatedStatus.isDisplayed()).to.eventually.be.true
            .and.notify(next);
    });

    this.When(/^I click the add button$/, function (next) {
        messagesPage.addToDisasterButton.click().then(function () {
            browser.sleep(500);
            next();
        });
    });

    this.Given(/^I have a "([^"]*)" disaster in "([^"]*)" district, "([^"]*)" subcounty already registered$/,
        function (disaster, district, subcounty, next) {
            disasterLocation = district;
            dataSetupPage.registerDisaster(disaster, district, subcounty, next);
        }
    );

    this.Then(/^I should see field required error message$/, function (next) {
        this.expect(messagesPage.getAddToDisasterErrors()).to
            .eventually.be.equal('This field is required').and.notify(next);
    });

    this.Then(/^the error message disappear$/, function (next) {
        this.expect(messagesPage.getAddToDisasterErrors()).to
            .eventually.be.equal('').and.notify(next);
    });

    this.When(/^I click on actions button$/, function (next) {
        messagesPage.actionsButton.click().then(next);
    });

    this.Then(/^I should not see the associate to disaster button$/, function (next) {
        this.expect(messagesPage.associateToDisasterButton.isDisplayed()).to.eventually.be.false.and.notify(next);
    });

    this.Given(/^I navigate to messages page$/, function (next) {
        homePage.messagesTab.click().then(next);
    });

    this.Then(/I should see (.*) uncategorized message on the admin panel/, function (count, next) {
        browser.driver.navigate().refresh();
        this.expect(messagesPage.getTextByCss('.nav-sidebar .badge')).to
            .eventually.be.equal(count.toString()).and.notify(next);
    });

    this.Then(/^I should see the total number of messages displayed$/, function (next) {
        browser.driver.navigate().refresh();
        this.expect(messagesPage.getTextByCss('.section .sub-section-header .badge')).to
            .eventually.be.equal(numberOfMassMessages.toString());

        this.expect(messagesPage.getTextByCss('.nav-sidebar .badge')).to
            .eventually.be.equal(numberOfMassMessages.toString()).and.notify(next);
    });

    this.Then(/^I should see one message uncategorized$/, function (next) {
        this.expect(messagesPage.getTextByCss('#uncategorized-sms .huge-number')).to
            .eventually.be.equal('1').and.notify(next);
    });

    this.Then(/^I should see zero message uncategorized$/, function (next) {
        browser.driver.navigate().refresh();
        this.expect(messagesPage.getTextByCss('#uncategorized-sms .huge-number')).to
            .eventually.be.equal('0').and.notify(next);
    });

    this.Then(/^I should see (\d+) message$/, function (number, next) {
        var self = this;
        messagesPage.numberOfMessages()
            .then(function (noOfMessages) {
                self.expect(noOfMessages).to.equal(parseInt(number));
            })
            .then(next);
    });

    this.When(/^I refresh my messages$/, function (next) {
        messagesPage.refreshButton.click().then(next);
    });

    this.Then(/^I should see the (\d+) messages in "([^"]*)" ordered$/, function (numberOfRows, location, next) {
        for (index = 0; index < numberOfRows; index++) {
            should_see_my_messages(this, next, location, index, parseInt(numberOfRows), numberOfRows - index - 1);
        }
        ;
    });

    this.Given(/^I POST "([^"]*)" at "([^"]*)" to the NECOC DMS$/, function (text, time, next) {
        dataSetupPage.postMessage({
            text: text,
            time: time
        }, function (message) {
            var format = 'MMM DD, YYYY - h:mmA';
            message.formattedTime = moment(message.time).format(format);
            messages.push(message);
            next();
        });
    });

    this.Given(/^I have the following messages in the NECOC DMS:$/, function (table, next) {
        table.hashes().map(function (row) {
            dataSetupPage.postMessage(row, function (message) {
                var format = 'MMM DD, YYYY - h:mmA';
                message.formattedTime = moment(message.time).format(format);
                messages.push(message);
            });
        });
        browser.sleep(3000).then(function () {
            next();
        })
    });

    this.When(/^I sort by "([^"]*)" ascending$/, function (sortKey, next) {
        browser.refresh().then(function () {
            element(by.cssContainingText(".sort", "Date Time")).click().then(function () {
                element(by.cssContainingText(".sort", sortKey)).click().then(next);
            })
        });
    });

    this.When(/^I sort by "([^"]*)" descending$/, function (sortKey, next) {
        browser.refresh().then(function () {
            element(by.cssContainingText(".sort", "Date Time")).click().then(function () {
                element(by.cssContainingText(".sort", sortKey)).click().then(function () {
                    element(by.cssContainingText(".sort", sortKey)).click().then(next);
                })
            })
        });
    });

    this.Then(/^I should see the messages in the following order:$/, function (table, next) {
        var self = this;
        table.hashes().forEach(function (message, index) {
            self.expect(messagesPage.getMessageData('text', index)).to.eventually.equal(message.text);
        });
        browser.sleep(1000).then(function () {
            next();
        })
    });
};
module.exports = function () {
    var messagesPage = require("../pages/messages-page"),
        homePage = require("../pages/home-page"),
        disasterLocation = null,
        numberOfMassMessages = 15;

    this.World = require("../support/world").World;

    this.Given(/^I am logged in as a NECOC admin$/, function (next) {
        browser.get('/');
        next();
    });

    this.When(/^I POST a message to the NECOC DMS$/, function (next) {
        messagesPage.postMessage(next);
    });

    this.When(/^I visit the messages listing page$/, function (next) {
        browser.setLocation('/admin/messages');
        next();
    });

    this.Then(/^I should see my messages$/, function (next) {
        should_see_my_messages(this, next);
    });

    var should_see_my_messages = function (self, next, district) {
        messagesPage.numberOfMessages()
            .then(function (noOfMessages) {
                self.expect(noOfMessages).to.equal(1);
            })
            .then(function () {
                self.expect(messagesPage.getMessageData('text', 0)).to.eventually.equal(messagesPage.messages[0].text);
            })
            .then(function () {
                self.expect(messagesPage.getMessageData('time | date:"MMM dd, yyyy - h:mma"', 0)).to.eventually.equal(messagesPage.formattedTime);
            })
            .then(function () {
                self.expect(messagesPage.getMessageData('location', 0)).to.eventually.equal(district || messagesPage.senderLocation.name);
            })
            .then(function () {
                self.expect(messagesPage.getMessageData('source', 0)).to.eventually.equal(messagesPage.messages[0].source + ' (' + messagesPage.messages[0].phone + ')')
                    .and.notify(next);
            })
    };

    this.When(/^I POST a list of messages to NECOC DMS$/, function (next) {
        messagesPage.postMessages(numberOfMassMessages, next);
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
        messagesPage.postMobileUser(next);
    });

    this.When(/^I select my location as "([^"]*)"$/, function (district, next) {
        messagesPage.selectLocation(district).then(next);
    });

    this.Then(/^I should only see my message in "([^"]*)"$/, function (location, next) {
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

    this.When(/^I have a disaster in "([^"]*)" registered$/, function (location, next) {
        disasterLocation = location;
        messagesPage.registerDisaster(location, next);
    });

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

};
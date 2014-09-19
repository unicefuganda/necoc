var myAfterHooks = function () {
  this.registerHandler('AfterFeatures', function (event, callback) {
      this.driver.close();
      callback();
  });
};

module.exports = myAfterHooks;
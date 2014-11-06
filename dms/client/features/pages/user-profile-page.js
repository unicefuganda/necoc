var UserProfilePage = function () {
    this.element_by_ng_binding = function(binding){
        return element(by.binding(binding)).getText();
    };
};

module.exports = new UserProfilePage();
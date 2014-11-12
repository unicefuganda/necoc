Feature: Mobile User

  Scenario: Create Mobile User
    Given I have no users
    And I am logged in as a NECOC admin
    And I have "Mukono" district and "Nabbaale" subcounty already registered
    When I navigate to the users page
    And I click the create new user button
    And I enter my "name" as "Solomon"
    And I enter my "email" as "solomon@gmail.com"
    And I enter my "phone" as "0775019449"
    And I select my "district" as "Mukono"
    And I select my "subcounty" as "Nabbaale"
    And I click  save and close
    Then I should see my details in mobile users table in row 1

  Scenario: Create Mobile User -- Validation
    Given I am logged in as a NECOC admin
    And I have "Mukono" district and "Nabbaale" subcounty already registered
    When I navigate to the users page
    And I click the create new user button
    And I click the save button
    Then I should see fields required error messages
    When I have a Mobile User with email "solomon@gmail.com" and phone "0775019449"
    And I enter my "name" as "Ayoyo"
    And I enter my "email" as "solomon@gmail.com"
    And I enter my "phone" as "0775019449"
    And I select my "district" as "Mukono"
    And I select my "subcounty" as "Nabbaale"
    And I choose to grant web access
    And I enter my "username" as "test_user"
    Then I should not see the field required error messages
    When I click the save button
    Then I should see other server-side validation errors

  Scenario: Create System User
    Given I have no users
    And I am logged in as a NECOC admin
    And I have "Mukono" district and "Nabbaale" subcounty already registered
    When I navigate to the users page
    And I click the create new user button
    And I enter my "name" as "Solomon"
    And I enter my "email" as "solomon@gmail.com"
    And I enter my "phone" as "0775019449"
    And I select my "district" as "Mukono"
    And I select my "subcounty" as "Nabbaale"
    And I choose to grant web access
    And I enter my "username" as "solomon1990"
    And I click  save and close
    Then I should see my details in mobile users table in row 1
    When I click "Solomon" in the mobile users table
    Then I should see my details in the profile page
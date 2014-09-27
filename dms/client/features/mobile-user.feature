Feature: Mobile User

  Scenario: Create Mobile User
    Given I am logged in as a NECOC admin
    When I navigate to the Admin Panel
    And I have "Mukono" district already registered
    And I click the create new user button
    And I enter my "name" as "Solomon"
    And I enter my "email" as "solomon@gmail.com"
    And I enter my "phone" as "0775019449"
    And I select my "district" as "Mukono"
    And I click  save and close
    Then I should see my details in mobile users table

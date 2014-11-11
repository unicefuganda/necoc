Feature: User Profile

  Scenario: Edit User Profile
    Given I have no users
    And I am logged in as a NECOC admin
    And I have "Mukono" district and "Nabbaale" subcounty already registered
    When I navigate to the users page
    And I click "Test User" in the mobile users table
    And I edit the user
    And I update my "name" as "Solomon"
    And I update my "email" as "solomon@gmail.com"
    And I update my "phone" as "0775019449"
    And I update by selecting my "district" as "Mukono"
    And I update by selecting my "subcounty" as "Nabbaale"
    And I save the updated user details
    Then I should see my updated profile
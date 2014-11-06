Feature: User Profile

  Scenario: View profile
    Given I am logged in as a NECOC admin
    When I click on my profile link
    Then I should see my profile

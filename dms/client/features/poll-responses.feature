Feature: Poll Response

  Scenario: View poll responses
    Given I am logged in as a NECOC admin
    And I have a poll and response with keyword "haha" in "Kampala"
    And I visit the poll responses listing page
    Then I should see my poll response
    When I navigate to "/admin/polls"
    And I click the poll in "Mukono"
    Then I should see the associated poll responses
    When I click the poll page back button
    Then I should see the poll listing page


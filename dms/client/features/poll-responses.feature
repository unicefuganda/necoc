Feature: Poll Response

  Scenario: View poll responses
    Given I am logged in as a NECOC admin
    And I have a poll and response with keyword "haha" in "Mukono"
    And I have a Mobile User with email "email@email.email" and phone "234567"
    When I navigate to "/admin/polls"
    And I click the poll in "Mukono"
    Then I should see the associated poll responses
    When I click the poll page back button
    Then I should see the poll listing page

  Scenario: Export poll responses
    Given I am logged in as a NECOC admin
    And I have a poll and response with keyword "haha" in "Mukono"
    And I have a Mobile User with email "email@email.email" and phone "234567"
    When I navigate to "/admin/polls"
    And I click the poll in "Mukono"
    Then I should see the export poll button

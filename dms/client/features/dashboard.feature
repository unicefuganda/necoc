Feature: Dashboard

  Scenario: Show messages on the message panel
    Given I am logged in as a NECOC admin
    And I have "Kampala" district already registered
    And I POST a message to the NECOC DMS
    When I navigate to map location "/admin/dashboard"
    And I click the messages panel chevron
    Then I should see my messages

  Scenario: Show filtered messages by district on the message panel
    Given I am logged in as a NECOC admin
    And I have "Gulu" district already registered
    And I have "Kampala" district already registered
    And I POST "NECOC Gulu water everywhere" to the NECOC DMS
    And I POST "NECOC Kampala there are mosquitoes here" to the NECOC DMS
    When I navigate to map location "/admin/dashboard/gulu"
    And I click the messages panel chevron
    Then I should only see my message in "Gulu"

  Scenario: Show filtered messages by subcounty on the message panel
    Given I am logged in as a NECOC admin
    And I have "Gulu" district and "Awach" subcounty already registered
    And I have "Kampala" district already registered
    And I POST "NECOC Awach water everywhere" to the NECOC DMS
    And I POST "NECOC Kampala there are mosquitoes here" to the NECOC DMS
    When I navigate to map location "/admin/dashboard/gulu/awach"
    And I click the messages panel chevron
    Then I should see my message with location "Gulu >> Awach"
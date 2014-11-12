Feature: Dashboard

  Scenario: Show messages on the message panel
    Given I am logged in as a NECOC admin
    And I have "Kampala" district already registered
    And I POST "NECOC Kampala Fire" to the NECOC DMS
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

  Scenario: Show map options on dashboard and Hide on other tabs.
    Given I am logged in as a NECOC admin
    Then I should see map options panel on dashboard
    When I navigate to "/admin/disasters"
    Then I should not see map options panel

  Scenario: Apply time filters to map and sliding panel
    Given I am logged in as a NECOC admin
    And I have a "Flood" disaster in "Gulu" district, "Awach" subcounty already registered
    And I POST "NECOC Awach Flood here" to the NECOC DMS
    And I navigate to map location "/admin/dashboard"
    Then I see should see 1 disasters bubble on the map
    When I navigate to map location "/admin/dashboard/gulu"
    Then I should see a message cluster marker with 1 incoming messages
    Then I should see a disaster cluster marker with 1 disasters
    Then I should see "gulu" district with layer color "#E31A1C"
    And I click the messages panel chevron
    Then I should see my message with location "Gulu >> Awach"
    When I enter a from date filter as "2014-01-06"
    And I enter a to date filter as "2014-02-06"
    Then I should not see a message cluster marker
    Then I should not see a disaster cluster marker
    Then I should see "gulu" district with layer color "#FFEDA0"
    And I click the messages panel chevron
    Then I should see 0 message

  Scenario: Apply disaster filter to map and sliding panel
    Given I am logged in as a NECOC admin
    And I have a "Flood" disaster in "Gulu" district, "Awach" subcounty already registered
    And I POST "NECOC Awach Flood here" to the NECOC DMS
    And I navigate to map location "/admin/dashboard"
    Then I see should see 1 disasters bubble on the map
    When I enter the disaster type as "Fire"
    Then I see should see 0 disasters bubble on the map
    When I navigate to map location "/admin/dashboard/gulu"
    Then I should see a message cluster marker with 1 incoming messages
    Then I should see a disaster cluster marker with 1 disasters
    Then I should see "gulu" district with layer color "#E31A1C"
    And I click the messages panel chevron
    Then I should see my message with location "Gulu >> Awach"
    When I select the disaster type as "Fire"
    Then I should not see a message cluster marker
    Then I should not see a disaster cluster marker
    Then I should see "gulu" district with layer color "#FFEDA0"
    And I click the messages panel chevron
    Then I should see 0 message


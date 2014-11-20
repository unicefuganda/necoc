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
    Then I should see "gulu" district with layer color "#ef2602"
    And I click the messages panel chevron
    Then I should see my message with location "Gulu >> Awach"
    When I enter a from date filter as "2014-01-06"
    And I enter a to date filter as "2014-02-06"
    Then I should not see a message cluster marker
    Then I should not see a disaster cluster marker
    Then I should see "gulu" district with layer color "#dfff67"
    And I click the messages panel chevron
    Then I should see 0 message

  Scenario: Apply disaster filter to map and sliding panel
    Given I am logged in as a NECOC admin
    And I have a "Flood" disaster in "Gulu" district, "Awach" subcounty already registered
    And I POST "NECOC Awach Flood here" to the NECOC DMS
    And I navigate to map location "/admin/dashboard"
    Then I see should see 1 disasters bubble on the map
    When I add the disaster type as "Fire"
    Then I see should see 0 disasters bubble on the map
    When I navigate to map location "/admin/dashboard/gulu"
    Then I should see a message cluster marker with 1 incoming messages
    Then I should see a disaster cluster marker with 1 disasters
    Then I should see "gulu" district with layer color "#ef2602"
    And I click the messages panel chevron
    Then I should see my message with location "Gulu >> Awach"
    When I select in the dashboard the disaster type as "Fire"
    Then I should not see a message cluster marker
    Then I should not see a disaster cluster marker
    Then I should see "gulu" district with layer color "#dfff67"
    And I click the messages panel chevron
    Then I should see 0 message

  Scenario: Show Uganda stats summary on sliding panel
    Given I am logged in as a NECOC admin
    And I have a "Fire" disaster in "Mukono" district, "goma" subcounty already registered
    When I navigate to map location "/admin/dashboard"
    And I click the stats summary panel chevron
    Then I should see the disaster stats

  Scenario: Show district stats summary on sliding panel
    Given I am logged in as a NECOC admin
    And I have a "Fire" disaster in "Mukono" district, "goma" subcounty already registered
    When I navigate to map location "/admin/dashboard/mukono"
    And I click the stats summary panel chevron
    Then I should see in "mukono" district the disaster stats

  Scenario: Show subcounty stats summary on sliding panel
    Given I am logged in as a NECOC admin
    And I have a "Fire" disaster in "Mukono" district, "goma" subcounty already registered
    When I navigate to map location "/admin/dashboard/mukono/goma"
    And I click the stats summary panel chevron
    Then I should see in goma the disaster stats

  Scenario: Show no disaster on sliding panel
    Given I am logged in as a NECOC admin
    And I have a "Fire" disaster in "Mukono" district, "goma" subcounty already registered
    When I have "Kampala" district already registered
    And I navigate to map location "/admin/dashboard/kampala"
    And I click the stats summary panel chevron
    Then I should see in "kampala" district zero disaster stats

  Scenario: Apply time filters to stats summary pannel
    Given I am logged in as a NECOC admin
    And I have a "Fire" disaster in "Mukono" district, "goma" subcounty already registered
    And I navigate to map location "/admin/dashboard/mukono"
    When I enter a from date filter as "2014-01-06"
    And I enter a to date filter as "2014-02-06"
    And I click the stats summary panel chevron
    Then I should see in "mukono" district zero disaster stats

  Scenario: Apply disaster type filter to stats summary pannel
    Given I am logged in as a NECOC admin
    And I have a "Flood" disaster in "Gulu" district, "Awach" subcounty already registered
    And I navigate to map location "/admin/dashboard/gulu"
    When I add the disaster type as "Fire"
    And I click the stats summary panel chevron
    Then I should see in "gulu" district zero disaster stats
    When I select in the dashboard the disaster type as "Flood"
    Then I should see in "gulu" district the disaster stats

Feature: Map

  Scenario: View Uganda Map
    Given I am logged in as a NECOC admin
    When I navigate to "/admin/dashboard"
    Then I should see a map of Uganda centered at latitude "1.436" and longitude "32.884"
    Then I should see a map of Uganda zoomed at level "7"

  Scenario: Highlight district
    Given I am logged in as a NECOC admin
    When I navigate to "/admin/dashboard"
    And hover over "Lira"
    Then "Lira" should be highlighted
    Then I should see map legend displayed

  Scenario: Zoom into districts on click
    Given I am logged in as a NECOC admin
    When I navigate to "/admin/dashboard"
    And I click "Lira" district
    Then I should see Uganda map zoomed into "Lira" district

  Scenario: Navigate to district
    Given I am logged in as a NECOC admin
    When I navigate to map location "/admin/dashboard/lira"
    Then I should see Uganda map zoomed into "Lira" district
    Then I should see the map title as "Uganda / Lira"

  Scenario: Navigate to subcounty
    Given I am logged in as a NECOC admin
    When I navigate to map location "/admin/dashboard/gulu"
    And I click "Awach" subcounty in "Gulu" district
    Then I should see the map title as "Uganda / Gulu / Awach"
    And the map zooms into "Awach"

  Scenario: View Messages and Disasters cluster markers on each Subcounty
    Given I am logged in as a NECOC admin
    And I have "Gulu" district and "Awach" subcounty already registered
    And I POST "NECOC Awach Flood" to the NECOC DMS
    When I navigate to map location "/admin/dashboard/gulu"
    Then I should see a message cluster marker with 1 incoming messages
    Then I should not see a disaster cluster marker

  Scenario: View Messages HeatMap
    Given I am logged in as a NECOC admin
    And I have "Lira" district already registered
    When I navigate to map location "/admin/dashboard"
    And I click "Lira" district
    Then I should see "lira" district with layer color "#dfff67"
    Given I am logged in as a NECOC admin
    And I have "Gulu" district and "Awach" subcounty already registered
    And I POST "NECOC Awach Fire" to the NECOC DMS
    When I navigate to map location "/admin/dashboard"
    And I click "Gulu" district
    Then I should see "gulu" district with layer color "#ef2602"

  Scenario: View Legend on the Map
    Given I am logged in as a NECOC admin
    And I have "Gulu" district and "Awach" subcounty already registered
    When I navigate to map location "/admin/dashboard"
    Then I should see map legend displayed
    Then I should see the legend title as "Messages"
    Then I should see the legend labels as "0,,1"
    When I POST "NECOC Awach Fire" to the NECOC DMS
    And I POST "NECOC Awach Fire is killing us" to the NECOC DMS
    And I POST "NECOC Awach There is a fire here" to the NECOC DMS
    And I POST "NECOC Awach Fire please" to the NECOC DMS
    And I navigate to map location "/admin/dashboard"
    Then I should see the legend labels as "0,2,4"

  Scenario: Search location on the map
    Given I am logged in as a NECOC admin
    When I navigate to map location "/admin/dashboard"
    And I search for "lira" district
    Then I should see Uganda map zoomed into "Lira" district
    When I clear the text I entered in the district field
    Then I should see a map of Uganda zoomed at level "7"

  Scenario: View Disasters Bubbles on the map
    Given I am logged in as a NECOC admin
    And I have a "Flood" disaster in "Gulu" district, "Awach" subcounty already registered
    When I navigate to map location "/admin/dashboard"
    Then I see should see 1 disasters bubble on the map
    When I click "Gulu" district
    Then I should see a disaster cluster marker with 1 disasters

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

  Scenario: Zoom into districts on click
    Given I am logged in as a NECOC admin
    When I navigate to "/admin/dashboard"
    And click "Lira" district
    Then I should see Uganda map zoomed into "Lira" district

  Scenario: Navigate to district
    Given I am logged in as a NECOC admin
    When I navigate to "/admin/dashboard/lira"
    Then I should see Uganda map zoomed into "Lira" district
    Then I should see the map title as "Uganda / Lira"

  Scenario: View Messages bubble
    Given I am logged in as a NECOC admin
    And I have "Lira" district already registered
    When I navigate to "/admin/dashboard/lira"
    Then I should see a messages bubble with 0 incoming messages

  Scenario: View Messages HeatMap
    Given I am logged in as a NECOC admin
    When I navigate to "/admin/dashboard/lira"
    Then I should see "lira" district with layer color "#FFEDA0"
    Given I am logged in as a NECOC admin
    When I have "Kampala" district already registered
    When I POST a message to the NECOC DMS
    And I navigate to "/admin/dashboard/kampala"
    Then I should see "kampala" district with layer color "#800026"

  Scenario: View Messages Legend
    Given I am logged in as a NECOC admin
    When I navigate to "/admin/dashboard"
    Then I should see map legend displayed


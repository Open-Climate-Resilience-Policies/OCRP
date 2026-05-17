Feature: View policy details
  In order to evaluate policy requirements and evidence
  As a site visitor
  I want to open a policy from the policy library and read its detail page

  Scenario: BDD-002 visitor can open a policy detail page from the policy library
    Given the policy site is available
    When the visitor opens the policy library
    And the visitor selects a listed policy
    Then the policy detail page is displayed
    And the page includes the policy title
    And the page provides a way back to the policy library


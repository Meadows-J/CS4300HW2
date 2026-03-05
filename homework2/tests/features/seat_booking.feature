Feature: Seat Booking
  As a user
  I want to book seats for a movie
  So that I can reserve my spot

  Scenario: Book an available seat
    Given I have selected a movie
    And there are available seats
    When I select an available seat
    And I confirm the booking
    Then the seat should be marked as booked
    And I should see a confirmation message
    And the booking should be created in the system

  Scenario: Cannot book an already booked seat
    Given I have selected a movie
    And there is a booked seat
    When I try to book the booked seat
    Then I should see an error message "This seat is already booked!"
    And the booking should not be created

  Scenario: View available seats
    Given I have selected a movie
    When I navigate to the seat selection page
    Then I should see all available seats
    And I should see the seat number
    And I should see the seat status

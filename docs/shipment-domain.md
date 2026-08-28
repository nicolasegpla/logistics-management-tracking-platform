# Shipment

## Context

`Shipment` is a domain entity that represents a shipment, including its states, behaviors, and the rules it must follow within the domain.

## Responsibility

It is responsible for managing its own state, validating behaviors that affect it, and ensuring that its business rules are respected.

## States

The `Shipment` entity has three available states:

* `CREATED`
* `IN_TRANSIT`
* `DELIVERED`

## Business Rules

* Every newly created `Shipment` must start with the `CREATED` status.
* The initial value of `delivery_date` must be `None`.
* A `Shipment` must respect its lifecycle and cannot skip steps.
* A `Shipment` in the `DELIVERED` state cannot transition back to a previous state.
* Every `Shipment` in the `DELIVERED` state must have a valid `datetime` value in `delivery_date`.

## Valid Transitions

* `CREATED -> IN_TRANSIT`
* `IN_TRANSIT -> DELIVERED`

## Invalid Transitions

* `CREATED -> DELIVERED`
* `IN_TRANSIT -> CREATED`
* `DELIVERED -> IN_TRANSIT`
* `DELIVERED -> CREATED`

## Testing

We created a total of 6 tests: 4 happy-path tests and 2 sad-path tests.

### Happy Path

* The first test validates that a new `Shipment` is created with the `CREATED` status.
* The second test validates that `shipment.delivery_date` starts as `None`.
* The third test validates that a `Shipment` can transition from `CREATED` to `IN_TRANSIT`.
* The fourth test validates that a `Shipment` can transition from `IN_TRANSIT` to `DELIVERED`, and that `delivery_date` is assigned a `datetime` instance when the shipment becomes `DELIVERED`.

### Sad Path

* Validates that a `Shipment` cannot skip its lifecycle and transition directly from `CREATED` to `DELIVERED`, and that its status remains `CREATED`.
* Validates that a `Shipment` cannot regress from `DELIVERED` to `IN_TRANSIT`, and that its status remains `DELIVERED` while `delivery_date` keeps its original `datetime` value.

The tests pass because we expect invalid operations to raise a `ValueError`.

## Design Decisions

### Enum

Initially, shipment states were represented using hardcoded or arbitrary values. This could create maintainability and consistency problems as the application grows, especially if state names need to change.

I replaced those values with an `Enum` that defines the allowed shipment states in one place.

This helps:

* prevent typos and arbitrary values;
* keep the allowed states explicit;
* provide a single source of truth;
* improve maintainability;
* improve consistency across the codebase.

## What I Learned

* `Given / When / Then` is a useful mental model for designing tests because it helps structure the initial state, the action being performed, and the expected result.
* An incomplete test suite can leave important behavior uncovered. For example, `test_shipment_can_move_from_created_to_in_transit` verifies that the status can change correctly, but without `test_shipment_cant_move_from_created_to_delivered`, the domain could still allow an invalid transition while the existing tests remain green. A green test suite only guarantees the behaviors that have actually been specified and tested.
* Domain invariants must be protected even when an operation fails. For example, if an invalid transition is attempted, the test should verify not only that an exception is raised, but also that the entity's data was not partially mutated and remains consistent.

## Domain Status

We currently have the first domain entity, `Shipment`, including its business rules, state-transition methods, and a unit test suite that validates the behaviors currently specified for the shipment lifecycle.

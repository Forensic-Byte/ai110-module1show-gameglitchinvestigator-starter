# AI Interactions

## Challenge 1: Edge-case test set

**Task prompt in this collaboration:** “Can you do that entire tab please.” I followed the course's Challenge 1 instructions to identify edge inputs and generate pytest cases; I did not send a separate, verbatim test-generation prompt.

| Edge case | Why it was included | Test coverage |
|---|---|---|
| Empty and whitespace-only input | A blank guess should show a useful validation message and not count as a turn. | `test_empty_guess_is_rejected`; UI validation tests |
| Decimal and malformed input | Converting a decimal with `int(float(...))` silently changes what the player entered. | `test_non_integer_guess_is_rejected` |
| Negative and extremely large integers | Both are valid Python integers but outside the current game's selectable range; they should not crash or consume an attempt. | `test_integer_edge_cases_parse_without_crashing`; `test_out_of_range_guess_does_not_consume_an_attempt` |

**Review and correction:** An early draft set the “clear guess” marker inside the shared reset helper. AppTest showed that changing difficulty then cleared the first guess on the next rerun. I moved that marker to the explicit New Game button and kept difficulty changes responsible for resetting only the newly selected game's state.

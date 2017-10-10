## Puffle

### What is this?

Puffle is a wrapper for running solidity tests in truffle on testrpc. Puffle runs each set of tests against a fresh instance of testrpc, such that modifications to your testrpc during your tests (like time) do not impact future tests in the same overall batch. (You can magic the testrpc blockchain forwards, but blockchains cannot go backwards!)

You may configure your paths and options in `site-packages/puffle/bin/puffle.json`.

### Contributing

Contributions are welcome!

#### TODO:
    - Add support for individual compilation.
    - Probably other stuff.
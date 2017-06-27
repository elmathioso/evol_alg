# evol_alg
List of evolutionary algorithms

This repository contains a few examples of basic evolutionary algorithms, mainly focused on string manipulation.

  * genalg: Basic example
  * DeBuijn_Morse: Debruijn sequence optimization using genetic algorithms 

## Considerations
The following should be taken in consideration when designing and tuning an algorithm:

### Initial seed

  * random
  * random position from list

### Mutation

  * switch spots (swap)
  * switch to random
  * add random
  * remove random
  * add/remove
  * elitism (no change of the best)

### Death

  * No death
  * Weakest death
  * Random death

### Reproduction

  * half and half
  * interlaced

### Constraints (optional)

  * unique genes/ all genes must be present (alphabet problem)

### Fitness

  * similarity to target
  * size

## References

  * [Evolutionary algorithms](https://en.wikipedia.org/wiki/Evolutionary_algorithm)
  * [Genetic algorithms](https://en.wikipedia.org/wiki/Genetic_algorithm)
  * [Debruijn sequence](https://en.wikipedia.org/wiki/De_Bruijn_sequence)
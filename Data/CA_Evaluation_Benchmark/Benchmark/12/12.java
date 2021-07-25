public static int[] primes(int number) {
    List<Integer> factors = new ArrayList<>();
    for(int factor = 2; factor <= number; factor++) {
        while (number % factor == 0) {
            factors.add(factor);
            number = number / factor;
        }
    }
    return factors.stream().mapToInt(n -> n.intValue()).toArray();
}
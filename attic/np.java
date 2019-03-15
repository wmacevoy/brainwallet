import java.math.*;
public class np {
    static final int ROUNDS = 40;
    static BigInteger bd(int bits, int delta) {
	return BigInteger.ONE.shiftLeft(bits).add(BigInteger.valueOf(delta));
    }
    static BigInteger [] PRIMES = new BigInteger[] {
	bd(127,-1),
	bd(128,-3),
        bd(160,-3),
        bd(192,-3),
        bd(224,-3),
        bd(256,-3)
    };

    public static BigInteger nextPrime(BigInteger x) {
	return x.nextProbablePrime();
    }
    public static BigInteger prevPrime(BigInteger x) {
	if (x.compareTo(BigInteger.valueOf(2)) <= 0) {
	    throw new UnsupportedOperationException("no previous");
	}
	do {
	    x = x.subtract(BigInteger.ONE);
	} while (!x.isProbablePrime(ROUNDS));
	return  x;
    }
    
    public static void testPrimes() {
	for (BigInteger p : PRIMES) {
	    System.out.println("" + p + " is prime: " + p.isProbablePrime(ROUNDS));
	}
    }
    public static void test() {
	BigInteger x = BigInteger.valueOf(1).shiftLeft(16);
	for (int i = 0; i<20; ++i) {
	    System.out.println(x);
	    x = nextPrime(x);
	}
	System.out.println("BACK");	
	for (int i = 0; i<20; ++i) {
	    System.out.println(x);
	    x = prevPrime(x);
	}
    }
    public static void main(String[] args) {
	testPrimes();
	test();
	System.out.println("BIGGER=[");
	for (int b=8; b<512; b += 8) {
	    BigInteger x=BigInteger.valueOf(1).shiftLeft(b);
	    BigInteger p = nextPrime(x).subtract(x);
	    System.out.print("," +b + ":2**" + b +"+" + p +"");
	}
	System.out.println("SMALLER=[");
	for (int b=8; b<512; b += 8) {
	    BigInteger x=BigInteger.valueOf(1).shiftLeft(b);
	    BigInteger q = prevPrime(x).subtract(x);
	    System.out.print("," +b + ":2**" + b + "" + q +")");
	}
    }
}
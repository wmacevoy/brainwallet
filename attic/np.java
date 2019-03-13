import java.math.*;
public class np {
    public static BigInteger nextPrime(BigInteger x) {
	return x.nextProbablePrime();
    }
    public static BigInteger prevPrime(BigInteger x) {
	BigInteger delta = BigInteger.valueOf((int) Math.floor(Math.log(x.doubleValue())));
	BigInteger y=x;
	BigInteger p=null;
	for (;;) {
	    y = y.subtract(delta);
	    p=y.nextProbablePrime();
	    if (p.compareTo(x) < 0) break;
	}
	for (;;) {
	    y=p;
	    p=y.nextProbablePrime();
	    if (p.compareTo(x) >= 0) return y;
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
	//	test();
	for (int i=0; i<args.length; ++i) {
	    int b = Integer.parseInt(args[i]);
	    BigInteger x=BigInteger.valueOf(1).shiftLeft(b);
	    BigInteger p = nextPrime(x).subtract(x);
	    BigInteger q = prevPrime(x).subtract(x);
	    System.out.println("np[" + b + "]=" + p + "L");
	    System.out.println("pp[" + b + "]=" + q + "L");
	}
    }
}
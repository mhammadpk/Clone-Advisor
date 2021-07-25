  static int fibonacci(int value, boolean printThis) {
    int result;
    if (value==0 || value==1) {
      result = value;
      if (printThis) {
        System.out.print(result);
        System.out.print(", ");
      }
    } else {
      if (printThis) {
        result =  fibonacci(value-1, true)+fibonacci(value-2, false);
        System.out.print(result);
        System.out.print(", ");
      } else {
        result = fibonacci(value-1, false)+fibonacci(value-2, false);
      }
    }
    return result;
  }

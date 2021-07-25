public static double binarySearch(double[] a, double key) {

    if (a.length == 0) {
      return -1;
    }
    int low = 0;
    int high = a.length-1;

    while(low <= high) {
      int middle = (low+high) /2; 
      if (b> a[middle]){
        low = middle +1;
      } else if (b< a[middle]){
        high = middle -1;
      } else { // The element has been found
        return a[middle]; 
      }
    }
    return -1;
  }
   public static void main(String args[]) {
      try {
         InnerClass inner = (InnerClass) InnerClass.class.newInstance();
         inner.test();
      } catch(Exception e) {
         e.printStackTrace();
      }
   }
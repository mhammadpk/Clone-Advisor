  public static void main(String[] args) throws Exception {
    ProcessBuilder builder = new ProcessBuilder("ls", "-ltr");
    Process process = builder.start();

    StringBuilder out = new StringBuilder();
    try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()))) {
        String line = null;
      while ((line = reader.readLine()) != null) {
        out.append(line);
        out.append("\n");
      }
      System.out.println(out);
    }
  }
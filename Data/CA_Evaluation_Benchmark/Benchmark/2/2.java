public static String savePage(final String URL) throws IOException {
    String line = "", all = "";
    URL myUrl = null;
    BufferedReader in = null;
    try {
        myUrl = new URL(URL);
        in = new BufferedReader(new InputStreamReader(myUrl.openStream()));

        while ((line = in.readLine()) != null) {
            all += line;
        }
    } finally {
        if (in != null) {
            in.close();
        }
    }

    return all;
}
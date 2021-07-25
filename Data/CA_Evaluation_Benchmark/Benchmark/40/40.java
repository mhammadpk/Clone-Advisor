    public void parseFile(final InputStream inStream) {
        final BufferedReader reader = new BufferedReader(new InputStreamReader(
                inStream));
        try {
            startSheet();
            processRows(reader);
            finishSheet();
        } catch (final IOException e) {
            throw new DecisionTableParseException(
                    "An error occurred reading the CSV data.", e);
        }
    }
 
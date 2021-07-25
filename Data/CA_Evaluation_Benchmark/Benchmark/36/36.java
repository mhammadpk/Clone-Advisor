    public void initSQLServer() {
        try {
            Class.forName(DRIVER).newInstance();
            try {
                connection = DriverManager.getConnection(DATABASE_URL, "root", "Dropatrain!248");
                statement = connection.createStatement();
            } catch (SQLException e) {
                System.out.println("SQLException: " + e.getMessage());
                System.out.println("SQLState: " + e.getSQLState());
                System.out.println("VendorError: " + e.getErrorCode());
            }
        } catch (Exception ex) {
            System.out.println(ex);
        }
    }
public void testSharedLocks2()
    throws SQLException 
{
    Statement s = createStatement();
    ResultSet rs = s.executeQuery("select * from t1");
    scrollForward(rs);
    Connection con2 = openDefaultConnection();
    Statement s2 = con2.createStatement();
    try {
        final ResultSet rs2 = s2.executeQuery("select * from t1");
        scrollForward(rs2);
    } finally {
        rs.close();
        con2.rollback();
        con2.close();
    }
    s.close();
}
 
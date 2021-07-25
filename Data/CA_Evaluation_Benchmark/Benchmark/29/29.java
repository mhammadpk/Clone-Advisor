public static Date getDateFromString(String format, String dateStr) {

    DateFormat formatter = new SimpleDateFormat(format);
    Date date = null;
    try {
        date = (Date) formatter.parse(dateStr);
    } catch (ParseException e) {
        e.printStackTrace();
    }

    return date;
}
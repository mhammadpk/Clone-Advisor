private static Font getFont(String name) {
    Font font = null;
    if (name == null) {
        return SERIF_FONT;
    }

    try {
        // load from a cache map, if exists
        if (fonts != null && (font = fonts.get(name)) != null) {
            return font;
        }
        String fName = Params.get().getFontPath() + name;
        File fontFile = new File(fName);
        font = Font.createFont(Font.TRUETYPE_FONT, fontFile);
        GraphicsEnvironment ge = GraphicsEnvironment
                .getLocalGraphicsEnvironment();

        ge.registerFont(font);

        fonts.put(name, font);
    } catch (Exception ex) {
        log.info(name + " not loaded.  Using serif font.");
        font = SERIF_FONT;
    }
    return font;
}
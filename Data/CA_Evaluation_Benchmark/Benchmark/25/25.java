/**
 * Launches a file browser or opens a file with java Desktop.open() if is
 * supported
 * 
 * @param file
 */
private void launchFile(File file) {
    if (!Desktop.isDesktopSupported())
        return;
    Desktop dt = Desktop.getDesktop();
    try {
        dt.open(file);
    } catch (IOException ex) {
        launchFile(file.getPath());
    }
}
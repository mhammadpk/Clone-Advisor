    private File[] selectDir() {
        JFileChooser fileChooser = new JFileChooser(lastDir);
        fileChooser.setMultiSelectionEnabled(true);
        fileChooser.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY);
        int showOpenDialog = fileChooser.showOpenDialog(null);
        if (showOpenDialog != JFileChooser.APPROVE_OPTION) {
            return null;
        }
        File[] uploadDir = fileChooser.getSelectedFiles();
        lastDir = new File(uploadDir[uploadDir.length-1].getParent());
        return uploadDir;
    }
public static void unzip(InputStream inputStream, File targetDirectory) throws IOException, IllegalAccessException {
    try (ZipArchiveInputStream zis = new ZipArchiveInputStream(new BufferedInputStream(inputStream))) {
        ZipArchiveEntry entry = null;
        while ((entry = zis.getNextZipEntry()) != null) {
            File entryDestination = new File(targetDirectory, entry.getName());
            // prevent zipSlip
            if (!entryDestination.getCanonicalPath().startsWith(targetDirectory.getCanonicalPath() + File.separator)) {
                throw new IllegalAccessException("Entry is outside of the target dir: " + entry.getName());
            }
            if (entry.isDirectory()) {
                entryDestination.mkdirs();
            } else {
                entryDestination.getParentFile().mkdirs();
                try (OutputStream out = new FileOutputStream(entryDestination)) {
                    IOUtils.copy(zis, out);
                }
            }

        }
    }
}
 
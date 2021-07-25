public static long getChecksumCRC32(InputStream stream, int bufferSize) 
  throws IOException {
    CheckedInputStream checkedInputStream = new CheckedInputStream(stream, new CRC32());
    byte[] buffer = new byte[bufferSize];
    while (checkedInputStream.read(buffer, 0, buffer.length) >= 0) {}
    return checkedInputStream.getChecksum().getValue();
}
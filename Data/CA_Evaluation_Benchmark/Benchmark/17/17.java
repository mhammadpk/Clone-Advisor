public static void createRSAKeys() throws Exception {
    KeyPairGenerator kpg = KeyPairGenerator.getInstance("RSA");
    kpg.initialize(512);
    KeyPair kp = kpg.genKeyPair();
    RSAPublicKey publicKey = (RSAPublicKey) kp.getPublic();
    RSAPrivateKey privateKey = (RSAPrivateKey) kp.getPrivate();
    KeyFactory fact = KeyFactory.getInstance("RSA");        
    RSAPublicKeySpec pub = fact.getKeySpec(kp.getPublic(), RSAPublicKeySpec.class);
    RSAPrivateKeySpec priv = fact.getKeySpec(kp.getPrivate(), RSAPrivateKeySpec.class);
    saveToFile("keys/public.key", pub.getModulus(), pub.getPublicExponent());
    saveToFile("keys/private.key", priv.getModulus(), priv.getPrivateExponent());
    System.out.println("RSA public & private keys are generated");
}

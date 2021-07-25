 public void testGetMethod() throws SecurityException, NoSuchMethodException, IllegalArgumentException,
            IllegalAccessException, InvocationTargetException {
        Method m = valueObject.getClass().getMethod(methodName, new Class[] {});
        Object ret = m.invoke(valueObject, new Object[] {});
        Assert.assertEquals(11, ret);
    }
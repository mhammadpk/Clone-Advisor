public void initialize(final IPath containerName, IJavaProject project) throws CoreException {
    IPath ws = ResourcesPlugin.getWorkspace().getRoot().getLocation();
    final IPath containerPath = ws.append("../TestContainer/");
    IClasspathContainer container = new IClasspathContainer() {

        public IPath getPath() {
            return containerName;
        }

        public int getKind() {
            return IClasspathContainer.K_APPLICATION;
        }

        public String getDescription() {
            return "Test Container";
        }

        public IClasspathEntry[] getClasspathEntries() {
            if (TestExternalLibContainerInitializer.this.entries == null) {
                TestExternalLibContainerInitializer.this.entries = new IClasspathEntry[] { JavaCore.newLibraryEntry(containerPath, null, null) };
            }
            return TestExternalLibContainerInitializer.this.entries;
        }
    };
    JavaCore.setClasspathContainer(containerName, new IJavaProject[] { project }, new IClasspathContainer[] { container }, null);
}
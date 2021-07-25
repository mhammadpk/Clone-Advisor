@Override
protected void createGraphicalViewer(final Composite parent) {
    _rulerComposite = new RulerComposite(parent, SWT.NONE);
    GraphicalViewer viewer = new PatchedGraphicalViewer();
    viewer.createControl(_rulerComposite);
    setGraphicalViewer(viewer);
    configureGraphicalViewer();
    hookGraphicalViewer();
    initializeGraphicalViewer();
    _rulerComposite.setGraphicalViewer((ScrollingGraphicalViewer) getGraphicalViewer());
    WorkbenchHelpSystem.getInstance().setHelp(_rulerComposite, SdsUiPlugin.PLUGIN_ID + ".synoptic_display_studio");
    viewer.getControl().addKeyListener(keyAdapter);
}
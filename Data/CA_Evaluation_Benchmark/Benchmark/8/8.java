public void createPartControl(Composite parent) {
    graphicalViewer = new ScrollingGraphicalViewer();
    canvas = (FigureCanvas) graphicalViewer.createControl(parent);
    ScalableFreeformRootEditPart root = new ScalableFreeformRootEditPart();
    graphicalViewer.setRootEditPart(root);
    graphicalViewer.setEditDomain(new EditDomain());
    graphicalViewer.setEditPartFactory(new PartFactory());
    graphicalViewer.setContents(diagram);
}
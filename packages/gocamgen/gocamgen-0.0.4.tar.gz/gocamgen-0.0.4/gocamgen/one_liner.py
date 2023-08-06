# Parse GAF file, get assocs
# Create class that accepts list of assocs and creates a model, with connections if len(assocs) > 1
# Interpret extensions field - may require calculating aspect of term; also, determining if GP

from gocamgen.gocamgen import GoCamModel, CamTurtleRdfWriter, Annoton
from ontobio.rdfgen.assoc_rdfgen import SimpleAssocRdfTransform, CamRdfTransform



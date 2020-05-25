package debug.openllet;

import java.io.BufferedOutputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.PrintWriter;
import java.util.logging.Level;

import org.semanticweb.owlapi.apibinding.OWLManager;
import org.semanticweb.owlapi.model.IRI;
import org.semanticweb.owlapi.model.OWLClass;
import org.semanticweb.owlapi.model.OWLNamedIndividual;
import org.semanticweb.owlapi.model.OWLOntology;
import org.semanticweb.owlapi.model.OWLOntologyManager;
import org.semanticweb.owlapi.reasoner.InferenceType;
import openllet.owlapi.OpenlletReasoner;
import openllet.owlapi.OpenlletReasonerFactory;

public class Openllet {
	@SuppressWarnings("deprecation")
	public static void main(String[] args) throws Exception {

		File c=new File(args[0]);
		String task = args[1];
		//File c=new File("C:\\Users\\Gunjan\\Documents\\GitHub\\OWL2Bench\\OWL2Bench\\OWL2RL-10-output.owl");
		//String task = "C";
		IRI physicalIRI = IRI.create(c);
		OWLOntologyManager manager = OWLManager.createOWLOntologyManager();
		OWLOntology ontology = manager.loadOntologyFromOntologyDocument(physicalIRI);
		System.out.println("Total Logical Axiom Count......."+ ontology.getLogicalAxiomCount());
		long startTime = System.nanoTime();
        final OpenlletReasoner reasoner = OpenlletReasonerFactory.getInstance().createReasoner(ontology);
        long endTime = System.nanoTime();
        long duration = ((endTime - startTime));
        System.out.println("Time taken for Reasoner Creation " + duration );
    
        if(task.matches("C")) {
            System.out.println("Started Consistency Checking");
            startTime = System.nanoTime();
            System.out.println(" " + reasoner.isConsistent() );
             endTime = System.nanoTime();
            duration = ((endTime - startTime));
            System.out.println("Time taken for Consistency Check " + duration );
            
            
            }
        else if(task.matches("R")) {
        	System.out.println("Started Instance Checking");
         startTime = System.nanoTime();
      
         for (OWLNamedIndividual individual: ontology.getIndividualsInSignature()) {
        	//for (OWLNamedIndividual individual: ontology.individualsInSignature()) {
        	reasoner.getTypes(individual,false);
    		}
         endTime = System.nanoTime();
         duration = ((endTime - startTime));
        System.out.println("Time taken for Realization " + duration );}
            else if(task.matches("CT")) {
            	System.out.println("Started Classification Time");
             startTime = System.nanoTime();
            reasoner.precomputeInferences(InferenceType.CLASS_HIERARCHY);
             endTime = System.nanoTime();
             duration = ((endTime - startTime));
            System.out.println("Time taken for Classification " + duration );}
            /*
            startTime = System.nanoTime();
            for (OWLClass clazz : ontology.getClassesInSignature()) {
        		reasoner.getInstances(
        		clazz, false);
        		}
            endTime = System.nanoTime();
            duration = ((endTime - startTime));
            System.out.println("Time taken for Retrieval " + duration );
        	//System.out.println(ontology.getIndividualsInSignature());
        	 * 
        	 */
            
	}
}





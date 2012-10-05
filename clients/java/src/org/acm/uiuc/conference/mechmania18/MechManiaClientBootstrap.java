package org.acm.uiuc.conference.mechmania18;

public class MechManiaClientBootstrap {

	// Expected number of arguments on the command line
	// * IP Address of Server
	// * Port Number of Server
	// * Client Key
	private static final int EXPECTED_ARGUMENT_COUNT = 1;
	
	/**
	 * @param args String array of arguments passed in from command line
	 */
	public static void main(String[] args) {
		System.out.println("Found " + args.length + " arguments on command line.");
		
		// Check for argument array length
		if (args.length < EXPECTED_ARGUMENT_COUNT) {
			printUsage();
			System.exit(1);
		}
		
		// We have enough arguments to start the client
		long startupTime = System.currentTimeMillis();
		
		MechManiaGameEnvironment environment = new MechManiaGameEnvironment(
				args[0]  // IP address/hostname of server
				);
		
		MechMania mm18 = new MechMania();
		mm18.start(environment);
		
		// Log time spent running before exiting
		System.out.println("Client ended in " + (System.currentTimeMillis() - startupTime) + "ms");
	}
	
	/**
	 * Print usage parameters.
	 * 
	 * Note that there are not any JVM options output, but are represented by the [...]; this is intentional.
	 * 
	 * Each implementation may perform better with different memory configurations or an alternative
	 * garbage collector.  It is up to the teams to decide what works well for them or if they would
	 * rather stick with the defaults and see where they end up when the smoke settles.
	 * 
	 */
	private static void printUsage() {
		System.out.println("MechMania 18 Java Client");
		System.out.println("Command Line Usage");
		System.out.println();
		System.out.println("JAVA ... <host_addr> <port_num> <clientkey>");
		System.out.println();
		System.out.println("<host_addr> Hostname or IP address of game server to connect to");
		System.out.println("<port_num>  Port number of game server to connect to");
		System.out.println("<clientkey> Access key given to authorize connection to game server");
		System.out.println();
	}

}

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Queue;
import java.util.Scanner;
import java.util.Vector;

public class BaseballElimination {
	private int V = 0;
	private int numberOfTeams = 0;
	private List<String> teams = null;
	private final HashMap<String, Team> teamByName = new HashMap<String, Team>();

	
	public static void main(String[] args) {
//	    BaseballElimination division = new BaseballElimination("/home/ivanmolotkov/Документы/Java/BaseballElimination/src/teams4.txt");
	    BaseballElimination division = new BaseballElimination(args[0]);
	    for (String team : division.teams()) {
	        if (division.isEliminated(team)) {
	            System.out.print(team + " is eliminated by the subset R = { ");
	            for (String t : division.certificateOfElimination(team)) {
	            	System.out.print(t + " ");
	            }
	            System.out.println("}");
	        }
	        else {
	        	System.out.println(team + " is not eliminated");
	        }
	    }
	}
	
	private class FlowEdge {
		private final int v, w;
		private final double capacity;
		private double flow = 0;
		FlowEdge(int v, int w, double capacity) {
			this.v = v;
			this.w = w;
			this.capacity = capacity;
		}
		
		public int from() { return this.v; }
		public int to() {return this.w; }
		public double capacity() { return this.capacity; }
		public double flow() { return this.flow; }
		
		public int other(int vertex) {
			if (vertex == v) return w;
			else if (vertex == w) return v;
			else throw new RuntimeException("Illegal endpoint");
		} 
	
		public double residualCapacityTo(int vertex) {
			if (vertex == v) return this.flow;
			else if (vertex == w) return this.capacity - this.flow;
			else throw new RuntimeException("Illegal endpoint");
		}
	
		public void addResidualFlowTo(int vertex, double delta) {
			if (vertex == v) this.flow -= delta;
			else if (vertex == w) this.flow += delta;
			else throw new RuntimeException("Illegal endpoint");			
		}
	}

	private class Team {
		private final String name;
		private final int wins;
		private final int losses;
		private final int remaining;
		private final int[] remainingGames;
	
		public Team(String name, int wins, int losses, int remaining, int[] gamesAgainstTeams) {
			this.name = name;
			this.wins = wins;
			this.losses = losses;
			this.remaining = remaining;
			this.remainingGames = Arrays.copyOf(gamesAgainstTeams, gamesAgainstTeams.length);
		}
		
		public String name() { return this.name; }
		public int wins() { return this.wins; }
		public int losses() { return this.losses; }
		public int remaining() { return this.remaining; }
		public int remainingAgainst(int teamIndex) { return remainingGames[teamIndex]; }
	}
		
	
	public BaseballElimination(String filename) {
		try {
			Scanner in = new Scanner(new FileInputStream(filename));
			this.numberOfTeams = in.nextInt();
			this.teams = new Vector<String>();
			for (int i = 0; i < numberOfTeams; i++) {
				String name = in.next();
				int w = in.nextInt();
				int l = in.nextInt();
				int r = in.nextInt();
				int[] arr = new int[numberOfTeams];
				for (int j = 0; j < numberOfTeams; j++) arr[j] = in.nextInt(); 
				this.teams.add(name);
				teamByName.put(name, new Team(name, w, l, r, arr));
			}
			this.V = 1 + (numberOfTeams-1)*(numberOfTeams-2)/2 + (numberOfTeams - 1) + 1;
			in.close();
		} catch (FileNotFoundException e) {
			
		}
	}
	
	private class FlowNetwork {
		private final List<FlowEdge>[] adj;
		private FlowEdge[] edgeTo;
		private boolean marked[]; 
		private double value = 0.0;
		private final List<String> relevantTeams;
		
		FlowNetwork(String name) {
			adj = (List<FlowEdge>[]) new Vector[V];
			for (int i = 0; i < V; i++) {
				adj[i] = new Vector<FlowEdge>();
			}
			relevantTeams = new Vector<String>();
			for (String team : teams) {
				if (!team.equals(name)) relevantTeams.add(team);
			}
			
			int z = 1;
			for (int i = 0; i < numberOfTeams-1; i++) {
				for (int j = i+1; j < numberOfTeams-1; j++, z++) {
					addEdge(0, z, against(relevantTeams.get(i), relevantTeams.get(j)));
				}
			}
			int k = 1 + (numberOfTeams-1)*(numberOfTeams-2)/2;
			z = 1;
			for (int i = 0; i < numberOfTeams-1; i++) {
				for (int j = i+1; j < numberOfTeams-1; j++, z++) {
					addEdge(z, k + i, Double.POSITIVE_INFINITY);
					addEdge(z, k + j, Double.POSITIVE_INFINITY);
				}
			}
			for (int i = k; i < V-1; i++) {
				addEdge(i, V-1, wins(name) + remaining(name) - wins(relevantTeams.get(i-k)));
			}
			FordFulkerson();
		}

		private void addEdge(int from, int to, double capacity) {
			if (from < 0 || from >= V || to < 0 || to > V) throw new IllegalArgumentException("Wrong parameters of the edge");
			FlowEdge e = new FlowEdge(from, to, capacity);
			adj[from].add(e);
			adj[to].add(e);
		}
				
		public boolean isEliminated() {
			boolean result = false;
			for (FlowEdge e : adj[0]) {
				if (Math.abs(e.capacity() - e.flow()) > 0.0001) result = true;
			}
			return result;
		}
		

		private void FordFulkerson() {
			while (hasAugmentedPath()) {
				double bottle = Double.POSITIVE_INFINITY;
				for(int v = V-1; v != 0; v = edgeTo[v].other(v)) {
					bottle = Math.min(bottle, edgeTo[v].residualCapacityTo(v));
				}
				for(int v = V-1; v != 0; v = edgeTo[v].other(v)) {
					edgeTo[v].addResidualFlowTo(v, bottle);
				}
				value += bottle;
			}
		}

		private boolean hasAugmentedPath() {
			edgeTo = new FlowEdge[V];
			marked = new boolean[V];
			
			Queue<Integer> q = new LinkedList<Integer>();
			q.add(0);
			while (!q.isEmpty()) {
				int v = q.poll();
				marked[v] = true;
				for (FlowEdge e : adj[v]) {
					int w = e.other(v);
					if (e.residualCapacityTo(w) > 0 && !marked[w]) {
						edgeTo[w] = e;
						marked[w] = true;
						q.add(w);
					}
				}
			}
			return marked[V-1];
		}
		
		public double value() { return value; }
		
	}		
	
	public int numberOfTeams() { return numberOfTeams; }
	public Iterable<String> teams() { return this.teams; }
	
	public int wins(String name) { 
		if (!teams.contains(name)) throw new IllegalArgumentException("Team " + name + "does not exist");
		return teamByName.get(name).wins();
	}
	
	public int losses(String name) { 
		if (!teams.contains(name)) throw new IllegalArgumentException("Team " + name + "does not exist");
		return teamByName.get(name).losses(); 
	}
	
	public int remaining(String name) { 
		if (!teams.contains(name)) throw new IllegalArgumentException("Team " + name + "does not exist");
		return teamByName.get(name).remaining();
	}
	
	public int against(String name1, String name2) {
		if (!teams.contains(name1)) throw new IllegalArgumentException("Team " + name1 + "does not exist");
		if (!teams.contains(name2)) throw new IllegalArgumentException("Team " + name2 + "does not exist");
		int index = 0;
		for (int i = 0; i < teams.size() && !teams.get(i).equals(name1); i++, index = i) {	}
		return teamByName.get(name2).remainingGames[index];
	}
	
	public boolean isEliminated(String name) {
		if (!teams.contains(name)) throw new IllegalArgumentException("Team " + name + "does not exist");
		int max = 0;
		for (String team : teams) {
			max = Math.max(max, wins(team));
		}
		if (max > wins(name) + remaining(name)) {
			return true;
		} else {
			FlowNetwork f = new FlowNetwork(name);
			return f.isEliminated();			
		}
	}
	
	public Iterable<String> certificateOfElimination(String name) {
		if (!teams.contains(name)) throw new IllegalArgumentException("Team " + name + "does not exist");
		if (!isEliminated(name)) return null;
		int max = 0;
		for (String team : teams) {
			max = Math.max(max, wins(team));
		}
		if (max > wins(name) + remaining(name)) {
			return Collections.singletonList(teams.get(0));
		}
		List<String> answer = new Vector<String>();
		for (String team : teams) {
			if (wins(team) + remaining(team) - against(team, name) > wins(name) + remaining(name)) {
				answer.add(team);
			}
		}
		return answer;
	}
}

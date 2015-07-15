package n_queens;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.TreeMap;

public class RunHybrid {
	private static int sizePop = 100;
	private static int maxPop = 400;
	private static int NUM_EXP = 10;
	private static int melhor = Integer.MAX_VALUE;
	private static int pior = 0;
	private static double soma = 0;
	private static double media = 0.0;
	private static double desvio = 0.0;
	private static double variancia = 0.0;
	private final static List<Integer> N = Arrays.asList(6,8,16,32,64,100,300,500);
	private static List<Integer> ataquesAvaliados = new ArrayList<Integer>();

	private static List<Node> best5 = new ArrayList<Node>();

	public static void main(String ... args) {
		System.out.println("\n--------------- Algoritmo Hibrido - Descida de Encosta / Genético para N-Qeens -----------------");
		for(Integer n : N) {
			System.out.println("\n---------------------------------");
			System.out.println("Resultados para N = " +n+"\n" );

			soma = 0;
			media = 0.0;
			desvio = 0.0;
			variancia = 0.0;
			int ataques = 0;

			//Run genetico
			for(int i = 0; i<NUM_EXP; i++) {
				Node solucao = new Node(n);
				solucao= Genetico.runGenetico(n, sizePop, maxPop);
				ataques = solucao.contabilizarAtaques();
				ataquesAvaliados.add(ataques);
				soma += ataques;
				if(ataques < melhor) {
					melhor = ataques;
				}
				if(ataques > pior) {
					pior = ataques;
				}
				calculaBest5();
			}

			//Run descida
			for(Node atual : best5) {
				Node solucao = new Node(n);
				List<Node> vizinhos = atual.gerarVizinhos();
				solucao = new Node(n);
				solucao= DescidaEncosta.runDescidaEncosta(atual,vizinhos);
				ataques = solucao.contabilizarAtaques();
				ataquesAvaliados.add(ataques);

				soma += ataques;
				if(ataques < melhor) {
					melhor = ataques;
				}
				if(ataques > pior) {
					pior = ataques;
				}
			}
			media = (soma/(NUM_EXP + best5.size()));

			for (Integer a : ataquesAvaliados) {
				variancia += Math.pow((((double)a) - media), 2);
			}
			variancia /= (double)NUM_EXP;
			desvio = Math.sqrt(variancia);


			System.out.println("Resultados:");
			System.out.println("\tMelhor:" + melhor);
			System.out.println("\tPior:" + pior);
			System.out.println("\tMédia:" + media);
			System.out.println("\tDesvio:" + desvio);
		}

	}
	private static void calculaBest5() {
		TreeMap<Integer,Node> geneticos = Genetico.getAtaqueEstado();
		int i = 0;
		for(Node n : geneticos.values()) {
			if(i == 5) {
				break;
			}
			best5.add(n);
			i++;
		}
	}
}

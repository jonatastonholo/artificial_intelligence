package n_queens;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class RunGenetico {
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


	public static void main(String ... args) {
		try{
			System.out.println("\n--------------- Algoritmo Genético N-Qeens -----------------");
			for(Integer n : N) {
				soma = 0;
				media = 0.0;
				desvio = 0.0;
				variancia = 0.0;
				System.out.println("\n---------------------------------");
				System.out.println("Resultados para N = " +n+"\n" );
				for(int i = 0; i<NUM_EXP; i++) {
					int ataques = 0;
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
				}
				media = (soma/NUM_EXP);

				for (Integer ataques : ataquesAvaliados) {
					variancia += Math.pow((((double)ataques) - media), 2);
				}
				variancia /= (double)NUM_EXP;
				desvio = Math.sqrt(variancia);


				System.out.println("Resultados:");
				System.out.println("\tMelhor:" + melhor);
				System.out.println("\tPior:" + pior);
				System.out.println("\tMédia:" + media);
				System.out.println("\tDesvio:" + desvio);
			}
		}catch(Exception e) {
			main();
		}
	}
}

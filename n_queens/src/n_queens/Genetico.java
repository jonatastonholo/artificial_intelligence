package n_queens;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.TreeMap;

public final class Genetico {
	private static List<Node> cruzou = new ArrayList<Node>();
	static TreeMap<Integer,Node> ataqueEstado = new TreeMap<Integer, Node>();
	public static Node runGenetico(int size, int sizePop, int maxPop) {
		List<Node> populacao = gerarPopulacao(size, sizePop);
		Node solucao = null;
		for(int i=0; i<maxPop; i++) {
			ataqueEstado = analizarAtaquesPopulacao(populacao);
			if (ataqueEstado.containsKey(0)) {
				// Se encontrar a solução ótima, não precisa continuar.
				solucao = ataqueEstado.get(0);
				break;
			} else if(populacao.size() >= maxPop) {
				solucao = ataqueEstado.get(ataqueEstado.firstKey());
				break;
			}


			List<Node> novaPopulacao = new ArrayList<Node>(populacao.size());

			for(int j=0; j < populacao.size(); j++) {

				//Seleção de pais
				List<Node> paisSelecionados = selecionarCromossomosPais(populacao,novaPopulacao);

				//Cruzando os pais
				List<Node> filhos = cruzarCromossomos(paisSelecionados);

				//mutar filhos nem sempre ocorre
				mutacao(filhos);

				//Apenas 2 filhos são selecionados para a nova população
				List<Node> filhosSelecionados = selecaoFilhos(filhos);

				//Colocar filhos na nova população
				novaPopulacao.addAll(filhosSelecionados);
				//novaPopulacao.addAll(filhos);
			}

			/* Troca a antiga população pela nova população */
			populacao = novaPopulacao;
		}
		return solucao;
	}

	private static List<Node> gerarPopulacao(int size, int sizePop) {
		List<Node> populacao = new ArrayList<Node>(sizePop);

		for(int i = 0; i<sizePop; i++) {
			populacao.add(Node.getRandomState(size));
		}
		return populacao;
	}

	public static TreeMap<Integer,Node> analizarAtaquesPopulacao(List<Node> populacao) {
		Map<Integer,Node> estadoAtaque = new TreeMap<Integer,Node>();

		for(Node state : populacao) {
			if(state != null) {
				estadoAtaque.put(state.contabilizarAtaques(),state);
			}
		}

		return (TreeMap<Integer, Node>) estadoAtaque;
	}

	private static List<Node> selecionarCromossomosPais(List<Node> populacao, List<Node> novaPopulacao) {
		Random rand = new Random();
		int melhor1 = Integer.MAX_VALUE;
		//Buscar melhores pais, i.e. Menor ataque

		Node cromossomo1 = null;
		Node cromossomo2 = null;

		do {
			for(Node n : populacao) {
				if(n!=null) {
					int ataque = n.contabilizarAtaques();
					if(ataque < melhor1) {
						melhor1 = ataque;
						cromossomo1 = n;
					}
				} else {
					cromossomo1 = Node.getRandomState(populacao.get(0).getSize());
					int ataque = cromossomo1.contabilizarAtaques();
					if(ataque < melhor1) {
						melhor1 = ataque;
						cromossomo1 = n;
					}
				}
			}
		} while(cromossomo1 == null);

		do{

			do{
				int selecao = rand.nextInt(populacao.size() - 1);
				cromossomo2 = populacao.get(selecao);
			}while(cromossomo2 == null);



		}while((cromossomo1 == cromossomo2)) ;


		return Arrays.asList(cromossomo1,cromossomo2);
	}

	private static List<Node> cruzarCromossomos(List<Node> pais) {
		//Cruzamento 50-50

		Node cromossomo1 = pais.get(0);
		Node cromossomo2 = pais.get(1);

		cruzou.addAll(pais);

		//cromo 1
		List<Integer> meioCromossomo11 = cromossomo1.getTabuleiro().subList(0, (cromossomo1.getSize()/2));
		List<Integer> meioCromossomo12 = cromossomo1.getTabuleiro().subList((cromossomo1.getSize()/2), cromossomo1.getSize());
		//cromo 2
		List<Integer> meioCromossomo21 = cromossomo2.getTabuleiro().subList(0, (cromossomo2.getSize()/2));
		List<Integer> meioCromossomo22 = cromossomo2.getTabuleiro().subList((cromossomo2.getSize()/2), cromossomo2.getSize());

		//Cruzamento gera 4 filhos
		List<Integer> novoEstadoFilho1 = new ArrayList<Integer>();
		List<Integer> novoEstadoFilho2 = new ArrayList<Integer>();
		List<Integer> novoEstadoFilho3 = new ArrayList<Integer>();
		List<Integer> novoEstadoFilho4 = new ArrayList<Integer>();

		novoEstadoFilho1.addAll(meioCromossomo11);
		novoEstadoFilho1.addAll(meioCromossomo21);

		novoEstadoFilho2.addAll(meioCromossomo11);
		novoEstadoFilho2.addAll(meioCromossomo22);

		novoEstadoFilho3.addAll(meioCromossomo12);
		novoEstadoFilho3.addAll(meioCromossomo21);

		novoEstadoFilho4.addAll(meioCromossomo12);
		novoEstadoFilho4.addAll(meioCromossomo22);

		Node filho1 = new Node(cromossomo1.getSize());
		filho1.setTabuleiro(novoEstadoFilho1);

		Node filho2 = new Node(cromossomo1.getSize());
		filho2.setTabuleiro(novoEstadoFilho2);

		Node filho3 = new Node(cromossomo1.getSize());
		filho3.setTabuleiro(novoEstadoFilho3);

		Node filho4 = new Node(cromossomo1.getSize());
		filho4.setTabuleiro(novoEstadoFilho4);

		if(filho1.getTabuleiro().size() > filho1.getSize() ||
				filho2.getTabuleiro().size() > filho2.getSize() ||
				filho3.getTabuleiro().size() > filho3.getSize() ||
				filho4.getTabuleiro().size() > filho4.getSize() ) {
			System.out.println("");
		}


		return Arrays.asList(filho1,filho2,filho3,filho4);
	}

	private static void mutacao(List<Node> filhos) {
		//Mutar aleatoriamente uma peça no tabuleiro de cada filho sujeito à uma chance de 5%
		int chanceMutar = 5;
		Random rand = new Random();

		for (Node filho : filhos) {
			if(rand.nextInt(100) < chanceMutar) {
				filho.mutacao(rand.nextInt(filho.getSize()), filho.getTabuleiro());
			}
		}
	}

	private static List<Node> selecaoFilhos(List<Node> filhos){
		int melhor1 = Integer.MAX_VALUE;
		int melhor2 = Integer.MAX_VALUE;
		Node melhorFilho1 = null;
		Node melhorFilho2 = null;

		for(Node n : filhos) {
			int ataque = n.contabilizarAtaques();
			if(ataque < melhor1) {
				melhor1 = ataque;
				melhorFilho1 = n;
			}
		}
		for(Node n : filhos) {
			int ataque = n.contabilizarAtaques();
			if(ataque > melhor1 && ataque < melhor2) {
				melhor2 = ataque;
				melhorFilho2 = n;
			}
		}
		return Arrays.asList(melhorFilho1, melhorFilho2);
	}
	public static TreeMap<Integer, Node> getAtaqueEstado() {
		return ataqueEstado;
	}

}

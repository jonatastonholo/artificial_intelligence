package n_queens;


import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Random;

/**
 * @author Jônatas
 *
 */
public class Node {
	private List<Integer> tabuleiro;
	private int size;

	public Node(int size) {
		this.size = size;
		tabuleiro = new ArrayList<Integer>(size);
	}

	/**
	 * @return the tabuleiro
	 */
	public List<Integer> getTabuleiro() {
		return tabuleiro;
	}

	/**
	 * @param tabuleiro the tabuleiro to set
	 */
	public void setTabuleiro(List<Integer> tabuleiro) {
		this.tabuleiro = tabuleiro;
	}

	/**
	 * @return the size
	 */
	public int getSize() {
		return size;
	}

	/**
	 * @param size the size to set
	 */
	public void setSize(int size) {
		this.size = size;
	}

	/**
	 * Função objetivo
	 * @return ataques
	 */
	public int contabilizarAtaques() {
		int ataques = 0;

		for (int i=0; i<tabuleiro.size(); i++) { // coluna
			for(int j = i; j<tabuleiro.size(); j++) { // coluna

				//ataques na mesma linha
				if(tabuleiro.get(i) == tabuleiro.get(j)) {
					ataques++;
				}
				else if(tabuleiro.get(j) == tabuleiro.get(i) + (j - i) ) { // Diagonais anteriores
					ataques++;
				}
				else if (tabuleiro.get(i) == tabuleiro.get(j) - (j - i)) { // Diagonais posteriores
					ataques++;
				}

			}
		}

		return ataques;
	}

	/**
	 * Inicia tabuleiro [0 1 2 3 4 ...]
	 */
	public void setInitialState() {

		for(int i = 0; i < this.size; i++){
			this.tabuleiro.add(i);
		}

	}

	public static Node getRandomState(int size) {
		Node newNode = new Node(size);
		Random rand = new Random();
		for (int i = 0; i<size; i++) {
			newNode.getTabuleiro().add(i, rand.nextInt(size));
		}
		return newNode;
	}

	public List<Node> gerarVizinhos() {
		List<Node> vizinhos = new ArrayList<Node>();
		for (int i = 0; i < size; i++) {
			for (int j = 0; j < size; j++) {
				if (tabuleiro.get(i) != j) { // Não gerar na mesma linha
					Node vizinho = new Node(size);
					vizinho.tabuleiro.addAll(tabuleiro);
					Collections.shuffle(vizinho.tabuleiro);
					vizinhos.add(vizinho);
				}
			}
		}
		return vizinhos;
	}

	public void mutacao(int posicaoGene, List<Integer> tabuleiro) {
		if(tabuleiro != null && !tabuleiro.isEmpty()) {
			Random rand = new Random();
			int valorAnterior = tabuleiro.get(posicaoGene);
			do {
				tabuleiro.add(posicaoGene,rand.nextInt(size));
			} while(tabuleiro.get(posicaoGene) == valorAnterior);
		}
	}
}

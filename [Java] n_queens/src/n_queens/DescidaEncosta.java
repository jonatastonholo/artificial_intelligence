package n_queens;

import java.util.ArrayList;
import java.util.List;

public final class DescidaEncosta {
	private static int ataques_atual = Integer.MAX_VALUE;
	private static int ataques_Vizinho = Integer.MIN_VALUE;
	private static int min_value = Integer.MAX_VALUE;
	private static List<Node> vizinhos = new ArrayList<Node>();

	public static Node runDescidaEncosta(Node atual, List<Node> vizinhos) {
		Node solucao = new Node(atual.getSize());
		ataques_atual = atual.contabilizarAtaques();
		boolean isSolucao = true;
		while(isSolucao) {
			for(Node vizinho : vizinhos) {
				if(vizinho.contabilizarAtaques() < ataques_atual) {
					solucao = vizinho;
					ataques_atual = vizinho.contabilizarAtaques();
				} else {
					isSolucao = false;
				}
			}
		}
		return solucao;
	}
}
